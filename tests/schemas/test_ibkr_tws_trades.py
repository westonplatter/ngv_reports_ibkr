import pandas as pd
import pandera.pandas as pa
import pytest

from ngv_reports_ibkr.schemas.ibkr_tws_trades import (
    ibkr_tws_trades_schema,
    validate_ibkr_tws_trades,
    validate_ibkr_tws_trades_lazy,
)


def create_valid_tws_trade_df():
    """Create a minimal valid TWS trade DataFrame for testing."""
    return pd.DataFrame(
        {
            # Contract Information
            "advancedError": [""],
            "conId": [345678901],
            "symbol": ["MCLF6"],
            "secType": ["FUT"],
            "exchange": ["NYMEX"],
            "currency": ["USD"],
            "localSymbol": ["MCLF6"],
            "tradingClass": ["MCL"],
            "lastTradeDateOrContractMonth": ["20251218"],
            "multiplier": ["100"],
            "strike": [0.0],
            "right": [""],
            # Account Information
            "account": ["U1234567"],
            "action": ["SELL"],
            # Order Timing
            "activeStartTime": [""],
            "activeStopTime": [""],
            # Order Parameters
            "adjustableTrailingUnit": [0],
            "adjustedOrderType": [""],
            "adjustedStopLimitPrice": [""],
            "adjustedStopPrice": [""],
            "adjustedTrailingAmount": [""],
            "advancedErrorOverride": [""],
            "algoId": [""],
            "algoParams": ["[]"],
            "algoStrategy": [""],
            "allOrNone": [False],
            "auctionStrategy": [0],
            "autoCancelDate": [""],
            "autoCancelParent": [False],
            "auxPrice": [0.0],
            "basisPoints": [""],
            "basisPointsType": [""],
            "blockOrder": [False],
            "cashQty": [0.0],
            "clearingAccount": [""],
            "clearingIntent": ["IB"],
            "clientId": [1],
            "competeAgainstBestOffset": [""],
            "conditions": ["[]"],
            "conditionsCancelOrder": [False],
            "conditionsIgnoreRth": [False],
            "continuousUpdate": [False],
            "delta": [""],
            "deltaNeutralAuxPrice": [""],
            "deltaNeutralClearingAccount": [""],
            "deltaNeutralClearingIntent": [""],
            "deltaNeutralConId": [0],
            "deltaNeutralDesignatedLocation": [""],
            "deltaNeutralOpenClose": [""],
            "deltaNeutralOrderType": ["None"],
            "deltaNeutralSettlingFirm": [""],
            "deltaNeutralShortSale": [False],
            "deltaNeutralShortSaleSlot": [0],
            "designatedLocation": [""],
            "discretionaryAmt": [0.0],
            "discretionaryUpToLimitPrice": [False],
            "displaySize": [""],
            "dontUseAutoPriceForHedge": [False],
            "duration": [""],
            "eTradeOnly": [False],
            "exemptCode": [-1],
            "extOperator": [""],
            "faGroup": [""],
            "faMethod": [""],
            "faPercentage": [""],
            "faProfile": [""],
            "filledQuantity": [1.0],
            "firmQuoteOnly": [False],
            "goodAfterTime": [""],
            "goodTillDate": [""],
            "hedgeParam": [""],
            "hedgeType": [""],
            "hidden": [False],
            "imbalanceOnly": [False],
            "isOmsContainer": [False],
            "isPeggedChangeAmountDecrease": [False],
            "lmtPrice": [58.55],
            "lmtPriceOffset": [""],
            "manualOrderTime": [""],
            "midOffsetAtHalf": [""],
            "midOffsetAtWhole": [""],
            "mifid2DecisionAlgo": [""],
            "mifid2DecisionMaker": [""],
            "mifid2ExecutionAlgo": [""],
            "mifid2ExecutionTrader": [""],
            "minCompeteSize": [""],
            "minQty": [""],
            "minTradeQty": [""],
            "modelCode": [""],
            "nbboPriceCap": [""],
            "notHeld": [False],
            "ocaGroup": [""],
            "ocaType": [0],
            "openClose": [""],
            "optOutSmartRouting": [False],
            "orderComboLegs": ["[]"],
            "orderId": [100],
            "orderMiscOptions": ["[]"],
            "orderRef": [""],
            "orderType": ["LMT"],
            "origin": [0],
            "outsideRth": [False],
            "overridePercentageConstraints": [False],
            "parentId": [0],
            "parentPermId": [0],
            "peggedChangeAmount": [0.0],
            "percentOffset": [""],
            "permId": [987654321],
            "postToAts": [""],
            "randomizePrice": [False],
            "randomizeSize": [False],
            "refFuturesConId": [None],
            "referenceChangeAmount": [0.0],
            "referenceContractId": [0],
            "referenceExchangeId": [""],
            "referencePriceType": [0],
            "routeMarketableToBbo": [False],
            "rule80A": [""],
            "scaleAutoReset": [False],
            "scaleInitFillQty": [""],
            "scaleInitLevelSize": [""],
            "scaleInitPosition": [""],
            "scalePriceAdjustInterval": [""],
            "scalePriceAdjustValue": [""],
            "scalePriceIncrement": [""],
            "scaleProfitOffset": [""],
            "scaleRandomPercent": [False],
            "scaleSubsLevelSize": [""],
            "scaleTable": [""],
            "settlingFirm": [""],
            "shareholder": [""],
            "shortSaleSlot": [0],
            "smartComboRoutingParams": ["[]"],
            "softDollarTier": ["SoftDollarTier(name='', value='', displayName='')"],
            "solicited": [False],
            "startingPrice": [""],
            "stockRangeLower": [""],
            "stockRangeUpper": [""],
            "stockRefPrice": [""],
            "sweepToFill": [False],
            "tif": ["DAY"],
            "totalQuantity": [1.0],
            "trailStopPrice": [""],
            "trailingPercent": [""],
            "transmit": [True],
            "triggerMethod": [0],
            "triggerPrice": [""],
            "usePriceMgmtAlgo": [False],
            "volatility": [""],
            "volatilityType": [0],
            "whatIf": [False],
            # Order Status
            "status": ["Filled"],
            "filled": [1.0],
            "remaining": [0.0],
            "avgFillPrice": [58.55],
            "lastFillPrice": [58.55],
            # Fill Information
            "fill_time_direct": [pd.Timestamp("2025-01-15 15:30:00", tz="UTC")],
            "fill_execution_id": ["0000ijkl.34567890.01.01"],
            "fill_execution_time": [pd.Timestamp("2025-01-15 15:30:00", tz="UTC")],
            "fill_shares": [1.0],
            "fill_price": [58.55],
            "fill_exchange": ["NYMEX"],
            "fill_side": ["SLD"],
            "fill_cumQty": [1.0],
            "fill_avgPrice": [58.55],
            "fill_commission": [0.77],
            "fill_commissionCurrency": ["USD"],
            "fill_realizedPNL": [18.46],
            "fill_contract_conId": [345678901.0],
            # Log Information
            "log_time": [pd.Timestamp("2025-01-15 15:30:00", tz="UTC")],
            "log_status": ["Filled"],
            "log_message": [""],
            "log_errorCode": [None],
        }
    )


