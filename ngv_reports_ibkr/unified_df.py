"""
Unified Trades DataFrame: Merge TWS realtime trades with Flex Report trades.

This module provides functions to create a single unified trades DataFrame from both
IBKR TWS realtime API trades and Flex Report trades, using execution ID as the primary
key for deduplication.

See: data/unified_trades.md for complete specification.
"""

import warnings
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd


def prepare_tws_trades(tws_df: pd.DataFrame, source_tag: str = "TWS") -> pd.DataFrame:
    """
    Transform TWS realtime trades DataFrame to unified schema.

    Expects input DataFrame to already be processed with:
    - expand_all_trade_columns(tws_df)
    - expand_fills_and_logs(tws_df, fills_col="fills", log_col="log")
    - Transforms.filter_to_executions(tws_df)

    Args:
        tws_df: TWS trades DataFrame with expanded contract/order/fills columns
        source_tag: Tag to identify data source (default: "TWS")

    Returns:
        DataFrame in unified schema

    Raises:
        KeyError: If required columns are missing
        ValueError: If schema validation fails
    """
    # F2: Check required columns exist
    required_cols = [
        "fill_execution_id",
        "account",
        "conId",
        "permId",
        "symbol",
        "secType",
        "currency",
        "fill_exchange",
        "multiplier",
        "strike",
        "lastTradeDateOrContractMonth",
        "right",
        "action",
        "fill_shares",
        "fill_price",
        "fill_execution_time",
        "fill_commission",
        "fill_commissionCurrency",
        "fill_realizedPNL",
    ]
    missing = [col for col in required_cols if col not in tws_df.columns]
    if missing:
        raise KeyError(f"Missing required columns in TWS DataFrame: {missing}")

    # F5: Validate timezone awareness
    if not isinstance(tws_df["fill_execution_time"].dtype, pd.DatetimeTZDtype):
        warnings.warn("fill_execution_time is not timezone-aware. Converting to UTC.", UserWarning)

    unified = pd.DataFrame(
        {
            # Primary key
            "ib_execution_id": tws_df["fill_execution_id"],
            # Core identifiers
            "account_id": tws_df["account"],
            "contract_id": tws_df["conId"],
            "tws_perm_id": tws_df["permId"],
            "flex_order_id": None,  # TWS doesn't have Flex order IDs
            # Contract details
            "symbol": tws_df["symbol"],
            "asset_type": tws_df["secType"],
            "currency": tws_df["currency"],
            "exchange": tws_df["fill_exchange"],
            "multiplier": pd.to_numeric(tws_df["multiplier"], errors="coerce"),
            "strike": tws_df["strike"].astype(float),
            "expiry": tws_df["lastTradeDateOrContractMonth"],
            "right": tws_df["right"].replace("?", None),
            # Execution details
            "side": tws_df["action"],  # Already BUY/SELL
            "quantity": tws_df["fill_shares"],
            "price": tws_df["fill_price"],
            "execution_time": tws_df["fill_execution_time"],  # Already in UTC
            "commission": -tws_df["fill_commission"].abs(),  # Standardize to negative
            "commission_currency": tws_df["fill_commissionCurrency"],
            "realized_pnl": tws_df["fill_realizedPNL"],
            # TWS-specific fields
            "order_type": tws_df["orderType"],
            "tif": tws_df["tif"],
            "limit_price": tws_df["lmtPrice"],
            "aux_price": tws_df["auxPrice"],
            "total_quantity": tws_df["totalQuantity"],
            "order_status": tws_df["status"],
            "filled": tws_df["filled"],
            "remaining": tws_df["remaining"],
            "avg_fill_price": tws_df["avgFillPrice"],
            # Flex-only fields (null for TWS)
            "trade_id": None,
            "transaction_id": None,
            "trade_date": None,
            "trade_money": None,
            "proceeds": None,
            "net_cash": None,
            "cost": None,
            "close_price": None,
            "mtm_pnl": None,
            "cusip": None,
            "isin": None,
            # Source tracking
            "_data_source": source_tag,
        }
    )

    # F3: Convert nullable integer columns to proper dtype (efficient)
    unified["tws_perm_id"] = unified["tws_perm_id"].astype("Int64")
    unified["flex_order_id"] = pd.NA  # Single value, not Series
    unified["trade_id"] = pd.NA
    unified["transaction_id"] = pd.NA
    # Cast to Int64 after assignment
    unified["flex_order_id"] = unified["flex_order_id"].astype("Int64")
    unified["trade_id"] = unified["trade_id"].astype("Int64")
    unified["transaction_id"] = unified["transaction_id"].astype("Int64")

    return unified


