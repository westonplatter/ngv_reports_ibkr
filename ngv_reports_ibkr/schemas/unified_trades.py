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
        "ib_execution_id": Column("object", nullable=False, coerce=False),
        # ===== CORE IDENTIFIERS =====
        "account_id": Column("object", nullable=False, coerce=False),
        "contract_id": Column("int64", nullable=False, coerce=False),
        "tws_perm_id": Column("Int64", nullable=True, coerce=False),  # TWS-only
        "flex_order_id": Column("Int64", nullable=True, coerce=False),  # Flex-only
        # ===== CONTRACT DETAILS =====
        "symbol": Column("object", nullable=False, coerce=False),
        "asset_type": Column("object", nullable=False, coerce=False),  # STK, OPT, FOP, FUT
        "currency": Column("object", nullable=False, coerce=False),
        "exchange": Column("object", nullable=False, coerce=False),
        "multiplier": Column("float64", nullable=True, coerce=False),
        "strike": Column("float64", nullable=True, coerce=False),  # Options only
        "expiry": Column("object", nullable=True, coerce=False),  # Options/Futures
        "right": Column("object", nullable=True, coerce=False),  # C/P for options
        # ===== EXECUTION DETAILS =====
        "side": Column("object", nullable=False, coerce=False),  # BUY or SELL
        "quantity": Column("float64", nullable=False, coerce=False),
        "price": Column("float64", nullable=False, coerce=False),
        "execution_time": Column("datetime64[ns, UTC]", nullable=False, coerce=False),
        "commission": Column("float64", nullable=True, coerce=False),  # Negative = cost
        "commission_currency": Column("object", nullable=True, coerce=False),
        "realized_pnl": Column("float64", nullable=True, coerce=False),
        # ===== TWS-SPECIFIC FIELDS (nullable for Flex trades) =====
        "order_type": Column("object", nullable=True, coerce=False),  # LMT, MKT, STP, etc.
        "tif": Column("object", nullable=True, coerce=False),  # DAY, GTC, etc.
        "limit_price": Column("float64", nullable=True, coerce=False),
        "aux_price": Column("float64", nullable=True, coerce=False),
        "total_quantity": Column("float64", nullable=True, coerce=False),
        "order_status": Column("object", nullable=True, coerce=False),  # Submitted, Filled, etc.
        "filled": Column("float64", nullable=True, coerce=False),
        "remaining": Column("float64", nullable=True, coerce=False),
        "avg_fill_price": Column("float64", nullable=True, coerce=False),
        # ===== FLEX-SPECIFIC FIELDS (nullable for TWS trades) =====
        "trade_id": Column("Int64", nullable=True, coerce=False),
        "transaction_id": Column("Int64", nullable=True, coerce=False),
        "trade_date": Column("object", nullable=True, coerce=False),  # Settlement date
        "trade_money": Column("float64", nullable=True, coerce=False),
        "proceeds": Column("float64", nullable=True, coerce=False),
        "net_cash": Column("float64", nullable=True, coerce=False),
        "cost": Column("float64", nullable=True, coerce=False),
        "close_price": Column("float64", nullable=True, coerce=False),
        "mtm_pnl": Column("float64", nullable=True, coerce=False),
        "cusip": Column("object", nullable=True, coerce=False),
        "isin": Column("object", nullable=True, coerce=False),
        # ===== SOURCE TRACKING =====
        "_data_source": Column("object", nullable=False, coerce=False),  # TWS or FLEX
    },
    strict=False,  # Allow additional columns
    coerce=False,  # Strict type validation, no coercion
    ordered=False,  # Column order doesn't matter
)
