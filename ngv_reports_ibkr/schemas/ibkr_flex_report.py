"""
Pandera schema for IBKR Flex Report Trades.

This schema validates the structure and types of IBKR flex report trade data.
It allows additional columns to be present but requires all expected columns.
"""

from pandera.pandas import Column, DataFrameSchema

# Schema for IBKR Flex Report Trades
# Based on data with 71 columns and 154 rows
ibkr_flex_report_trades_schema = DataFrameSchema(
    columns={
        # Account Information
        "accountId": Column("object", nullable=True, coerce=False),
        "acctAlias": Column("object", nullable=True, coerce=False),
        "model": Column("object", nullable=True, coerce=False),
        "currency": Column("object", nullable=True, coerce=False),
        "fxRateToBase": Column("float64", nullable=False, coerce=True),
        # Asset Information
        "assetCategory": Column("object", nullable=True, coerce=False),
        "symbol": Column("object", nullable=True, coerce=False),
        "description": Column("object", nullable=True, coerce=False),
        "conid": Column("int64", nullable=False, coerce=False),
        "securityID": Column("object", nullable=True, coerce=False),
        "securityIDType": Column("object", nullable=True, coerce=False),
        "cusip": Column("object", nullable=True, coerce=False),
        "isin": Column("object", nullable=True, coerce=False),
        "listingExchange": Column("object", nullable=True, coerce=False),
        # Underlying Information
        "underlyingConid": Column("object", nullable=True, coerce=False),
        "underlyingSymbol": Column("object", nullable=True, coerce=False),
        "underlyingSecurityID": Column("object", nullable=True, coerce=False),
        "underlyingListingExchange": Column("object", nullable=True, coerce=False),
        "issuer": Column("object", nullable=True, coerce=False),
        # Contract Details
        "multiplier": Column("float64", nullable=False, coerce=True),
        "strike": Column("object", nullable=True, coerce=False),
        "expiry": Column("object", nullable=True, coerce=False),
        "tradeID": Column("int64", nullable=False, coerce=False),
        "putCall": Column("object", nullable=True, coerce=False),
        "reportDate": Column("object", nullable=True, coerce=False),
        "principalAdjustFactor": Column("object", nullable=True, coerce=False),
        # Trade Timing
        "dateTime": Column("datetime64[ns, US/Eastern]", nullable=False, coerce=False),
        "tradeDate": Column("object", nullable=True, coerce=False),
        "settleDateTarget": Column("object", nullable=True, coerce=False),
        # Transaction Details
        "transactionType": Column("object", nullable=True, coerce=False),
        "exchange": Column("object", nullable=True, coerce=False),
        "quantity": Column("float64", nullable=False, coerce=True),
        "tradePrice": Column("float64", nullable=False, coerce=False),
        "tradeMoney": Column("float64", nullable=False, coerce=False),
        "proceeds": Column("float64", nullable=False, coerce=False),
        "taxes": Column("int64", nullable=False, coerce=False),
        # Commission and Costs
        "ibCommission": Column("float64", nullable=False, coerce=False),
        "ibCommissionCurrency": Column("object", nullable=True, coerce=False),
        "netCash": Column("float64", nullable=False, coerce=False),
        "closePrice": Column("float64", nullable=False, coerce=False),
        "openCloseIndicator": Column("object", nullable=True, coerce=False),
        "notes": Column("object", nullable=True, coerce=False),
        "cost": Column("float64", nullable=False, coerce=False),
        # P&L Information
        "fifoPnlRealized": Column("float64", nullable=False, coerce=False),
        "mtmPnl": Column("float64", nullable=False, coerce=False),
        # Original Trade Information
        "origTradePrice": Column("int64", nullable=False, coerce=False),
        "origTradeDate": Column("object", nullable=True, coerce=False),
        "origTradeID": Column("object", nullable=True, coerce=False),
        "origOrderID": Column("int64", nullable=False, coerce=False),
        "clearingFirmID": Column("object", nullable=True, coerce=False),
        # Transaction IDs
        "transactionID": Column("int64", nullable=False, coerce=False),
        "buySell": Column("object", nullable=True, coerce=False),
        "ibOrderID": Column("int64", nullable=False, coerce=False),
        "ibExecID": Column("object", nullable=True, coerce=False),
        "brokerageOrderID": Column("object", nullable=True, coerce=False),
        "orderReference": Column("object", nullable=True, coerce=False),
        "volatilityOrderLink": Column("object", nullable=True, coerce=False),
        "exchOrderId": Column("object", nullable=True, coerce=False),
        "extExecID": Column("object", nullable=True, coerce=False),
        # Order Timing - orderTime has 7.1% nulls according to documentation
        "orderTime": Column("datetime64[ns, US/Eastern]", nullable=True, coerce=False),
        "openDateTime": Column("object", nullable=True, coerce=False),
        "holdingPeriodDateTime": Column("object", nullable=True, coerce=False),
        "whenRealized": Column("object", nullable=True, coerce=False),
        "whenReopened": Column("object", nullable=True, coerce=False),
        # Order Details
        "levelOfDetail": Column("object", nullable=True, coerce=False),
        "changeInPrice": Column("int64", nullable=False, coerce=False),
        "changeInQuantity": Column("int64", nullable=False, coerce=False),
        "orderType": Column("object", nullable=True, coerce=False),
        "traderID": Column("object", nullable=True, coerce=False),
        "isAPIOrder": Column("object", nullable=True, coerce=False),
        "accruedInt": Column("int64", nullable=False, coerce=False),
    },
    strict=False,  # Allow additional columns
    coerce=False,  # Strict type validation, no coercion
    ordered=False,  # Column order doesn't matter
)


def validate_ibkr_flex_report_trades(df):
    """
    Validate an IBKR flex report trades DataFrame against the schema.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR flex report trade data

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
    >>> validated_df = validate_ibkr_flex_report_trades(df)
    """
    return ibkr_flex_report_trades_schema.validate(df, lazy=False)


def validate_ibkr_flex_report_trades_lazy(df):
    """
    Validate an IBKR flex report trades DataFrame, collecting all errors.

    This version uses lazy validation to collect all validation errors
    instead of stopping at the first error.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR flex report trade data

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
    ...     validated_df = validate_ibkr_flex_report_trades_lazy(df)
    ... except pa.errors.SchemaErrors as err:
    ...     print(err.failure_cases)
    """
    return ibkr_flex_report_trades_schema.validate(df, lazy=True)
