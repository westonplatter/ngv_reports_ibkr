"""
Tests for IbkrTws real-time data source and positions export.

Uses mock ib_async objects to validate:
1. IbkrTws.positions_df() returns a validated DataFrame
2. The DataFrame matches the Pandera positions schema
3. TwsReportOutputAdapterPandas delegates correctly
4. Edge cases: empty positions, multiple asset types
"""

from collections import namedtuple
from unittest.mock import MagicMock

import pandas as pd
import pandera.pandas as pa
import pytest
from ib_async import Contract, Future, Option, Stock

from ngv_reports_ibkr.ibkr_tws import IbkrTws, TwsReportOutputAdapterPandas
from ngv_reports_ibkr.schemas.ibkr_tws_positions import (
    ibkr_tws_positions_schema,
    validate_ibkr_tws_positions,
    validate_ibkr_tws_positions_lazy,
)


# ib_async Position is a namedtuple: (account, contract, position, avgCost)
Position = namedtuple("Position", ["account", "contract", "position", "avgCost"])


def _make_fut_contract():
    """Create a realistic futures contract (MCL Crude Oil)."""
    c = Future()
    c.conId = 345678901
    c.symbol = "MCL"
    c.secType = "FUT"
    c.exchange = "NYMEX"
    c.currency = "USD"
    c.localSymbol = "MCLG6"
    c.tradingClass = "MCL"
    c.lastTradeDateOrContractMonth = "20260219"
    c.multiplier = "100"
    c.strike = 0.0
    c.right = ""
    return c


def _make_stk_contract():
    """Create a realistic stock contract (AAPL)."""
    c = Stock()
    c.conId = 265598
    c.symbol = "AAPL"
    c.secType = "STK"
    c.exchange = "SMART"
    c.currency = "USD"
    c.localSymbol = "AAPL"
    c.tradingClass = "AAPL"
    c.lastTradeDateOrContractMonth = ""
    c.multiplier = ""
    c.strike = 0.0
    c.right = ""
    return c


def _make_opt_contract():
    """Create a realistic option contract (AAPL call)."""
    c = Option()
    c.conId = 123456789
    c.symbol = "AAPL"
    c.secType = "OPT"
    c.exchange = "SMART"
    c.currency = "USD"
    c.localSymbol = "AAPL  260220C00200000"
    c.tradingClass = "AAPL"
    c.lastTradeDateOrContractMonth = "20260220"
    c.multiplier = "100"
    c.strike = 200.0
    c.right = "C"
    return c


def _make_positions_single():
    """Single futures position."""
    return [
        Position(
            account="U1234567",
            contract=_make_fut_contract(),
            position=2.0,
            avgCost=5836.54,
        )
    ]


def _make_positions_mixed():
    """Multiple positions across asset types."""
    return [
        Position(
            account="U1234567",
            contract=_make_fut_contract(),
            position=2.0,
            avgCost=5836.54,
        ),
        Position(
            account="U1234567",
            contract=_make_stk_contract(),
            position=100.0,
            avgCost=185.50,
        ),
        Position(
            account="U1234567",
            contract=_make_opt_contract(),
            position=-5.0,
            avgCost=3.25,
        ),
    ]


# ---------------------------------------------------------------------------
# IbkrTws.positions_df tests
# ---------------------------------------------------------------------------


def test_positions_df_returns_dataframe():
    """Test that positions_df returns a pandas DataFrame."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_single()

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


def test_positions_df_returns_none_for_empty():
    """Test that positions_df returns None when account has no positions."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = []

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    assert df is None


def test_positions_df_expands_contract_fields():
    """Test that contract objects are expanded into flat DataFrame columns."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_single()

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    # Contract column should be gone, replaced with flat fields
    assert "contract" not in df.columns

    # Core contract fields should be present
    assert "conId" in df.columns
    assert "symbol" in df.columns
    assert "secType" in df.columns
    assert "exchange" in df.columns
    assert "currency" in df.columns

    # Values should match the mock contract
    assert df.iloc[0]["conId"] == 345678901
    assert df.iloc[0]["symbol"] == "MCL"
    assert df.iloc[0]["secType"] == "FUT"


def test_positions_df_preserves_position_data():
    """Test that position quantity and avgCost are preserved correctly."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_single()

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    assert df.iloc[0]["account"] == "U1234567"
    assert df.iloc[0]["position"] == 2.0
    assert df.iloc[0]["avgCost"] == 5836.54


def test_positions_df_mixed_asset_types():
    """Test with futures, stocks, and options in the same account."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_mixed()

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    assert len(df) == 3

    # Verify each asset type
    sec_types = df["secType"].tolist()
    assert "FUT" in sec_types
    assert "STK" in sec_types
    assert "OPT" in sec_types

    # Verify the option has strike and right populated
    opt_row = df[df["secType"] == "OPT"].iloc[0]
    assert opt_row["strike"] == 200.0
    assert opt_row["right"] == "C"

    # Verify short position (negative quantity)
    assert opt_row["position"] == -5.0


def test_positions_df_calls_ib_with_account_id():
    """Test that the correct account ID is passed to the IB API."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = []

    tws = IbkrTws(ib=mock_ib)
    tws.positions_df("U9999999")

    mock_ib.positions.assert_called_once_with(account="U9999999")


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------


