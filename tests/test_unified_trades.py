"""
Tests for unified_df module - TWS + Flex Report trade unification.

Covers core transformation, merging, deduplication, and validation logic.
"""

from datetime import datetime, timezone

import pandas as pd
import pytest

from ngv_reports_ibkr.schemas.unified_trades import unified_trades_schema
from ngv_reports_ibkr.unified_df import (
    create_unified_trades,
    merge_unified_trades,
    prepare_flex_trades,
    prepare_tws_trades,
    validate_unified_trades,
)

# ============================================================================
# Test Fixtures - Sample Data
# ============================================================================


@pytest.fixture
def sample_tws_df():
    """
    Sample TWS trades DataFrame (already expanded with fills/logs).

    Simulates output from:
    - expand_all_trade_columns()
    - expand_fills_and_logs()
    - Transforms.filter_to_executions()
    """
    return pd.DataFrame(
        {
            "fill_execution_id": ["0001.abcd.01.01", "0002.efgh.01.01"],
            "account": ["U1234567", "U1234567"],
            "conId": [12345, 67890],
            "permId": [1400000001, 1400000002],
            "symbol": ["AAPL", "MSFT"],
            "secType": ["STK", "STK"],
            "currency": ["USD", "USD"],
            "fill_exchange": ["SMART", "SMART"],
            "multiplier": ["1", "1"],
            "strike": [0.0, 0.0],
            "lastTradeDateOrContractMonth": ["", ""],
            "right": ["?", "?"],
            "action": ["BUY", "SELL"],
            "fill_shares": [100.0, 50.0],
            "fill_price": [150.25, 380.50],
            "fill_execution_time": [pd.Timestamp("2025-01-15 10:30:00", tz="UTC"), pd.Timestamp("2025-01-15 11:00:00", tz="UTC")],
            "fill_commission": [1.0, 0.5],
            "fill_commissionCurrency": ["USD", "USD"],
            "fill_realizedPNL": [0.0, 150.0],
            "orderType": ["LMT", "MKT"],
            "tif": ["DAY", "DAY"],
            "lmtPrice": [150.0, 0.0],
            "auxPrice": [0.0, 0.0],
            "totalQuantity": [100.0, 50.0],
            "status": ["Filled", "Filled"],
            "filled": [100.0, 50.0],
            "remaining": [0.0, 0.0],
            "avgFillPrice": [150.25, 380.50],
        }
    )


@pytest.fixture
def sample_flex_df():
    """
    Sample Flex Report trades DataFrame.

    Note: Flex uses signed quantities (negative for SELL).
    """
    return pd.DataFrame(
        {
            "ibExecID": ["0003.ijkl.01.01", "0004.mnop.01.01"],
            "accountId": ["U1234567", "U1234567"],
            "conid": [11111, 22222],
            "ibOrderID": [900000001, 900000002],
            "symbol": ["TSLA", "GOOGL"],
            "assetCategory": ["STK", "STK"],
            "currency": ["USD", "USD"],
            "exchange": ["NASDAQ", "NASDAQ"],
            "multiplier": [1.0, 1.0],
            "strike": [None, None],
            "expiry": ["", ""],
            "putCall": [None, None],
            "buySell": ["BUY", "SELL"],
            "quantity": [25.0, -10.0],  # Note: negative for SELL
            "tradePrice": [250.75, 140.25],
            "dateTime": ["2025-01-15 12:00:00", "2025-01-15 13:00:00"],
            "ibCommission": [-0.25, -0.10],
            "ibCommissionCurrency": ["USD", "USD"],
            "fifoPnlRealized": [0.0, 50.0],
            "tradeID": [100001, 100002],
            "transactionID": [200001, 200002],
            "tradeDate": ["2025-01-17", "2025-01-17"],
            "tradeMoney": [6268.75, -1402.50],
            "proceeds": [-6268.75, 1402.50],
            "netCash": [-6269.00, 1402.40],
            "cost": [6268.75, -1402.50],
            "closePrice": [250.80, 140.30],  # Optional: closing price
            "mtmPnl": [0.0, 5.0],  # Optional: mark-to-market PnL
            "cusip": [None, None],  # Optional: CUSIP identifier
            "isin": [None, None],  # Optional: ISIN identifier
        }
    )


