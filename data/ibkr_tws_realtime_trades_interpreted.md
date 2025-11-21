# DataFrame Schema

## Overview

- **Rows**: 29
- **Columns**: 68
- **Memory Usage**: 0.05 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values |
|--------|-----------|------------|--------|---------------|
| `advancedError` | `object` | 0 | 0.0% | , ,  |
| `conId` | `int64` | 0 | 0.0% | 400000001, 400000002, 400000003 |
| `symbol` | `object` | 0 | 0.0% | BABA, MES, MNQ |
| `secType` | `object` | 0 | 0.0% | OPT, FUT, FUT |
| `exchange` | `object` | 0 | 0.0% | SMART, CME, CME |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `localSymbol` | `object` | 0 | 0.0% | BABA  251121C001000000, MESZ5, MNQZ5 |
| `tradingClass` | `object` | 0 | 0.0% | BABA, MES, MNQ |
| `lastTradeDateOrContractMonth` | `object` | 0 | 0.0% | 20251121, 20251219, 20251219 |
| `multiplier` | `object` | 0 | 0.0% | 100, 5, 2 |
| `strike` | `float64` | 0 | 0.0% | 162.5, 0.0, 0.0 |
| `right` | `object` | 0 | 0.0% | C, ?, ? |
| `orderId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `permId` | `int64` | 0 | 0.0% | 8888888, 9999999, 7777777 |
| `parentId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `clientId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `action` | `object` | 0 | 0.0% | BUY, BUY, SELL |
| `orderType` | `object` | 0 | 0.0% | LMT, LMT, LMT |
| `totalQuantity` | `float64` | 0 | 0.0% | 0.0, 1.0, 1.0 |
| `filledQuantity` | `float64` | 0 | 0.0% | 1.0, 0.0, 0.0 |
| `lmtPrice` | `float64` | 0 | 0.0% | 0.08, 6683.75, 24686.0 |
| `auxPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `trailStopPrice` | `object` | 29 | 100.0% |  |
| `trailingPercent` | `object` | 29 | 100.0% |  |
| `tif` | `object` | 0 | 0.0% | DAY, GTC, DAY |
| `goodAfterTime` | `object` | 0 | 0.0% | , ,  |
| `goodTillDate` | `object` | 0 | 0.0% | , ,  |
| `account_id` | `object` | 0 | 0.0% | U9999999, U9999999, U9999999 |
| `openClose` | `object` | 0 | 0.0% | , ,  |
| `origin` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `outsideRth` | `bool` | 0 | 0.0% | False, False, False |
| `ocaGroup` | `object` | 0 | 0.0% | , ,  |
| `ocaType` | `int64` | 0 | 0.0% | 3, 3, 3 |
| `orderRef` | `object` | 0 | 0.0% | , ,  |
| `transmit` | `bool` | 0 | 0.0% | True, True, True |
| `hidden` | `bool` | 0 | 0.0% | False, False, False |
| `allOrNone` | `bool` | 0 | 0.0% | False, False, False |
| `discretionaryAmt` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `triggerPrice` | `object` | 29 | 100.0% |  |
| `adjustedStopPrice` | `object` | 29 | 100.0% |  |
| `adjustedStopLimitPrice` | `object` | 29 | 100.0% |  |
| `algoStrategy` | `object` | 0 | 0.0% | , ,  |
| `algoParams` | `object` | 0 | 0.0% | [], [], [] |
| `cashQty` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `whatIf` | `bool` | 0 | 0.0% | False, False, False |
| `notHeld` | `bool` | 0 | 0.0% | False, False, False |
| `status` | `object` | 0 | 0.0% | Filled, Cancelled, Cancelled |
| `filled` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `remaining` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `avgFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `lastFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `fill_time_direct` | `datetime64[ns, UTC]` | 5 | 17.2% | 2025-01-20 15:30:00+00:00, 2025-01-20 16:15:00+00:00, 202... |
| `fill_execution_id` | `object` | 5 | 17.2% | 0000wxyz.abcd1234.01.01, 0000efgh.5678ijkl.01.01, 0000mnop... |
| `fill_execution_time` | `datetime64[ns, UTC]` | 5 | 17.2% | 2025-01-20 15:30:00+00:00, 2025-01-20 16:15:00+00:00, 202... |
| `fill_shares` | `float64` | 5 | 17.2% | 1.0, 1.0, 1.0 |
| `fill_price` | `float64` | 5 | 17.2% | 0.08, 224.75, 40.5 |
| `fill_exchange` | `object` | 5 | 17.2% | MEMX, CME, CME |
| `fill_side` | `object` | 5 | 17.2% | BOT, SLD, BOT |
| `fill_cumQty` | `float64` | 5 | 17.2% | 1.0, 1.0, 1.0 |
| `fill_avgPrice` | `float64` | 5 | 17.2% | 0.08, 224.75, 40.5 |
| `fill_commission` | `float64` | 5 | 17.2% | 1.5059, 0.47, 0.47 |
| `fill_commissionCurrency` | `object` | 5 | 17.2% | USD, USD, USD |
| `fill_realizedPNL` | `float64` | 5 | 17.2% | 296.4454, 0.0, 284.06 |
| `fill_contract_conId` | `float64` | 5 | 17.2% | 600000001.0, 600000002.0, 600000003.0 |
| `log_time` | `datetime64[ns, UTC]` | 5 | 17.2% | 2025-01-20 15:30:00+00:00, 2025-01-20 16:15:00+00:00, 202... |
| `log_status` | `object` | 5 | 17.2% | Filled, Filled, Filled |
| `log_message` | `object` | 5 | 17.2% | Fill 1.0@0.08, Fill 1.0@224.75, Fill 1.0@40.5 |
| `log_errorCode` | `float64` | 5 | 17.2% | 0.0, 0.0, 0.0 |

## Data Type Summary

- **object**: 33 columns
- **float64**: 19 columns
- **int64**: 7 columns
- **bool**: 6 columns
- **datetime64[ns, UTC]**: 3 columns

## Columns with Missing Data

- `trailStopPrice`: 29 nulls (100.0%)
- `trailingPercent`: 29 nulls (100.0%)
- `triggerPrice`: 29 nulls (100.0%)
- `adjustedStopPrice`: 29 nulls (100.0%)
- `adjustedStopLimitPrice`: 29 nulls (100.0%)
- `fill_time_direct`: 5 nulls (17.2%)
- `fill_execution_id`: 5 nulls (17.2%)
- `fill_execution_time`: 5 nulls (17.2%)
- `fill_shares`: 5 nulls (17.2%)
- `fill_price`: 5 nulls (17.2%)
- `fill_exchange`: 5 nulls (17.2%)
- `fill_side`: 5 nulls (17.2%)
- `fill_cumQty`: 5 nulls (17.2%)
- `fill_avgPrice`: 5 nulls (17.2%)
- `fill_commission`: 5 nulls (17.2%)
- `fill_commissionCurrency`: 5 nulls (17.2%)
- `fill_realizedPNL`: 5 nulls (17.2%)
- `fill_contract_conId`: 5 nulls (17.2%)
- `log_time`: 5 nulls (17.2%)
- `log_status`: 5 nulls (17.2%)
- `log_message`: 5 nulls (17.2%)
- `log_errorCode`: 5 nulls (17.2%)