def prepare_flex_trades(flex_df: pd.DataFrame, source_tag: str = "FLEX") -> pd.DataFrame:
    """
    Transform Flex Report trades DataFrame to unified schema.

    Args:
        flex_df: Flex Report trades DataFrame
        source_tag: Tag to identify data source (default: "FLEX")

    Returns:
        DataFrame in unified schema

    Raises:
        KeyError: If required columns are missing
        ValueError: If schema validation fails
    """
    # F2: Check required columns exist
    required_cols = [
        "ibExecID",
        "accountId",
        "conid",
        "ibOrderID",
        "symbol",
        "assetCategory",
        "currency",
        "exchange",
        "multiplier",
        "strike",
        "expiry",
        "putCall",
        "buySell",
        "quantity",
        "tradePrice",
        "dateTime",
        "ibCommission",
        "ibCommissionCurrency",
        "fifoPnlRealized",
        "tradeID",
        "transactionID",
        "tradeDate",
        "tradeMoney",
        "proceeds",
        "netCash",
        "cost",
    ]
    missing = [col for col in required_cols if col not in flex_df.columns]
    if missing:
        raise KeyError(f"Missing required columns in Flex DataFrame: {missing}")

    # F5: Validate timezone awareness (Flex dateTime may not be UTC)
    datetime_col = pd.to_datetime(flex_df["dateTime"], utc=True)
    if not isinstance(datetime_col.dtype, pd.DatetimeTZDtype):
        warnings.warn("dateTime could not be converted to timezone-aware UTC datetime.", UserWarning)

    unified = pd.DataFrame(
        {
            # Primary key
            "ib_execution_id": flex_df["ibExecID"],
            # Core identifiers
            "account_id": flex_df["accountId"],
            "contract_id": flex_df["conid"],
            "tws_perm_id": None,  # Flex doesn't have TWS perm IDs
            "flex_order_id": flex_df["ibOrderID"],
            # Contract details
            "symbol": flex_df["symbol"],
            "asset_type": flex_df["assetCategory"],
            "currency": flex_df["currency"],
            "exchange": flex_df["exchange"],
            "multiplier": pd.to_numeric(flex_df["multiplier"], errors="coerce"),
            "strike": pd.to_numeric(flex_df["strike"], errors="coerce"),
            "expiry": flex_df["expiry"],
            "right": flex_df["putCall"],
            # Execution details
            "side": flex_df["buySell"],  # Already BUY/SELL
            "quantity": flex_df["quantity"].abs(),  # Take absolute value (Flex uses signed quantities)
            "price": flex_df["tradePrice"],
            "execution_time": pd.to_datetime(flex_df["dateTime"], utc=True),
            "commission": flex_df["ibCommission"],  # Already negative
            "commission_currency": flex_df["ibCommissionCurrency"],
            "realized_pnl": flex_df["fifoPnlRealized"],
            # TWS-specific fields (null for Flex)
            "order_type": None,
            "tif": None,
            "limit_price": None,
            "aux_price": None,
            "total_quantity": None,
            "order_status": None,
            "filled": None,
            "remaining": None,
            "avg_fill_price": None,
            # Flex-specific fields
            "trade_id": flex_df["tradeID"],
            "transaction_id": flex_df["transactionID"],
            "trade_date": flex_df["tradeDate"],
            "trade_money": flex_df["tradeMoney"],
            "proceeds": flex_df["proceeds"],
            "net_cash": flex_df["netCash"],
            "cost": flex_df["cost"],
            "close_price": flex_df.get("closePrice"),
            "mtm_pnl": flex_df.get("mtmPnl"),
            "cusip": flex_df.get("cusip"),
            "isin": flex_df.get("isin"),
            # Source tracking
            "_data_source": source_tag,
        }
    )

    # F3: Convert nullable integer columns to proper dtype (efficient)
    unified["tws_perm_id"] = pd.NA
    unified["tws_perm_id"] = unified["tws_perm_id"].astype("Int64")
    unified["flex_order_id"] = unified["flex_order_id"].astype("Int64")
    unified["trade_id"] = unified["trade_id"].astype("Int64")
    unified["transaction_id"] = unified["transaction_id"].astype("Int64")

    # Convert string columns to object dtype (handle NaN columns from CSV)
    for col in ["cusip", "isin"]:
        if col in unified.columns and unified[col].dtype != "object":
            unified[col] = unified[col].astype("object")

    return unified