def _create_valid_positions_df():
    """Create a minimal valid positions DataFrame for schema testing."""
    return pd.DataFrame(
        {
            "account": ["U1234567"],
            "position": [2.0],
            "avgCost": [5836.54],
            "conId": [345678901],
            "symbol": ["MCL"],
            "secType": ["FUT"],
            "exchange": ["NYMEX"],
            "currency": ["USD"],
            "localSymbol": ["MCLG6"],
            "tradingClass": ["MCL"],
            "lastTradeDateOrContractMonth": ["20260219"],
            "multiplier": ["100"],
            "strike": [0.0],
            "right": [""],
        }
    )


def test_schema_validates_correct_data():
    """Test that valid positions data passes schema validation."""
    df = _create_valid_positions_df()
    validated_df = validate_ibkr_tws_positions(df)

    assert validated_df is not None
    assert len(validated_df) == 1
    assert validated_df["symbol"].iloc[0] == "MCL"


def test_schema_allows_extra_columns():
    """Test that schema allows additional columns beyond the defined ones."""
    df = _create_valid_positions_df()
    df["marketValue"] = [11673.08]

    validated_df = validate_ibkr_tws_positions(df)
    assert "marketValue" in validated_df.columns


def test_schema_rejects_missing_required_columns():
    """Test that schema rejects data when required columns are missing."""
    df = _create_valid_positions_df()
    df = df.drop(columns=["conId"])

    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_tws_positions(df)

    assert "conId" in str(exc_info.value)


def test_schema_rejects_wrong_data_types():
    """Test that schema rejects data with incorrect types."""
    df = _create_valid_positions_df()
    df["position"] = ["not_a_number"]

    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_tws_positions(df)

    assert "position" in str(exc_info.value).lower()


def test_schema_lazy_validation_multiple_errors():
    """Test that lazy validation collects multiple errors at once."""
    df = _create_valid_positions_df()
    df["position"] = ["not_a_number"]
    df["conId"] = ["not_an_integer"]

    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        validate_ibkr_tws_positions_lazy(df)

    error_message = str(exc_info.value).lower()
    assert "position" in error_message
    assert "conid" in error_message
    assert len(exc_info.value.failure_cases) >= 2


def test_schema_nullable_string_fields():
    """Test that nullable string fields accept None values."""
    df = _create_valid_positions_df()
    df["localSymbol"] = [None]
    df["tradingClass"] = [None]
    df["lastTradeDateOrContractMonth"] = [None]
    df["multiplier"] = [None]
    df["right"] = [None]
    df["exchange"] = [None]

    validated_df = validate_ibkr_tws_positions(df)
    assert validated_df is not None


def test_schema_nullable_float_fields():
    """Test that nullable float fields accept NaN values."""
    df = _create_valid_positions_df()
    df["strike"] = [float("nan")]

    validated_df = validate_ibkr_tws_positions(df)
    assert validated_df is not None


# ---------------------------------------------------------------------------
# TwsReportOutputAdapterPandas tests
# ---------------------------------------------------------------------------


def test_adapter_get_positions():
    """Test that adapter delegates to IbkrTws.positions_df()."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_single()

    tws = IbkrTws(ib=mock_ib)
    adapter = TwsReportOutputAdapterPandas(tws=tws)

    df = adapter.get_positions("U1234567")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["symbol"] == "MCL"


def test_adapter_get_positions_returns_none_for_empty():
    """Test adapter returns None when no positions exist."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = []

    tws = IbkrTws(ib=mock_ib)
    adapter = TwsReportOutputAdapterPandas(tws=tws)

    df = adapter.get_positions("U1234567")
    assert df is None


def test_adapter_put_all():
    """Test that put_all returns dict with positions key."""
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_mixed()

    tws = IbkrTws(ib=mock_ib)
    adapter = TwsReportOutputAdapterPandas(tws=tws)

    result = adapter.put_all("U1234567")

    assert "positions" in result
    assert isinstance(result["positions"], pd.DataFrame)
    assert len(result["positions"]) == 3


def test_adapter_process_accounts():
    """Test that process_accounts iterates over all managed accounts."""
    mock_ib = MagicMock()
    mock_ib.managedAccounts.return_value = ["U1111111", "U2222222"]
    mock_ib.positions.return_value = _make_positions_single()

    tws = IbkrTws(ib=mock_ib)
    adapter = TwsReportOutputAdapterPandas(tws=tws)

    results = adapter.process_accounts()

    assert len(results) == 2
    assert all("positions" in r for r in results)


# ---------------------------------------------------------------------------
# Integration: IbkrTws -> DataFrame -> Schema validation
# ---------------------------------------------------------------------------


def test_end_to_end_positions_df_passes_schema():
    """
    Integration test: IbkrTws fetches positions, expands contracts,
    and the resulting DataFrame passes Pandera schema validation.
    """
    mock_ib = MagicMock()
    mock_ib.positions.return_value = _make_positions_mixed()

    tws = IbkrTws(ib=mock_ib)
    df = tws.positions_df("U1234567")

    # Should not raise - the DataFrame should already be validated
    validated_df = validate_ibkr_tws_positions(df)
    assert len(validated_df) == 3

    # All required columns present
    for col in ["account", "position", "avgCost", "conId", "symbol", "secType", "currency"]:
        assert col in validated_df.columns
