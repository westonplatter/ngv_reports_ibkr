"""
Tests for code that must behave the same on ib_async v2 and v3.

v3 is not on PyPI yet, so these build v3-shaped objects by hand: Decimal
numbers, ``commissionAndFees``, and ``util.pandasDf``.
"""

from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
from ib_async import util

from ngv_reports_ibkr.custom_flex_report import CustomFlexReport
from ngv_reports_ibkr.expand_contract_columns import (
    expand_fills_and_logs,
    expand_order_status_column,
    extract_object_attributes,
)
from ngv_reports_ibkr.ib_async_compat import commission_and_fees, pandas_df, to_float
from ngv_reports_ibkr.utils.objects import gen_json

FLEX_XML = """<FlexQueryResponse queryName="test" type="AF">
<FlexStatements count="1">
<FlexStatement accountId="U1234567" fromDate="20250115" toDate="20250115">
<AccountInformation accountId="U1234567" currency="USD" />
<Trades>
<Trade accountId="U1234567" symbol="MES" quantity="1" tradePrice="6000.25" />
<Trade accountId="U9999999" symbol="MNQ" quantity="-2" tradePrice="21000.5" />
</Trades>
<ChangeInNAV accountId="U1234567" startingValue="1000" endingValue="1100" />
<ChangeInNAV accountId="U9999999" startingValue="2000" endingValue="2100" />
</FlexStatement>
</FlexStatements>
</FlexQueryResponse>
"""


@pytest.fixture
def flex_report(tmp_path: Path) -> CustomFlexReport:
    path = tmp_path / "report.xml"
    path.write_text(FLEX_XML)
    return CustomFlexReport(path=str(path))


def test_to_float():
    assert to_float(Decimal("1.5")) == 1.5
    assert isinstance(to_float(Decimal("1.5")), float)
    assert to_float(None) is None
    assert to_float(2.0) == 2.0
    assert to_float("x") == "x"


def test_commission_and_fees_prefers_v3_name():
    v3 = SimpleNamespace(commissionAndFees=Decimal("1.25"), commission=Decimal(9))
    v2 = SimpleNamespace(commission=1.25)
    assert commission_and_fees(v3) == Decimal("1.25")
    assert commission_and_fees(v2) == 1.25
    assert commission_and_fees(None) is None


def test_pandas_df_uses_pandasDf_when_present(monkeypatch):
    calls = []

    def fake_pandas_df(objs):
        calls.append(objs)
        return pd.DataFrame(objs)

    monkeypatch.setattr(util, "pandasDf", fake_pandas_df, raising=False)
    df = pandas_df([{"a": 1}])
    assert calls == [[{"a": 1}]]
    assert isinstance(df, pd.DataFrame)


def test_pandas_df_falls_back_to_util_df(monkeypatch):
    # v2 has no pandasDf, and its util.df returns pandas.
    calls = []

    def fake_v2_df(objs):
        calls.append(objs)
        return pd.DataFrame(objs)

    monkeypatch.delattr(util, "pandasDf", raising=False)
    monkeypatch.setattr(util, "df", fake_v2_df)
    df = pandas_df([{"a": 1}])
    assert calls == [[{"a": 1}]]
    assert df["a"].tolist() == [1]


def test_flex_df_returns_pandas(flex_report):
    df = flex_report.df("Trade")
    assert isinstance(df, pd.DataFrame)
    assert len(df.index) == 2


def test_flex_empty_topic_returns_none(flex_report):
    assert flex_report.orders_by_account_id("U1234567") is None


def test_flex_empty_topic_returns_none_with_v3_empty_frame(flex_report, monkeypatch):
    # v3 pandasDf([]) returns an empty DataFrame with no columns.
    real_to_pandas = getattr(util, "pandasDf", util.df)
    monkeypatch.setattr(util, "pandasDf", lambda objs: real_to_pandas(objs) if objs else pd.DataFrame(columns=[]), raising=False)
    assert flex_report.orders_by_account_id("U1234567") is None
    assert flex_report.change_in_nav_by_account_id("U1234567") is not None


def test_change_in_nav_by_account_id_filters(flex_report):
    df = flex_report.change_in_nav_by_account_id("U1234567")
    assert df["accountId"].tolist() == ["U1234567"]
    assert df["endingValue"].tolist() == [1100]


def _v3_fill(shares, price, commission, realized_pnl):
    return SimpleNamespace(
        time=None,
        execution=SimpleNamespace(
            execId="0000abcd.12345678.01.01",
            time=None,
            shares=shares,
            price=price,
            exchange="CME",
            side="BOT",
            cumQty=shares,
            avgPrice=price,
        ),
        commissionReport=SimpleNamespace(commissionAndFees=commission, currency="USD", realizedPNL=realized_pnl),
        contract=SimpleNamespace(conId=600000001),
    )


def test_expand_fills_converts_decimal_to_float():
    df = pd.DataFrame(
        {
            "orderId": [1, 2],
            "fills": [
                [_v3_fill(Decimal(1), Decimal("6000.25"), Decimal("0.62"), None)],
                [_v3_fill(Decimal(2), Decimal("21000.5"), Decimal("1.24"), Decimal("10.5"))],
            ],
            "log": [[], []],
        }
    )
    out = expand_fills_and_logs(df)
    for col in ["fill_shares", "fill_price", "fill_cumQty", "fill_avgPrice", "fill_commission", "fill_realizedPNL"]:
        assert out[col].dtype == "float64", col
    assert out["fill_commission"].tolist() == [0.62, 1.24]
    assert pd.isna(out["fill_realizedPNL"].iloc[0])


def test_expand_order_status_converts_decimal_to_float():
    status = SimpleNamespace(status="Filled", filled=Decimal(1), remaining=Decimal(0), avgFillPrice=Decimal("6000.25"), lastFillPrice=Decimal("6000.25"))
    out = expand_order_status_column(pd.DataFrame({"orderStatus": [status]}))
    for col in ["filled", "remaining", "avgFillPrice", "lastFillPrice"]:
        assert out[col].dtype == "float64", col


def test_extract_object_attributes_converts_decimal_when_cleaning():
    order = SimpleNamespace(totalQuantity=Decimal(50), lmtPrice=None, orderType="MKT")
    data = extract_object_attributes(order, clean_numeric=True)
    assert data["totalQuantity"] == 50.0
    assert isinstance(data["totalQuantity"], float)
    assert data["lmtPrice"] is None


def test_gen_json_handles_slotted_dataclass_and_decimal():
    from dataclasses import dataclass

    @dataclass(frozen=True, slots=True)
    class Record:
        execId: str
        shares: Decimal

    assert gen_json({"fill": Record("0000abcd.12345678.01.01", Decimal("1.5"))}) == {
        "fill": {"execId": "0000abcd.12345678.01.01", "shares": "1.5"}
    }