@pytest.fixture
def sample_overlapping_exec_id():
    """
    TWS and Flex data with same execution ID (for deduplication testing).
    """
    tws = pd.DataFrame(
        {
            "fill_execution_id": ["0005.qrst.01.01"],
            "account": ["U1234567"],
            "conId": [33333],
            "permId": [1400000003],
            "symbol": ["SPY"],
            "secType": ["STK"],
            "currency": ["USD"],
            "fill_exchange": ["ARCA"],
            "multiplier": ["1"],
            "strike": [0.0],
            "lastTradeDateOrContractMonth": [""],
            "right": ["?"],
            "action": ["BUY"],
            "fill_shares": [100.0],
            "fill_price": [450.50],
            "fill_execution_time": [pd.Timestamp("2025-01-15 14:00:00", tz="UTC")],
            "fill_commission": [1.0],
            "fill_commissionCurrency": ["USD"],
            "fill_realizedPNL": [0.0],
            "orderType": ["LMT"],
            "tif": ["DAY"],
            "lmtPrice": [450.0],
            "auxPrice": [0.0],
            "totalQuantity": [100.0],
            "status": ["Filled"],
            "filled": [100.0],
            "remaining": [0.0],
            "avgFillPrice": [450.50],
        }
    )

    flex = pd.DataFrame(
        {
            "ibExecID": ["0005.qrst.01.01"],  # Same execution ID
            "accountId": ["U1234567"],
            "conid": [33333],
            "ibOrderID": [900000003],
            "symbol": ["SPY"],
            "assetCategory": ["STK"],
            "currency": ["USD"],
            "exchange": ["ARCA"],
            "multiplier": [1.0],
            "strike": [None],
            "expiry": [""],
            "putCall": [None],
            "buySell": ["BUY"],
            "quantity": [100.0],
            "tradePrice": [450.50],
            "dateTime": ["2025-01-15 14:00:00"],
            "ibCommission": [-1.0],
            "ibCommissionCurrency": ["USD"],
            "fifoPnlRealized": [0.0],
            "tradeID": [100003],
            "transactionID": [200003],
            "tradeDate": ["2025-01-17"],
            "tradeMoney": [45050.0],
            "proceeds": [-45050.0],
            "netCash": [-45051.0],
            "cost": [45050.0],
        }
    )

    return tws, flex


# ============================================================================
# Test prepare_tws_trades
# ============================================================================


def test_prepare_tws_trades_basic_mapping(sample_tws_df):
    """
    Test TWS → unified schema transformation.

    Verifies:
    - Field mapping works correctly
    - Commission standardized to negative
    - Nullable Int64 columns created properly
    - Source tag set correctly
    """
    unified = prepare_tws_trades(sample_tws_df)

    # Check schema mapping
    assert unified["ib_execution_id"].tolist() == ["0001.abcd.01.01", "0002.efgh.01.01"]
    assert unified["symbol"].tolist() == ["AAPL", "MSFT"]
    assert unified["side"].tolist() == ["BUY", "SELL"]
    assert unified["quantity"].tolist() == [100.0, 50.0]

    # Check commission standardized to negative
    assert all(unified["commission"] <= 0)

    # Check source tag
    assert all(unified["_data_source"] == "TWS")

    # Check nullable Int64 columns
    assert unified["tws_perm_id"].dtype == "Int64"
    assert unified["flex_order_id"].dtype == "Int64"
    assert pd.isna(unified["flex_order_id"]).all()


# ============================================================================
# Test prepare_flex_trades
# ============================================================================


def test_prepare_flex_trades_quantity_absolute(sample_flex_df):
    """
    Test Flex → unified schema transformation with signed quantity handling.

    Critical: Flex uses signed quantities (negative for SELL).
    Unified schema uses absolute quantities + side field.

    Verifies:
    - Negative quantities converted to absolute
    - Field mapping works correctly
    - Nullable Int64 columns created properly
    """
    unified = prepare_flex_trades(sample_flex_df)

    # Check quantity is absolute (not signed)
    assert unified["quantity"].tolist() == [25.0, 10.0]  # Both positive

    # Check side field indicates direction
    assert unified["side"].tolist() == ["BUY", "SELL"]

    # Check Flex-specific fields populated
    assert unified["trade_id"].tolist() == [100001, 100002]
    assert unified["transaction_id"].tolist() == [200001, 200002]

    # Check TWS-only fields are null
    assert pd.isna(unified["order_type"]).all()
    assert pd.isna(unified["tws_perm_id"]).all()

    # Check source tag
    assert all(unified["_data_source"] == "FLEX")


# ============================================================================
# Test merge_unified_trades
# ============================================================================


def test_merge_deduplicate_flex_first(sample_overlapping_exec_id):
    """
    Test deduplication strategy: flex_first.

    When same execution ID exists in both TWS and Flex,
    keep Flex as source of truth.
    """
    tws_df, flex_df = sample_overlapping_exec_id

    tws_unified = prepare_tws_trades(tws_df)
    flex_unified = prepare_flex_trades(flex_df)

    merged = merge_unified_trades(tws_unified=tws_unified, flex_unified=flex_unified, dedup_strategy="flex_first")

    # Should have only 1 row (deduplicated)
    assert len(merged) == 1

    # Should be from Flex (source of truth)
    assert merged["_data_source"].iloc[0] == "FLEX"

    # Should have Flex-specific fields populated
    assert not pd.isna(merged["trade_id"].iloc[0])


