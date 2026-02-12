"""
Pandera schema for IBKR TWS Real-Time Positions.

This schema validates the structure and types of position data fetched from
the IBKR Trader Workstation via ib_async. It defines the core columns that
are present after expanding the ib_async Position object's contract field
into flat DataFrame columns.

This is a preliminary schema based on known ib_async Position fields.
Additional columns and constraints should be added after real-time testing
confirms the exact shape of the data.

See: notebooks/ibkr_tws_realtime.ipynb for usage examples.
"""

from pandera.pandas import Column, DataFrameSchema

# Schema for IBKR TWS Positions
# Based on ib_async Position namedtuple: (account, contract, position, avgCost)
# Contract fields are expanded via expand_contract_column()
ibkr_tws_positions_schema = DataFrameSchema(
    columns={
        # ===== ACCOUNT =====
        "account": Column("str", nullable=False, coerce=False),
        # ===== POSITION DATA =====
        "position": Column("float64", nullable=False, coerce=False),
        "avgCost": Column("float64", nullable=False, coerce=False),
        # ===== CONTRACT FIELDS (expanded from contract object) =====
        "conId": Column("int64", nullable=False, coerce=False),
        "symbol": Column("str", nullable=False, coerce=False),
        "secType": Column("str", nullable=False, coerce=False),
        "exchange": Column("str", nullable=True, coerce=False),
        "currency": Column("str", nullable=False, coerce=False),
        "localSymbol": Column("str", nullable=True, coerce=False),
        "tradingClass": Column("str", nullable=True, coerce=False),
        # ===== CONTRACT-TYPE SPECIFIC FIELDS =====
        # These fields are present for futures/options, may be empty for stocks
        "lastTradeDateOrContractMonth": Column("str", nullable=True, coerce=False),
        "multiplier": Column("str", nullable=True, coerce=False),
        "strike": Column("float64", nullable=True, coerce=False),
        "right": Column("str", nullable=True, coerce=False),
    },
    strict=False,  # Allow additional columns from real-time data
    coerce=False,  # Strict type validation, no coercion
    ordered=False,  # Column order doesn't matter
)


def validate_ibkr_tws_positions(df):
    """
    Validate an IBKR TWS positions DataFrame against the schema.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR TWS position data

    Returns
    -------
    pd.DataFrame
        Validated DataFrame (returns original if validation passes)

    Raises
    ------
    pandera.errors.SchemaError
        If DataFrame doesn't match the expected schema
    """
    return ibkr_tws_positions_schema.validate(df, lazy=False)


def validate_ibkr_tws_positions_lazy(df):
    """
    Validate an IBKR TWS positions DataFrame, collecting all errors.

    This version uses lazy validation to collect all validation errors
    instead of stopping at the first error.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing IBKR TWS position data

    Returns
    -------
    pd.DataFrame
        Validated DataFrame (returns original if validation passes)

    Raises
    ------
    pandera.errors.SchemaErrors
        If DataFrame doesn't match the expected schema (contains all errors)
    """
    return ibkr_tws_positions_schema.validate(df, lazy=True)
