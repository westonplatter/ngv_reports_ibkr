# Upgrade ib_async v2 to v3 - Plan

- **Status:** IN PROGRESS. Steps 1 to 3 of "Order of work" are done: `ib-async>=2.1,<3`
  is declared, the code runs on both v2 and v3 through
  `ngv_reports_ibkr/ib_async_compat.py`, and CI tests v3 built from
  `next-protobuf`. v3 is not on PyPI yet (latest is 2.1.0).
- **Source:** the upstream
  [v3 migration guide](https://github.com/ib-api-reloaded/ib_async/blob/next-protobuf/docs/migration/v3.md),
  plus a read of v3's `flexreport.py` and `util.py` on the `next-protobuf` branch.
- **Scope:** what has to change, or be checked, in this package before it supports
  v3.

## Why act before the release

- `pyproject.toml` declares `ib-async` with no version bound.
- The first lock upgrade after v3 ships pulls it in, both here and in every
  downstream project. ngv-trader's FlexQuery trade and position sync is built on
  `CustomFlexReport`.
- Next release: declare `ib-async>=2.1,<3`. Lift the bound only once the work below
  lands.

## 1. `FlexReport.df()` returns polars (blocking)

v3's `FlexReport.df()` calls `util.df()`, which now builds a polars DataFrame and
needs the `ib_async[polars]` extra. Every method on `CustomFlexReport` uses pandas:
`.unique()`, boolean indexing, `.query()`, `.copy()`, the `parse_*_series`
transforms, and the pandera `pandas` schemas.

**Fix:** override `df` once on `CustomFlexReport`. Every method stays pandas, and no
polars dependency is added.

```python
from ib_async import util


class CustomFlexReport(FlexReport):
    def df(self, topic: str, parseNumbers: bool = True) -> pd.DataFrame:
        # v3: pandasDf; v2: util.df already returns pandas.
        to_pandas = getattr(util, "pandasDf", util.df)
        return to_pandas(self.extract(topic, parseNumbers))
```

- `util.pandasDf` is new in v3. On v2, `util.df` already returns pandas, so the
  `getattr` fallback works on both versions.
- `extract()` is unchanged: values are still parsed to `float` and then `int`, with
  no `Decimal`. So the Flex columns keep their v2 dtypes, and the
  `ibkr_flex_report` schemas are unaffected.
- **Empty topic:** v2 `util.df([])` returned `None`. v3 `pandasDf([])` returns an
  empty DataFrame with no columns.
  - `account_ids`, `open_positions_by_account_id` and `trades_by_account_id`
    already handle both cases.
  - `orders_by_account_id` and `change_in_nav_by_account_id` fail on either
    version: `None.query` on v2, and an undefined `accountId` column on v3. Add the
    same early return the other methods have.
- `change_in_nav_by_account_id` queries `accountId == account_id` without the `@`
  prefix. pandas looks for a column named `account_id` and raises
  `UndefinedVariableError`. This is an existing bug, worth fixing in the same
  change.
- `FlexReport.load()` now raises `FlexError` for a file that is not XML, where v2
  raised `ParseError`. Check `load_report` callers that catch the old error.

## 2. TWS trades: `Decimal` breaks the float64 schemas

In v3, execution, commission and order-status numbers are `Decimal | None`. In
pandas they become `object` columns. `schemas/ibkr_tws_trades.py` declares them
`float64` with `coerce=False`, so validation fails:

| Source | Columns |
| --- | --- |
| `Execution` | `fill_shares`, `fill_price`, `fill_cumQty`, `fill_avgPrice` |
| `CommissionReport` | `fill_commission`, `fill_realizedPNL` |
| `OrderStatus` | `filled`, `remaining`, `avgFillPrice` |
| `Order` | `totalQuantity`, `lmtPrice`, `filledQuantity`, ... |

**Fix:** convert to `float` at the expand step in `expand_contract_columns.py`
(`expand_order_status_column`, `expand_fills_and_logs`, and
`extract_object_attributes` for `Order`), keeping `None` as `None`. This leaves the
schemas and `unified_df.prepare_tws_trades` unchanged. The alternative is
`coerce=True` on those columns.

`prepare_tws_trades` does `-tws_df["fill_commission"].abs()`. That works on an
`object` column of `Decimal`s, but it would mix with float `NaN`s, so converting at
the expand step is the cleaner fix.

## 3. `commission` renamed to `commissionAndFees`

- `expand_fills_and_logs` reads `commissionReport.commission`. This works in v3
  with a `DeprecationWarning` and is removed in v4.
- v2.1.0's `CommissionReport` has no `commissionAndFees`. Read the new name first
  and fall back to the old one until v2 support is dropped.
- The output column stays `fill_commission`, so `unified_df` and the schemas are
  unaffected.

## 4. Unset sentinels become `None`

- v3 sets unset numeric fields to `None` instead of `UNSET_DOUBLE`,
  `UNSET_INTEGER` or NaN.
- `_clean_unset_value` becomes a no-op on v3, which is harmless. Keep it while v2 is
  supported.
- `tests/test_extract_object_attributes.py` asserts that a `MarketOrder`'s
  `lmtPrice` and `auxPrice` are `None` after cleaning. That still holds, but the
  comments describing `UNSET_DOUBLE` will be stale.
- `Order.totalQuantity` becomes `Decimal("50")`. It still equals `50`, so the
  current assertions pass.

## 5. Order types and records

- `LimitOrder` and `MarketOrder` are now functions that return a plain `Order`, and
  are still importable from `ib_async`.
  - The tests only call them, so they should pass.
  - `extract_object_attributes` walks `dir(order)`, so confirm its output keys
    don't change on the v3 `Order` dataclass (new fields such as `slOrderId` and
    `postOnly` will appear).