def merge_unified_trades(
    tws_unified: Optional[pd.DataFrame] = None, flex_unified: Optional[pd.DataFrame] = None, dedup_strategy: str = "flex_first"
) -> pd.DataFrame:
    """
    Merge TWS and Flex unified DataFrames with deduplication.

    Args:
        tws_unified: Unified TWS trades (from prepare_tws_trades)
        flex_unified: Unified Flex trades (from prepare_flex_trades)
        dedup_strategy: How to handle duplicates:
            - "flex_first": Keep Flex as source of truth (default)
            - "tws_first": Keep TWS as source of truth
            - "last": Keep last occurrence (lexically FLEX before TWS)

    Returns:
        Merged and deduplicated DataFrame sorted by execution_time
    """
    # Collect dataframes to merge
    dfs_to_merge = []
    if flex_unified is not None and not flex_unified.empty:
        dfs_to_merge.append(flex_unified)
    if tws_unified is not None and not tws_unified.empty:
        dfs_to_merge.append(tws_unified)

    if not dfs_to_merge:
        # Return empty DataFrame with expected schema
        return pd.DataFrame(
            columns=[
                "ib_execution_id",
                "account_id",
                "contract_id",
                "tws_perm_id",
                "flex_order_id",
                "symbol",
                "asset_type",
                "currency",
                "exchange",
                "multiplier",
                "strike",
                "expiry",
                "right",
                "side",
                "quantity",
                "price",
                "execution_time",
                "commission",
                "commission_currency",
                "realized_pnl",
                "order_type",
                "tif",
                "limit_price",
                "aux_price",
                "total_quantity",
                "order_status",
                "filled",
                "remaining",
                "avg_fill_price",
                "trade_id",
                "transaction_id",
                "trade_date",
                "trade_money",
                "proceeds",
                "net_cash",
                "cost",
                "close_price",
                "mtm_pnl",
                "cusip",
                "isin",
                "_data_source",
            ]
        )

    # F1: Combine sources (suppress FutureWarning for empty/NA column handling)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries", category=FutureWarning)
        unified = pd.concat(dfs_to_merge, ignore_index=True)

    # Deduplicate based on strategy
    if dedup_strategy == "flex_first":
        # Sort so FLEX comes before TWS alphabetically, then keep first
        unified = unified.sort_values("_data_source")
        unified = unified.drop_duplicates(subset=["ib_execution_id"], keep="first")
    elif dedup_strategy == "tws_first":
        # Sort so TWS comes before FLEX, then keep first
        unified = unified.sort_values("_data_source", ascending=False)
        unified = unified.drop_duplicates(subset=["ib_execution_id"], keep="first")
    else:  # "last"
        unified = unified.drop_duplicates(subset=["ib_execution_id"], keep="last")

    # Sort by execution time
    unified = unified.sort_values("execution_time").reset_index(drop=True)

    return unified


def validate_unified_trades(df: pd.DataFrame, verbose: bool = True) -> bool:
    """
    Run validation checks on unified trades DataFrame.

    Args:
        df: Unified trades DataFrame to validate
        verbose: Print validation results (default: True)

    Returns:
        True if all checks pass, False otherwise
    """
    checks = {
        "no_null_execution_ids": df["ib_execution_id"].notna().all(),
        "no_duplicate_execution_ids": df["ib_execution_id"].duplicated().sum() == 0,
        "valid_sides": df["side"].isin(["BUY", "SELL"]).all(),
        "positive_quantities": (df["quantity"] > 0).all(),
        "positive_prices": (df["price"] >= 0).all(),
        "valid_execution_times": df["execution_time"].notna().all(),
    }

    if verbose:
        print("Validation Results:")
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")

    return all(checks.values())