def test_validate_correct_tws_trade_data():
    """Test that valid TWS trade data passes validation."""
    df = create_valid_tws_trade_df()
    validated_df = validate_ibkr_tws_trades(df)

    # Validation should return the same DataFrame
    assert validated_df is not None
    assert len(validated_df) == 1
    assert validated_df["symbol"].iloc[0] == "MCLF6"
    assert validated_df["totalQuantity"].iloc[0] == 1.0


def test_tws_schema_allows_extra_columns():
    """Test that schema allows additional columns beyond the required ones."""
    df = create_valid_tws_trade_df()
    # Add an extra column that's not in the schema
    df["customColumn"] = ["extra_data"]

    # Should not raise an error
    validated_df = validate_ibkr_tws_trades(df)
    assert "customColumn" in validated_df.columns
    assert validated_df["customColumn"].iloc[0] == "extra_data"


def test_tws_schema_rejects_missing_required_columns():
    """Test that schema rejects data when required columns are missing."""
    df = create_valid_tws_trade_df()
    # Remove a required column
    df = df.drop(columns=["symbol"])

    # Should raise SchemaError
    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_tws_trades(df)

    assert "symbol" in str(exc_info.value).lower()


def test_tws_schema_rejects_wrong_data_types():
    """Test that schema rejects data with incorrect types."""
    df = create_valid_tws_trade_df()
    # Change conId from int64 to string
    df["conId"] = ["not_a_number"]

    # Should raise SchemaError
    with pytest.raises(pa.errors.SchemaError) as exc_info:
        validate_ibkr_tws_trades(df)

    assert "conid" in str(exc_info.value).lower()


def test_tws_schema_lazy_validation_multiple_errors():
    """Test that lazy validation collects multiple errors at once."""
    df = create_valid_tws_trade_df()

    # Introduce two different type errors
    df["conId"] = ["not_an_integer"]  # Should be int64
    df["totalQuantity"] = ["not_a_float"]  # Should be float64

    # Should raise SchemaErrors (plural) with lazy validation
    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        validate_ibkr_tws_trades_lazy(df)

    error_message = str(exc_info.value).lower()

    # Both column names should appear in the error message
    assert "conid" in error_message, "Expected 'conId' column error in lazy validation"
    assert "totalquantity" in error_message, "Expected 'totalQuantity' column error in lazy validation"

    # Verify we have 2 errors collected
    assert len(exc_info.value.failure_cases) >= 2, f"Expected at least 2 failure cases, got {len(exc_info.value.failure_cases)}"


def test_tws_schema_validates_datetime_columns():
    """Test that datetime columns with timezone are validated correctly."""
    df = create_valid_tws_trade_df()
    validated_df = validate_ibkr_tws_trades(df)

    # Check that UTC timezone is preserved
    assert validated_df["fill_time_direct"].iloc[0].tzinfo is not None
    assert validated_df["fill_execution_time"].iloc[0].tzinfo is not None
    assert validated_df["log_time"].iloc[0].tzinfo is not None


def test_tws_schema_handles_nullable_fill_columns():
    """Test that nullable fill columns allow NaN values while preserving dtype."""
    import numpy as np

    df = create_valid_tws_trade_df()

    # Set nullable fill columns to NaN while preserving float64 dtype
    df["fill_shares"] = pd.Series([np.nan], dtype="float64")
    df["fill_price"] = pd.Series([np.nan], dtype="float64")
    df["fill_commission"] = pd.Series([np.nan], dtype="float64")
    df["filledQuantity"] = pd.Series([np.nan], dtype="float64")

    # Should not raise an error since these columns are nullable
    validated_df = validate_ibkr_tws_trades(df)
    assert validated_df is not None
    assert pd.isna(validated_df["fill_shares"].iloc[0])
