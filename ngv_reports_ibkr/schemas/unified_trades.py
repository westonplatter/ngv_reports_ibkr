"""
Pandera schema for Unified Trades DataFrame.

This schema validates the unified trades structure that combines IBKR TWS realtime
trades with Flex Report trades. The schema includes fields from both sources, with
some fields being nullable depending on the data source.

See: data/unified_trades.md for specification.
"""

from pandera.pandas import Column, DataFrameSchema

# Schema for Unified Trades
unified_trades_schema = DataFrameSchema(
    columns={
        # ===== PRIMARY KEY =====
        "ib_execution_id": Column("object", nullable=False, coerce=True),
        # ===== CORE IDENTIFIERS =====
        "account_id": Column("object", nullable=False, coerce=True),
        "contract_id": Column("int64", nullable=False, coerce=False),
        "tws_perm_id": Column("Int64", nullable=True, coerce=False),  # TWS-only
        "flex_order_id": Column("Int64", nullable=True, coerce=False),  # Flex-only
        # ===== CONTRACT DETAILS =====
        "symbol": Column("object", nullable=False, coerce=True),
        "asset_type": Column("object", nullable=False, coerce=True),  # STK, OPT, FOP, FUT
        "currency": Column("object", nullable=False, coerce=True),
        "exchange": Column("object", nullable=False, coerce=True),
        "multiplier": Column("float64", nullable=True, coerce=True),
        "strike": Column("float64", nullable=True, coerce=True),  # Options only
        "expiry": Column("object", nullable=True, coerce=True),  # Options/Futures
        "right": Column("object", nullable=True, coerce=True),  # C/P for options
        # ===== EXECUTION DETAILS =====
        "side": Column("object", nullable=False, coerce=True),  # BUY or SELL
        "quantity": Column("float64", nullable=False, coerce=False),
        "price": Column("float64", nullable=False, coerce=False),
        "execution_time": Column("datetime64[ns, UTC]", nullable=False, coerce=True),
        "commission": Column("float64", nullable=True, coerce=True),  # Negative = cost
        "commission_currency": Column("object", nullable=True, coerce=True),
        "realized_pnl": Column("float64", nullable=True, coerce=True),
        # ===== TWS-SPECIFIC FIELDS (nullable for Flex trades) =====
        "order_type": Column("object", nullable=True, coerce=True),  # LMT, MKT, STP, etc.
        "tif": Column("object", nullable=True, coerce=True),  # DAY, GTC, etc.
        "limit_price": Column("float64", nullable=True, coerce=True),
        "aux_price": Column("float64", nullable=True, coerce=True),
        "total_quantity": Column("float64", nullable=True, coerce=True),
        "order_status": Column("object", nullable=True, coerce=True),  # Submitted, Filled, etc.
        "filled": Column("float64", nullable=True, coerce=True),
        "remaining": Column("float64", nullable=True, coerce=True),
        "avg_fill_price": Column("float64", nullable=True, coerce=True),
        # ===== FLEX-SPECIFIC FIELDS (nullable for TWS trades) =====
        "trade_id": Column("Int64", nullable=True, coerce=False),
        "transaction_id": Column("Int64", nullable=True, coerce=False),
        "trade_date": Column("object", nullable=True, coerce=True),  # Settlement date
        "trade_money": Column("float64", nullable=True, coerce=True),
        "proceeds": Column("float64", nullable=True, coerce=True),
        "net_cash": Column("float64", nullable=True, coerce=True),
        "cost": Column("float64", nullable=True, coerce=True),
        "close_price": Column("float64", nullable=True, coerce=True),
        "mtm_pnl": Column("float64", nullable=True, coerce=True),
        "cusip": Column("object", nullable=True, coerce=True),
        "isin": Column("object", nullable=True, coerce=True),
        # ===== SOURCE TRACKING =====
        "_data_source": Column("object", nullable=False, coerce=True),  # TWS or FLEX
    },
    strict=False,  # Allow additional columns
    coerce=False,  # Strict type validation, no coercion
    ordered=False,  # Column order doesn't matter
)