- `Fill`, `Position` and similar records are now slotted frozen dataclasses with no
  `__dict__`.
  - `utils/objects.gen_json` serializes with `getattr(o, "__dict__", str(o))`. For
    these records it would emit the `repr` string instead of a dict.
  - Switch it to `dataclasses.asdict` for dataclasses, and `str` for `Decimal`.
- **Pickled v2 snapshots** (`data/snapshots/`, read by
  `tests/test_unified_trades_manual.py`) reference v2 classes such as
  `ib_async.order.LimitOrder`, which no longer exist. Expect them not to unpickle
  on v3, and re-capture them on v3.
- `test_unified_trades_manual.py` calls `util.df(trades)` and then uses pandas.
  Switch it to `util.pandasDf`.

## 6. Python and CI

- v3 requires Python 3.11 or later. This package declares `>=3.10`, and CI tests
  3.10 to 3.14, with docs built on 3.10.
- Raise `requires-python` to `>=3.11`, drop 3.10 from the CI matrix, and move the
  docs build to 3.11 or later. This is a breaking change for consumers on 3.10, so
  release it as `feat!` / `BREAKING CHANGE`.
- v3 pulls in `protobuf>=7` and `aeventkit>=3`. Check that they resolve alongside
  this package's other dependencies.

## 7. Tests to add

- A `CustomFlexReport` test against a small anonymized XML fixture. It should check
  that `df()` returns pandas, and cover the empty-topic paths in section 1.
- An `expand_fills_and_logs` test with `Decimal` and `None` execution and commission
  values, validated against the TWS schema.
- Run once with `-W error::DeprecationWarning` on v3.

## Order of work

1. Release with `ib-async>=2.1,<3`.
2. Make the changes in sections 1 to 5 so they work on both versions (`df`
   override, float conversion, `commissionAndFees` fallback, `gen_json`), with the
   new tests.
3. Add a CI job (`ci-ib-async-v3`) that tests against v3 on Python 3.11 or later.
   Until v3 is on PyPI, it builds the wheel from the upstream `next-protobuf`
   branch, generating the protobuf bindings (`ib_async/_pb/`, not in git) first.
4. Once that job passes, widen the bound to `ib-async>=2.1,<4`. This supports both versions with no
   breaking change: Python 3.10 resolves v2, and 3.11 or later can resolve v3.
5. To drop v2 later: bump to `ib-async>=3,<4`, raise `requires-python` (section 6),
   remove the v2 fallbacks, re-capture the snapshots, and release as a major
   version.
6. Bump downstream consumers (ngv-trader) and lift their `<3` pins.