def test_merge_deduplicate_tws_first(sample_overlapping_exec_id):
    """
    Test deduplication strategy: tws_first.

    When same execution ID exists in both sources,
    keep TWS as source of truth.
    """
    tws_df, flex_df = sample_overlapping_exec_id

    tws_unified = prepare_tws_trades(tws_df)
    flex_unified = prepare_flex_trades(flex_df)

    merged = merge_unified_trades(tws_unified=tws_unified, flex_unified=flex_unified, dedup_strategy="tws_first")

    # Should have only 1 row (deduplicated)
    assert len(merged) == 1

    # Should be from TWS
    assert merged["_data_source"].iloc[0] == "TWS"

    # Should have TWS-specific fields populated
    assert not pd.isna(merged["order_type"].iloc[0])


def test_merge_no_duplicates(sample_tws_df, sample_flex_df):
    """
    Test merging when no overlapping execution IDs.

    Should combine all trades from both sources.
    """
    tws_unified = prepare_tws_trades(sample_tws_df)
    flex_unified = prepare_flex_trades(sample_flex_df)

    merged = merge_unified_trades(tws_unified=tws_unified, flex_unified=flex_unified, dedup_strategy="flex_first")

    # Should have all trades (2 TWS + 2 Flex = 4 total)
    assert len(merged) == 4

    # Check source distribution
    assert (merged["_data_source"] == "TWS").sum() == 2
    assert (merged["_data_source"] == "FLEX").sum() == 2

    # Check sorted by execution time
    assert merged["execution_time"].is_monotonic_increasing


# ============================================================================
# Test validate_unified_trades
# ============================================================================


def test_validate_unified_trades_valid(sample_tws_df):
    """
    Test validation passes for valid unified trades.
    """
    unified = prepare_tws_trades(sample_tws_df)

    is_valid = validate_unified_trades(unified, verbose=False)

    assert is_valid is True


def test_validate_unified_trades_invalid_side():
    """
    Test validation fails for invalid side values.
    """
    # Create invalid data with wrong side
    invalid_df = pd.DataFrame(
        {
            "ib_execution_id": ["test.001"],
            "side": ["INVALID"],  # Should be BUY or SELL
            "quantity": [100.0],
            "price": [50.0],
            "execution_time": [pd.Timestamp("2025-01-15 10:00:00", tz="UTC")],
        }
    )

    is_valid = validate_unified_trades(invalid_df, verbose=False)

    assert is_valid is False


# ============================================================================
# Test create_unified_trades (end-to-end)
# ============================================================================


def test_create_unified_trades_end_to_end(sample_tws_df, sample_flex_df):
    """
    Test complete workflow: prepare + merge + validate.

    This is the main entry point most users will call.
    """
    unified = create_unified_trades(tws_df=sample_tws_df, flex_df=sample_flex_df, dedup_strategy="flex_first", validate=True)

    # Check result
    assert len(unified) == 4
    assert all(unified["ib_execution_id"].notna())
    assert all(unified["quantity"] > 0)  # All quantities positive
    assert all(unified["side"].isin(["BUY", "SELL"]))


def test_create_unified_trades_schema_validation(sample_tws_df, sample_flex_df):
    """
    Test that created unified trades pass Pandera schema validation.
    """
    unified = create_unified_trades(
        tws_df=sample_tws_df, flex_df=sample_flex_df, dedup_strategy="flex_first", validate=False  # Skip built-in validation to test schema separately
    )

    # Should pass Pandera schema validation
    validated = unified_trades_schema.validate(unified)
    assert validated is not None
    assert len(validated) == len(unified)


# ============================================================================
# Edge Cases
# ============================================================================


def test_empty_dataframes():
    """
    Test handling of empty input DataFrames.
    """
    empty_tws = pd.DataFrame()
    empty_flex = pd.DataFrame()

    unified = create_unified_trades(tws_df=empty_tws, flex_df=empty_flex, validate=False)

    # Should return empty DataFrame with correct schema
    assert len(unified) == 0
    assert "ib_execution_id" in unified.columns


def test_only_tws_data(sample_tws_df):
    """
    Test with only TWS data (no Flex).
    """
    unified = create_unified_trades(tws_df=sample_tws_df, flex_df=None, validate=True)

    assert len(unified) == 2
    assert all(unified["_data_source"] == "TWS")


def test_only_flex_data(sample_flex_df):
    """
    Test with only Flex data (no TWS).
    """
    unified = create_unified_trades(tws_df=None, flex_df=sample_flex_df, validate=True)

    assert len(unified) == 2
    assert all(unified["_data_source"] == "FLEX")
