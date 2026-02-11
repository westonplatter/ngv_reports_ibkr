import pandas as pd
import pandera.pandas as pa
import pytest

from ngv_reports_ibkr.schemas.ibkr_flex_report import (
    ibkr_flex_report_trades_schema,
    validate_ibkr_flex_report_trades,
)


def create_valid_trade_df():
    """Create a minimal valid trade DataFrame for testing using MCL (Crude Oil futures)."""
    return pd.DataFrame(
        {
            # Account info - anonymized per prompt-ibkr-sample-data.md
            "accountId": ["U1234567"],
            "acctAlias": [""],
            "model": [""],
            "currency": ["USD"],
            "fxRateToBase": [1.0],
            # Asset info - keep real symbols/exchanges
            "assetCategory": ["FUT"],
            "symbol": ["MCLF6"],
            "description": ["MCL DEC25"],
            "conid": [345678901],  # Generic sequential ID
            "securityID": [""],
            "securityIDType": [""],
            "cusip": [""],
            "isin": [""],
            "listingExchange": ["NYMEX"],
            # Underlying info
            "underlyingConid": [""],
            "underlyingSymbol": ["MCL"],
            "underlyingSecurityID": [""],
            "underlyingListingExchange": [""],
            "issuer": [""],
            # Contract details
            "multiplier": [100.0],
            "strike": [""],
            "expiry": ["2025-12-18"],
            "tradeID": [1000000003],  # Generic trade ID range
            "putCall": [""],
            "reportDate": ["2025-01-15"],  # Generic January date
            "principalAdjustFactor": [""],
            # Trade timing - generic dates/times
            "dateTime": [pd.Timestamp("2025-01-15 10:30:00", tz="US/Eastern")],
            "tradeDate": ["2025-01-15"],
            "settleDateTarget": ["2025-01-16"],
            # Transaction details - keep realistic prices
            "transactionType": ["ExchTrade"],
            "exchange": ["NYMEX"],
            "quantity": [-1.0],
            "tradePrice": [58.55],
            "tradeMoney": [-5855.0],
            "proceeds": [5855.0],
            "taxes": [0],
            # Commission and costs
            "ibCommission": [-0.77],
            "ibCommissionCurrency": ["USD"],
            "netCash": [5854.23],
            "closePrice": [58.50],
            "openCloseIndicator": ["C"],
            "notes": [""],
            "cost": [5836.54],
            # P&L
            "fifoPnlRealized": [18.46],
            "mtmPnl": [5.0],
            # Original trade info
            "origTradePrice": [0],
            "origTradeDate": [""],
            "origTradeID": [""],
            "origOrderID": [0],
            "clearingFirmID": [""],
            # Transaction IDs - anonymized with distinct ranges
            "transactionID": [5000000003],  # Generic transaction ID range
            "buySell": ["SELL"],
            "ibOrderID": [9000000003],  # Generic order ID range
            "ibExecID": ["0000ijkl.34567890.01.01"],  # Generic hex-like format
            "brokerageOrderID": ["00aabbcc.00ddeeff.11223344.000"],
            "orderReference": [""],
            "volatilityOrderLink": [""],
            "exchOrderId": ["N/A"],
            "extExecID": ["GHI789RST000003"],  # Generic alphanumeric
            # Order timing
            "orderTime": [pd.Timestamp("2025-01-15 10:30:00", tz="US/Eastern")],
            "openDateTime": [""],
            "holdingPeriodDateTime": [""],
            "whenRealized": [""],
            "whenReopened": [""],
            # Order details
            "levelOfDetail": ["EXECUTION"],
            "changeInPrice": [0],
            "changeInQuantity": [0],
            "orderType": ["LMT"],
            "traderID": [""],
            "isAPIOrder": ["N"],
            "accruedInt": [0],
        }
    )


def test_validate_correct_trade_data():
    """Test that valid trade data passes validation."""
    df = create_valid_trade_df()
    validated_df = validate_ibkr_flex_report_trades(df)

    # Validation should return the same DataFrame
    assert validated_df is not None
    assert len(validated_df) == 1
    assert validated_df["symbol"].iloc[0] == "MCLF6"
    assert validated_df["quantity"].iloc[0] == -1.0  # Short position


def test_schema_allows_extra_columns():
    """Test that schema allows additional columns beyond the required ones."""
    df = create_valid_trade_df()
    # Add an extra column that's not in the schema
    df["customColumn"] = ["extra_data"]

    # Should not raise an error
    validated_df = validate_ibkr_flex_report_trades(df)
    assert "customColumn" in validated_df.columns
    assert validated_df["customColumn"].iloc[0] == "extra_data"


def test_schema_rejects_missing_required_columns():
    """Test that schema rejects data when required columns are missing."""
    df = create_valid_trade_df()
    # Remove a required column
    df = df.drop(columns=["quantity"])

    # Should raise SchemaError
    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_flex_report_trades(df)

    assert "quantity" in str(exc_info.value).lower()


def test_schema_rejects_wrong_data_types():
    """Test that schema rejects data with incorrect types."""
    df = create_valid_trade_df()
    # Change quantity from float to string
    df["quantity"] = ["not_a_number"]

    # Should raise SchemaError
    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_flex_report_trades(df)

    assert "quantity" in str(exc_info.value).lower()


def test_schema_lazy_validation_multiple_errors():
    """Test that lazy validation collects multiple errors at once."""
    from ngv_reports_ibkr.schemas.ibkr_flex_report import (
        validate_ibkr_flex_report_trades_lazy,
    )

    df = create_valid_trade_df()

    # Introduce two different type errors
    df["quantity"] = ["not_a_number"]  # Should be float64
    df["conid"] = ["not_an_integer"]  # Should be int64

    # Should raise SchemaErrors (plural) with lazy validation
    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        validate_ibkr_flex_report_trades_lazy(df)

    error_message = str(exc_info.value).lower()

    # Both column names should appear in the error message
    assert "quantity" in error_message, "Expected 'quantity' column error in lazy validation"
    assert "conid" in error_message, "Expected 'conid' column error in lazy validation"

    # Verify we have 2 errors collected
    assert len(exc_info.value.failure_cases) >= 2, f"Expected at least 2 failure cases, got {len(exc_info.value.failure_cases)}"


def test_multiplier_coercion_int_to_float():
    """Test that multiplier is coerced from int64 to float64."""
    df = create_valid_trade_df()
    # Set multiplier as int64 (equity contracts typically have multiplier=1)
    df["multiplier"] = [1]  # int64

    # Should coerce to float64 without raising error
    validated_df = validate_ibkr_flex_report_trades(df)

    assert validated_df["multiplier"].dtype == "float64"
    assert validated_df["multiplier"].iloc[0] == 1.0


def test_multiplier_coercion_decimal_options():
    """Test that decimal multipliers (options) are handled correctly."""
    df = create_valid_trade_df()
    # Set multiplier as decimal (options contracts use 0.01 multiplier)
    df["multiplier"] = [0.01]  # float64

    validated_df = validate_ibkr_flex_report_trades(df)

    assert validated_df["multiplier"].dtype == "float64"
    assert validated_df["multiplier"].iloc[0] == 0.01
