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
        "advancedError": Column("object", nullable=True, coerce=True),
        "conId": Column("int64", nullable=False, coerce=False),
        "symbol": Column("object", nullable=False, coerce=True),
        "secType": Column("object", nullable=False, coerce=True),
        "exchange": Column("object", nullable=False, coerce=True),
        "currency": Column("object", nullable=False, coerce=True),
        "localSymbol": Column("object", nullable=False, coerce=True),
        "tradingClass": Column("object", nullable=False, coerce=True),
        "lastTradeDateOrContractMonth": Column("object", nullable=False, coerce=True),
        "multiplier": Column("object", nullable=False, coerce=True),
        "strike": Column("float64", nullable=False, coerce=False),
        "right": Column("object", nullable=False, coerce=True),
        # Account Information
        "account": Column("object", nullable=False, coerce=True),
        "action": Column("object", nullable=False, coerce=True),
        # Order Timing
        "activeStartTime": Column("object", nullable=True, coerce=True),
        "activeStopTime": Column("object", nullable=True, coerce=True),
        # Order Parameters
        "adjustableTrailingUnit": Column("int64", nullable=False, coerce=False),
        "adjustedOrderType": Column("object", nullable=True, coerce=True),
        "adjustedStopLimitPrice": Column("object", nullable=True, coerce=True),
        "adjustedStopPrice": Column("object", nullable=True, coerce=True),
        "adjustedTrailingAmount": Column("object", nullable=True, coerce=True),
        "advancedErrorOverride": Column("object", nullable=True, coerce=True),
        "algoId": Column("object", nullable=True, coerce=True),
        "algoParams": Column("object", nullable=False, coerce=True),
        "algoStrategy": Column("object", nullable=True, coerce=True),
        "allOrNone": Column("bool", nullable=False, coerce=False),
        "auctionStrategy": Column("int64", nullable=False, coerce=False),
        "autoCancelDate": Column("object", nullable=True, coerce=True),
        "autoCancelParent": Column("bool", nullable=False, coerce=False),
        "auxPrice": Column("float64", nullable=False, coerce=False),
        "basisPoints": Column("object", nullable=True, coerce=True),
        "basisPointsType": Column("object", nullable=True, coerce=True),
        "blockOrder": Column("bool", nullable=False, coerce=False),
        "cashQty": Column("float64", nullable=False, coerce=False),
        "clearingAccount": Column("object", nullable=True, coerce=True),
        "clearingIntent": Column("object", nullable=False, coerce=True),
        "clientId": Column("int64", nullable=False, coerce=False),
        "competeAgainstBestOffset": Column("object", nullable=True, coerce=True),
        "conditions": Column("object", nullable=False, coerce=True),
        "conditionsCancelOrder": Column("bool", nullable=False, coerce=False),
        "conditionsIgnoreRth": Column("bool", nullable=False, coerce=False),
        "continuousUpdate": Column("bool", nullable=False, coerce=False),
        "delta": Column("object", nullable=True, coerce=True),
        "deltaNeutralAuxPrice": Column("object", nullable=True, coerce=True),
        "deltaNeutralClearingAccount": Column("object", nullable=True, coerce=True),
        "deltaNeutralClearingIntent": Column("object", nullable=True, coerce=True),
        "deltaNeutralConId": Column("int64", nullable=False, coerce=False),
        "deltaNeutralDesignatedLocation": Column("object", nullable=True, coerce=True),
        "deltaNeutralOpenClose": Column("object", nullable=True, coerce=True),
        "deltaNeutralOrderType": Column("object", nullable=False, coerce=True),
        "deltaNeutralSettlingFirm": Column("object", nullable=True, coerce=True),
        "deltaNeutralShortSale": Column("bool", nullable=False, coerce=False),
        "deltaNeutralShortSaleSlot": Column("int64", nullable=False, coerce=False),
        "designatedLocation": Column("object", nullable=True, coerce=True),
        "discretionaryAmt": Column("float64", nullable=False, coerce=False),
        "discretionaryUpToLimitPrice": Column("bool", nullable=False, coerce=False),
        "displaySize": Column("object", nullable=True, coerce=True),
        "dontUseAutoPriceForHedge": Column("bool", nullable=False, coerce=False),
        "duration": Column("object", nullable=True, coerce=True),
        "eTradeOnly": Column("bool", nullable=False, coerce=False),
        "exemptCode": Column("int64", nullable=False, coerce=False),
        "extOperator": Column("object", nullable=True, coerce=True),
        "faGroup": Column("object", nullable=True, coerce=True),
        "faMethod": Column("object", nullable=True, coerce=True),
        "faPercentage": Column("object", nullable=True, coerce=True),
        "faProfile": Column("object", nullable=True, coerce=True),
        "filledQuantity": Column("float64", nullable=True, coerce=False),
        "firmQuoteOnly": Column("bool", nullable=False, coerce=False),
        "goodAfterTime": Column("object", nullable=True, coerce=True),
        "goodTillDate": Column("object", nullable=True, coerce=True),
        "hedgeParam": Column("object", nullable=True, coerce=True),
        "hedgeType": Column("object", nullable=True, coerce=True),
        "hidden": Column("bool", nullable=False, coerce=False),
        "imbalanceOnly": Column("bool", nullable=False, coerce=False),
        "isOmsContainer": Column("bool", nullable=False, coerce=False),
        "isPeggedChangeAmountDecrease": Column("bool", nullable=False, coerce=False),
        "lmtPrice": Column("float64", nullable=False, coerce=False),
        "lmtPriceOffset": Column("object", nullable=True, coerce=True),
        "manualOrderTime": Column("object", nullable=True, coerce=True),
        "midOffsetAtHalf": Column("object", nullable=True, coerce=True),
        "midOffsetAtWhole": Column("object", nullable=True, coerce=True),
        "mifid2DecisionAlgo": Column("object", nullable=True, coerce=True),
        "mifid2DecisionMaker": Column("object", nullable=True, coerce=True),
        "mifid2ExecutionAlgo": Column("object", nullable=True, coerce=True),
        "mifid2ExecutionTrader": Column("object", nullable=True, coerce=True),
        "minCompeteSize": Column("object", nullable=True, coerce=True),
        "minQty": Column("object", nullable=True, coerce=True),
        "minTradeQty": Column("object", nullable=True, coerce=True),
        "modelCode": Column("object", nullable=True, coerce=True),
        "nbboPriceCap": Column("object", nullable=True, coerce=True),
        "notHeld": Column("bool", nullable=False, coerce=False),
        "ocaGroup": Column("object", nullable=True, coerce=True),
        "ocaType": Column("int64", nullable=False, coerce=False),
        "openClose": Column("object", nullable=True, coerce=True),
        "optOutSmartRouting": Column("bool", nullable=False, coerce=False),
        "orderComboLegs": Column("object", nullable=False, coerce=True),
        "orderId": Column("int64", nullable=False, coerce=False),
        "orderMiscOptions": Column("object", nullable=False, coerce=True),
        "orderRef": Column("object", nullable=True, coerce=True),
        "orderType": Column("object", nullable=False, coerce=True),
        "origin": Column("int64", nullable=False, coerce=False),
        "outsideRth": Column("bool", nullable=False, coerce=False),
        "overridePercentageConstraints": Column("bool", nullable=False, coerce=False),
        "parentId": Column("int64", nullable=False, coerce=False),
        "parentPermId": Column("int64", nullable=False, coerce=False),
        "peggedChangeAmount": Column("float64", nullable=False, coerce=False),
        "percentOffset": Column("object", nullable=True, coerce=True),
        "permId": Column("int64", nullable=False, coerce=False),
        "postToAts": Column("object", nullable=True, coerce=True),
        "randomizePrice": Column("bool", nullable=False, coerce=False),
        "randomizeSize": Column("bool", nullable=False, coerce=False),
        "refFuturesConId": Column("float64", nullable=True, coerce=True),
        "referenceChangeAmount": Column("float64", nullable=False, coerce=False),
        "referenceContractId": Column("int64", nullable=False, coerce=False),
        "referenceExchangeId": Column("object", nullable=True, coerce=True),
        "referencePriceType": Column("int64", nullable=False, coerce=False),
        "routeMarketableToBbo": Column("bool", nullable=False, coerce=False),
        "rule80A": Column("object", nullable=False, coerce=True),
        "scaleAutoReset": Column("bool", nullable=False, coerce=False),
        "scaleInitFillQty": Column("object", nullable=True, coerce=True),
        "scaleInitLevelSize": Column("object", nullable=True, coerce=True),
        "scaleInitPosition": Column("object", nullable=True, coerce=True),
        "scalePriceAdjustInterval": Column("object", nullable=True, coerce=True),
        "scalePriceAdjustValue": Column("object", nullable=True, coerce=True),
        "scalePriceIncrement": Column("object", nullable=True, coerce=True),
        "scaleProfitOffset": Column("object", nullable=True, coerce=True),
        "scaleRandomPercent": Column("bool", nullable=False, coerce=False),
        "scaleSubsLevelSize": Column("object", nullable=True, coerce=True),
        "scaleTable": Column("object", nullable=True, coerce=True),
        "settlingFirm": Column("object", nullable=True, coerce=True),
        "shareholder": Column("object", nullable=False, coerce=True),
        "shortSaleSlot": Column("int64", nullable=False, coerce=False),
        "smartComboRoutingParams": Column("object", nullable=False, coerce=True),
        "softDollarTier": Column("object", nullable=False, coerce=True),
        "solicited": Column("bool", nullable=False, coerce=False),
        "startingPrice": Column("object", nullable=True, coerce=True),
        "stockRangeLower": Column("object", nullable=True, coerce=True),
        "stockRangeUpper": Column("object", nullable=True, coerce=True),
        "stockRefPrice": Column("object", nullable=True, coerce=True),
        "sweepToFill": Column("bool", nullable=False, coerce=False),
        "tif": Column("object", nullable=False, coerce=True),
        "totalQuantity": Column("float64", nullable=False, coerce=False),
        "trailStopPrice": Column("object", nullable=True, coerce=True),
        "trailingPercent": Column("object", nullable=True, coerce=True),
        "transmit": Column("bool", nullable=False, coerce=False),
        "triggerMethod": Column("int64", nullable=False, coerce=False),
        "triggerPrice": Column("object", nullable=True, coerce=True),
        "usePriceMgmtAlgo": Column("bool", nullable=False, coerce=False),
        "volatility": Column("object", nullable=True, coerce=True),
        "volatilityType": Column("int64", nullable=False, coerce=False),
        "whatIf": Column("bool", nullable=False, coerce=False),
        # Order Status
        "status": Column("object", nullable=False, coerce=True),
        "filled": Column("float64", nullable=False, coerce=False),
        "remaining": Column("float64", nullable=False, coerce=False),
        "avgFillPrice": Column("float64", nullable=False, coerce=False),
        "lastFillPrice": Column("float64", nullable=False, coerce=False),
        # Fill Information
        "fill_time_direct": Column("datetime64[ns, UTC]", nullable=True, coerce=True),
        "fill_execution_id": Column("object", nullable=True, coerce=True),
        "fill_execution_time": Column("datetime64[ns, UTC]", nullable=True, coerce=True),
        "fill_shares": Column("float64", nullable=True, coerce=False),
        "fill_price": Column("float64", nullable=True, coerce=False),
        "fill_exchange": Column("object", nullable=True, coerce=True),
        "fill_side": Column("object", nullable=True, coerce=True),
        "fill_cumQty": Column("float64", nullable=True, coerce=False),
        "fill_avgPrice": Column("float64", nullable=True, coerce=False),
        "fill_commission": Column("float64", nullable=True, coerce=False),
        "fill_commissionCurrency": Column("object", nullable=True, coerce=True),
        "fill_realizedPNL": Column("float64", nullable=True, coerce=False),
        "fill_contract_conId": Column("float64", nullable=True, coerce=False),
        # Log Information (nullable after filter_to_executions - fills and logs don't always align)
        "log_time": Column("datetime64[ns, UTC]", nullable=True, coerce=True),
        "log_status": Column("object", nullable=True, coerce=True),
        "log_message": Column("object", nullable=True, coerce=True),
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