def check_field_coverage(unified_df: pd.DataFrame) -> None:
    """
    Check which fields are populated by each data source.

    Args:
        unified_df: Unified trades DataFrame
    """
    tws_only = unified_df[unified_df["_data_source"] == "TWS"]
    flex_only = unified_df[unified_df["_data_source"] == "FLEX"]

    print("Field Coverage:")
    print(f"\nTWS trades (n={len(tws_only)}):")
    if len(tws_only) > 0:
        print(f"  order_type: {tws_only['order_type'].notna().sum()}")
        print(f"  limit_price: {tws_only['limit_price'].notna().sum()}")
        print(f"  order_status: {tws_only['order_status'].notna().sum()}")

    print(f"\nFlex trades (n={len(flex_only)}):")
    if len(flex_only) > 0:
        print(f"  trade_id: {flex_only['trade_id'].notna().sum()}")
        print(f"  cost: {flex_only['cost'].notna().sum()}")
        print(f"  proceeds: {flex_only['proceeds'].notna().sum()}")


def backfill_strategy(tws_unified: pd.DataFrame, flex_unified: pd.DataFrame, cutoff_hours: int = 24) -> pd.DataFrame:
    """
    Merge with backfill strategy: Flex as primary, TWS for recent trades.

    Use Flex reports as the primary source for historical data, and TWS for
    recent trades (within cutoff_hours).

    Args:
        tws_unified: Unified TWS trades
        flex_unified: Unified Flex trades
        cutoff_hours: Hours from now to consider "recent" (default: 24)

    Returns:
        Merged DataFrame with backfill strategy applied
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(hours=cutoff_hours)

    # Keep TWS trades from within cutoff period
    recent_tws = tws_unified[tws_unified["execution_time"] > cutoff_date].copy()

    # Keep all Flex trades
    all_flex = flex_unified.copy()

    # Combine (Flex first for deduplication)
    return merge_unified_trades(tws_unified=recent_tws, flex_unified=all_flex, dedup_strategy="flex_first")


def create_unified_trades(
    tws_df: Optional[pd.DataFrame] = None, flex_df: Optional[pd.DataFrame] = None, dedup_strategy: str = "flex_first", validate: bool = True
) -> pd.DataFrame:
    """
    Complete workflow: prepare, merge, and validate unified trades.

    This is the main entry point for creating unified trades from TWS and/or Flex data.

    Args:
        tws_df: Raw TWS trades (already expanded with expand_all_trade_columns, etc.)
        flex_df: Raw Flex trades DataFrame
        dedup_strategy: Deduplication strategy (see merge_unified_trades)
        validate: Run validation checks (default: True)

    Returns:
        Unified and validated trades DataFrame

    Example:
        >>> from ngv_reports_ibkr.unified_df import create_unified_trades
        >>> unified = create_unified_trades(
        ...     tws_df=tws_trades,
        ...     flex_df=flex_trades,
        ...     dedup_strategy="flex_first"
        ... )
        >>> print(f"Total trades: {len(unified)}")
    """
    # Prepare TWS data if provided
    tws_unified = None
    if tws_df is not None and not tws_df.empty:
        tws_unified = prepare_tws_trades(tws_df)

    # Prepare Flex data if provided
    flex_unified = None
    if flex_df is not None and not flex_df.empty:
        flex_unified = prepare_flex_trades(flex_df)

    # Merge
    unified = merge_unified_trades(tws_unified=tws_unified, flex_unified=flex_unified, dedup_strategy=dedup_strategy)

    # Validate if requested
    if validate and not unified.empty:
        is_valid = validate_unified_trades(unified)
        if not is_valid:
            print("⚠️  Validation failed - please review data")

    # Print summary
    if not unified.empty:
        print(f"\nTotal unified trades: {len(unified)}")
        print(f"  From TWS: {(unified['_data_source'] == 'TWS').sum()}")
        print(f"  From Flex: {(unified['_data_source'] == 'FLEX').sum()}")

    return unified
