"""
Pandera schema for IBKR TWS Trades.

This schema validates the structure and types of IBKR TWS trade data.
It allows additional columns to be present but requires all expected columns.
"""

from pandera.pandas import Column, DataFrameSchema

# Schema for IBKR TWS Trades
# Based on data with 173 columns and 27 rows
ibkr_tws_trades_schema = DataFrameSchema(
    columns={
        # Contract Information
        "advancedError": Column("object", nullable=True, coerce=False),
        "conId": Column("int64", nullable=False, coerce=False),
        "symbol": Column("object", nullable=False, coerce=False),
        "secType": Column("object", nullable=False, coerce=False),
        "exchange": Column("object", nullable=False, coerce=False),
        "currency": Column("object", nullable=False, coerce=False),
        "localSymbol": Column("object", nullable=False, coerce=False),
        "tradingClass": Column("object", nullable=False, coerce=False),
        "lastTradeDateOrContractMonth": Column("object", nullable=False, coerce=False),
        "multiplier": Column("object", nullable=False, coerce=False),
        "strike": Column("float64", nullable=False, coerce=False),
        "right": Column("object", nullable=False, coerce=False),
        # Account Information
        "account": Column("object", nullable=False, coerce=False),
        "action": Column("object", nullable=False, coerce=False),
        # Order Timing
        "activeStartTime": Column("object", nullable=True, coerce=False),
        "activeStopTime": Column("object", nullable=True, coerce=False),
        # Order Parameters
        "adjustableTrailingUnit": Column("int64", nullable=False, coerce=False),
        "adjustedOrderType": Column("object", nullable=True, coerce=False),
        "adjustedStopLimitPrice": Column("object", nullable=True, coerce=False),
        "adjustedStopPrice": Column("object", nullable=True, coerce=False),
        "adjustedTrailingAmount": Column("object", nullable=True, coerce=False),
        "advancedErrorOverride": Column("object", nullable=True, coerce=False),
        "algoId": Column("object", nullable=True, coerce=False),
        "algoParams": Column("object", nullable=False, coerce=False),
        "algoStrategy": Column("object", nullable=True, coerce=False),
        "allOrNone": Column("bool", nullable=False, coerce=False),
        "auctionStrategy": Column("int64", nullable=False, coerce=False),
        "autoCancelDate": Column("object", nullable=True, coerce=False),
        "autoCancelParent": Column("bool", nullable=False, coerce=False),
        "auxPrice": Column("float64", nullable=False, coerce=False),
        "basisPoints": Column("object", nullable=True, coerce=False),
        "basisPointsType": Column("object", nullable=True, coerce=False),
        "blockOrder": Column("bool", nullable=False, coerce=False),
        "cashQty": Column("float64", nullable=False, coerce=False),
        "clearingAccount": Column("object", nullable=True, coerce=False),
        "clearingIntent": Column("object", nullable=False, coerce=False),
        "clientId": Column("int64", nullable=False, coerce=False),
        "competeAgainstBestOffset": Column("object", nullable=True, coerce=False),
        "conditions": Column("object", nullable=False, coerce=False),
        "conditionsCancelOrder": Column("bool", nullable=False, coerce=False),
        "conditionsIgnoreRth": Column("bool", nullable=False, coerce=False),
        "continuousUpdate": Column("bool", nullable=False, coerce=False),
        "delta": Column("object", nullable=True, coerce=False),
        "deltaNeutralAuxPrice": Column("object", nullable=True, coerce=False),
        "deltaNeutralClearingAccount": Column("object", nullable=True, coerce=False),
        "deltaNeutralClearingIntent": Column("object", nullable=True, coerce=False),
        "deltaNeutralConId": Column("int64", nullable=False, coerce=False),
        "deltaNeutralDesignatedLocation": Column("object", nullable=True, coerce=False),
        "deltaNeutralOpenClose": Column("object", nullable=True, coerce=False),
        "deltaNeutralOrderType": Column("object", nullable=False, coerce=False),
        "deltaNeutralSettlingFirm": Column("object", nullable=True, coerce=False),
        "deltaNeutralShortSale": Column("bool", nullable=False, coerce=False),
        "deltaNeutralShortSaleSlot": Column("int64", nullable=False, coerce=False),
        "designatedLocation": Column("object", nullable=True, coerce=False),
        "discretionaryAmt": Column("float64", nullable=False, coerce=False),
        "discretionaryUpToLimitPrice": Column("bool", nullable=False, coerce=False),
        "displaySize": Column("object", nullable=True, coerce=False),
        "dontUseAutoPriceForHedge": Column("bool", nullable=False, coerce=False),
        "duration": Column("object", nullable=True, coerce=False),
        "eTradeOnly": Column("bool", nullable=False, coerce=False),
        "exemptCode": Column("int64", nullable=False, coerce=False),
        "extOperator": Column("object", nullable=True, coerce=False),
        "faGroup": Column("object", nullable=True, coerce=False),
        "faMethod": Column("object", nullable=True, coerce=False),
        "faPercentage": Column("object", nullable=True, coerce=False),
        "faProfile": Column("object", nullable=True, coerce=False),
        "filledQuantity": Column("float64", nullable=True, coerce=False),
        "firmQuoteOnly": Column("bool", nullable=False, coerce=False),
        "goodAfterTime": Column("object", nullable=True, coerce=False),
        "goodTillDate": Column("object", nullable=True, coerce=False),
        "hedgeParam": Column("object", nullable=True, coerce=False),
        "hedgeType": Column("object", nullable=True, coerce=False),
        "hidden": Column("bool", nullable=False, coerce=False),
        "imbalanceOnly": Column("bool", nullable=False, coerce=False),
        "isOmsContainer": Column("bool", nullable=False, coerce=False),
        "isPeggedChangeAmountDecrease": Column("bool", nullable=False, coerce=False),
        "lmtPrice": Column("float64", nullable=False, coerce=False),
        "lmtPriceOffset": Column("object", nullable=True, coerce=False),
        "manualOrderTime": Column("object", nullable=True, coerce=False),
        "midOffsetAtHalf": Column("object", nullable=True, coerce=False),
        "midOffsetAtWhole": Column("object", nullable=True, coerce=False),
        "mifid2DecisionAlgo": Column("object", nullable=True, coerce=False),
        "mifid2DecisionMaker": Column("object", nullable=True, coerce=False),
        "mifid2ExecutionAlgo": Column("object", nullable=True, coerce=False),
        "mifid2ExecutionTrader": Column("object", nullable=True, coerce=False),
        "minCompeteSize": Column("object", nullable=True, coerce=False),
        "minQty": Column("object", nullable=True, coerce=False),
        "minTradeQty": Column("object", nullable=True, coerce=False),
        "modelCode": Column("object", nullable=True, coerce=False),
        "nbboPriceCap": Column("object", nullable=True, coerce=False),
        "notHeld": Column("bool", nullable=False, coerce=False),
        "ocaGroup": Column("object", nullable=True, coerce=False),
        "ocaType": Column("int64", nullable=False, coerce=False),
        "openClose": Column("object", nullable=True, coerce=False),
        "optOutSmartRouting": Column("bool", nullable=False, coerce=False),
        "orderComboLegs": Column("object", nullable=False, coerce=False),
        "orderId": Column("int64", nullable=False, coerce=False),
        "orderMiscOptions": Column("object", nullable=False, coerce=False),
        "orderRef": Column("object", nullable=True, coerce=False),
        "orderType": Column("object", nullable=False, coerce=False),
        "origin": Column("int64", nullable=False, coerce=False),
        "outsideRth": Column("bool", nullable=False, coerce=False),
        "overridePercentageConstraints": Column("bool", nullable=False, coerce=False),
        "parentId": Column("int64", nullable=False, coerce=False),
        "parentPermId": Column("int64", nullable=False, coerce=False),
        "peggedChangeAmount": Column("float64", nullable=False, coerce=False),
        "percentOffset": Column("object", nullable=True, coerce=False),
        "permId": Column("int64", nullable=False, coerce=False),
        "postToAts": Column("object", nullable=True, coerce=False),
        "randomizePrice": Column("bool", nullable=False, coerce=False),
        "randomizeSize": Column("bool", nullable=False, coerce=False),
        "refFuturesConId": Column("float64", nullable=True, coerce=True),
        "referenceChangeAmount": Column("float64", nullable=False, coerce=False),
        "referenceContractId": Column("int64", nullable=False, coerce=False),
        "referenceExchangeId": Column("object", nullable=True, coerce=False),
        "referencePriceType": Column("int64", nullable=False, coerce=False),
        "routeMarketableToBbo": Column("bool", nullable=False, coerce=False),
        "rule80A": Column("object", nullable=False, coerce=False),
        "scaleAutoReset": Column("bool", nullable=False, coerce=False),
        "scaleInitFillQty": Column("object", nullable=True, coerce=False),
        "scaleInitLevelSize": Column("object", nullable=True, coerce=False),
        "scaleInitPosition": Column("object", nullable=True, coerce=False),
        "scalePriceAdjustInterval": Column("object", nullable=True, coerce=False),
        "scalePriceAdjustValue": Column("object", nullable=True, coerce=False),
        "scalePriceIncrement": Column("object", nullable=True, coerce=False),
        "scaleProfitOffset": Column("object", nullable=True, coerce=False),
        "scaleRandomPercent": Column("bool", nullable=False, coerce=False),
        "scaleSubsLevelSize": Column("object", nullable=True, coerce=False),
        "scaleTable": Column("object", nullable=True, coerce=False),
        "settlingFirm": Column("object", nullable=True, coerce=False),
        "shareholder": Column("object", nullable=False, coerce=False),
        "shortSaleSlot": Column("int64", nullable=False, coerce=False),
        "smartComboRoutingParams": Column("object", nullable=False, coerce=False),
        "softDollarTier": Column("object", nullable=False, coerce=False),
        "solicited": Column("bool", nullable=False, coerce=False),
        "startingPrice": Column("object", nullable=True, coerce=False),
        "stockRangeLower": Column("object", nullable=True, coerce=False),
        "stockRangeUpper": Column("object", nullable=True, coerce=False),
        "stockRefPrice": Column("object", nullable=True, coerce=False),
        "sweepToFill": Column("bool", nullable=False, coerce=False),
        "tif": Column("object", nullable=False, coerce=False),
        "totalQuantity": Column("float64", nullable=False, coerce=False),
        "trailStopPrice": Column("object", nullable=True, coerce=False),
        "trailingPercent": Column("object", nullable=True, coerce=False),
        "transmit": Column("bool", nullable=False, coerce=False),
        "triggerMethod": Column("int64", nullable=False, coerce=False),
        "triggerPrice": Column("object", nullable=True, coerce=False),
        "usePriceMgmtAlgo": Column("bool", nullable=False, coerce=False),
        "volatility": Column("object", nullable=True, coerce=False),
        "volatilityType": Column("int64", nullable=False, coerce=False),
        "whatIf": Column("bool", nullable=False, coerce=False),
        # Order Status
        "status": Column("object", nullable=False, coerce=False),
        "filled": Column("float64", nullable=False, coerce=False),
        "remaining": Column("float64", nullable=False, coerce=False),
        "avgFillPrice": Column("float64", nullable=False, coerce=False),
        "lastFillPrice": Column("float64", nullable=False, coerce=False),
        # Fill Information
        "fill_time_direct": Column("datetime64[ns, UTC]", nullable=True, coerce=False),
        "fill_execution_id": Column("object", nullable=True, coerce=False),
        "fill_execution_time": Column("datetime64[ns, UTC]", nullable=True, coerce=False),
        "fill_shares": Column("float64", nullable=True, coerce=False),
        "fill_price": Column("float64", nullable=True, coerce=False),
        "fill_exchange": Column("object", nullable=True, coerce=False),
        "fill_side": Column("object", nullable=True, coerce=False),
        "fill_cumQty": Column("float64", nullable=True, coerce=False),
        "fill_avgPrice": Column("float64", nullable=True, coerce=False),
        "fill_commission": Column("float64", nullable=True, coerce=False),
        "fill_commissionCurrency": Column("object", nullable=True, coerce=False),
        "fill_realizedPNL": Column("float64", nullable=True, coerce=False),
        "fill_contract_conId": Column("float64", nullable=True, coerce=False),
        # Log Information (nullable after filter_to_executions - fills and logs don't always align)
        "log_time": Column("datetime64[ns, UTC]", nullable=True, coerce=False),
        "log_status": Column("object", nullable=True, coerce=False),
        "log_message": Column("object", nullable=True, coerce=False),
        "log_errorCode": Column("float64", nullable=True, coerce=True),
    },
    strict=False,  # Allow additional columns
    coerce=False,  # Strict type validation, no coercion
    ordered=False,  # Column order doesn't matter
)


def validate_ibkr_tws_trades(df):
    """
    Validate an IBKR TWS trades DataFrame against the schema.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR TWS trade data

    Returns
    -------
    pd.DataFrame
        Validated DataFrame (returns original if validation passes)

    Raises
    ------
    pandera.errors.SchemaError
        If DataFrame doesn't match the expected schema

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv("trades.csv")
    >>> validated_df = validate_ibkr_tws_trades(df)
    """
    return ibkr_tws_trades_schema.validate(df, lazy=False)


def validate_ibkr_tws_trades_lazy(df):
    """
    Validate an IBKR TWS trades DataFrame, collecting all errors.

    This version uses lazy validation to collect all validation errors
    instead of stopping at the first error.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR TWS trade data

    Returns
    -------
    pd.DataFrame
        Validated DataFrame (returns original if validation passes)

    Raises
    ------
    pandera.errors.SchemaErrors
        If DataFrame doesn't match the expected schema (contains all errors)

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv("trades.csv")
    >>> try:
    ...     validated_df = validate_ibkr_tws_trades_lazy(df)
    ... except pa.errors.SchemaErrors as err:
    ...     print(err.failure_cases)
    """
    return ibkr_tws_trades_schema.validate(df, lazy=True)
