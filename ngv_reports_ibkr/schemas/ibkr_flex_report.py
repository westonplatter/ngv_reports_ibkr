"""
Pandera schema for IBKR Flex Report Trades.

This schema validates the structure of IBKR flex report trade data.
It allows additional columns to be present but requires all expected columns.
"""

from pandera.pandas import Column, DataFrameSchema

# Schema for IBKR Flex Report Trades
# Based on data with 71 columns and 154 rows
ibkr_flex_report_trades_schema = DataFrameSchema(
    columns={
        # Account Information
        "accountId": Column(nullable=False),
        "acctAlias": Column(nullable=True),
        "model": Column(nullable=True),
        "currency": Column(nullable=True),
        "fxRateToBase": Column(nullable=False),
        # Asset Information
        "assetCategory": Column(nullable=True),
        "symbol": Column(nullable=True),
        "description": Column(nullable=True),
        "conid": Column("int64", nullable=False, coerce=False),
        "securityID": Column(nullable=True),
        "securityIDType": Column(nullable=True),
        "cusip": Column(nullable=True),
        "isin": Column(nullable=True),
        "listingExchange": Column(nullable=True),
        # Underlying Information
        "underlyingConid": Column(nullable=True),
        "underlyingSymbol": Column(nullable=True),
        "underlyingSecurityID": Column(nullable=True),
        "underlyingListingExchange": Column(nullable=True),
        "issuer": Column(nullable=True),
        # Contract Details
        "multiplier": Column("float64", nullable=False, coerce=True),
        "strike": Column(nullable=True),
        "expiry": Column(nullable=True),
        "tradeID": Column(nullable=False),
        "putCall": Column(nullable=True),
        "reportDate": Column(nullable=True),
        "principalAdjustFactor": Column(nullable=True),
        # Trade Timing
        "dateTime": Column("datetime64[ns, US/Eastern]", nullable=True, coerce=True),
        "tradeDate": Column(nullable=True),
        "settleDateTarget": Column(nullable=True),
        # Transaction Details
        "transactionType": Column(nullable=True),
        "exchange": Column(nullable=True),
        "quantity": Column("float64", nullable=False, coerce=True),
        "tradePrice": Column("float64", nullable=False, coerce=True),
        "tradeMoney": Column("float64", nullable=False, coerce=True),
        "proceeds": Column("float64", nullable=False, coerce=True),
        "taxes": Column("int64", nullable=False, coerce=False),
        # Commission and Costs
        "ibCommission": Column(nullable=False),
        "ibCommissionCurrency": Column(nullable=True),
        "netCash": Column(nullable=False),
        "closePrice": Column(nullable=False),
        "openCloseIndicator": Column(nullable=True),
        "notes": Column(nullable=True),
        "cost": Column(nullable=False),
        # P&L Information
        "fifoPnlRealized": Column("float64", nullable=False, coerce=True),
        "mtmPnl": Column("float64", nullable=False, coerce=True),
        # Original Trade Information
        "origTradePrice": Column(nullable=False),
        "origTradeDate": Column(nullable=True),
        "origTradeID": Column(nullable=True),
        "origOrderID": Column(nullable=False),
        "clearingFirmID": Column(nullable=True),
        # Transaction IDs
        "transactionID": Column(nullable=False),
        "buySell": Column(nullable=True),
        "ibOrderID": Column(nullable=False),
        "ibExecID": Column(nullable=True),
        "brokerageOrderID": Column(nullable=True),
        "orderReference": Column(nullable=True),
        "volatilityOrderLink": Column(nullable=True),
        "exchOrderId": Column(nullable=True),
        "extExecID": Column(nullable=True),
        # Order Timing - orderTime has 7.1% nulls according to documentation
        "orderTime": Column("datetime64[ns, US/Eastern]", nullable=True, coerce=True),
        "openDateTime": Column(nullable=True),
        "holdingPeriodDateTime": Column(nullable=True),
        "whenRealized": Column(nullable=True),
        "whenReopened": Column(nullable=True),
        # Order Details
        "levelOfDetail": Column(nullable=True),
        "changeInPrice": Column(nullable=False),
        "changeInQuantity": Column(nullable=False),
        "orderType": Column(nullable=True),
        "traderID": Column(nullable=True),
        "isAPIOrder": Column(nullable=True),
        "accruedInt": Column(nullable=False),
    },
    strict=False,  # Allow additional columns
    coerce=False,  # No DataFrame-level coercion; date columns coerce at column-level
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
