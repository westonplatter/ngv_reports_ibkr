"""
Simple utility to expand ib_async contract objects into DataFrame columns.
"""

import sys
import pandas as pd
# IBKR uses max float64 as "UNSET" indicator
UNSET_DOUBLE = sys.float_info.max
UNSET_INTEGER = 2147483647  # INT_MAX


def _clean_unset_value(value):
    """Replace IBKR's UNSET values with None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # Check if value is UNSET_DOUBLE or very close to it
        if abs(value - UNSET_DOUBLE) < 1e100 or value == UNSET_INTEGER:
            return None
    return value


def extract_object_attributes(obj, clean_numeric=False, exclude_attrs=None):
    """
    Extract data attributes from an object into a dictionary.

    Args:
        obj: Object to extract attributes from
        clean_numeric: Apply _clean_unset_value to numeric fields
        exclude_attrs: List of attribute names to skip

    Returns:
        Dictionary of attribute names and values
    """
    if obj is None:
        return {}

    exclude_attrs = exclude_attrs or []
    data = {}

    for attr_name in dir(obj):
        # Skip dunder methods, private methods, and excluded attrs
        if attr_name.startswith("_") or attr_name in exclude_attrs:
            continue

        # Skip callable methods
        attr_value = getattr(obj, attr_name, None)
        if callable(attr_value):
            continue

        # Clean numeric values if requested
        if clean_numeric and isinstance(attr_value, (int, float)):
            attr_value = _clean_unset_value(attr_value)

        data[attr_name] = attr_value

    return data


def expand_contract_column(df: pd.DataFrame, contract_col: str = "contract") -> pd.DataFrame:
    """
    Expand ib_async contract objects into separate DataFrame columns.

    Args:
        df: DataFrame containing contract objects
        contract_col: Name of column containing contract objects (default: 'contract')

    Returns:
        DataFrame with contract attributes as separate columns
    """
    contract_data = []

    for _, row in df.iterrows():
        contract = row[contract_col]
        if contract is None:
            contract_data.append({})
            continue

        data = {
            "conId": getattr(contract, "conId", None),
            "symbol": getattr(contract, "symbol", None),
            "secType": getattr(contract, "secType", None),
            "exchange": getattr(contract, "exchange", None),
            "currency": getattr(contract, "currency", None),
            "localSymbol": getattr(contract, "localSymbol", None),
            "tradingClass": getattr(contract, "tradingClass", None),
        }

        # Add contract-type specific fields
        if hasattr(contract, "lastTradeDateOrContractMonth"):
            data["lastTradeDateOrContractMonth"] = contract.lastTradeDateOrContractMonth
        if hasattr(contract, "multiplier"):
            data["multiplier"] = contract.multiplier
        if hasattr(contract, "strike"):
            data["strike"] = contract.strike
        if hasattr(contract, "right"):
            data["right"] = contract.right

        contract_data.append(data)

    contract_df = pd.DataFrame(contract_data)
    result_df = pd.concat([df.drop(contract_col, axis=1).reset_index(drop=True), contract_df.reset_index(drop=True)], axis=1)

    return result_df


def expand_order_column(df: pd.DataFrame, order_col: str = "order") -> pd.DataFrame:
    """
    Expand ib_async order objects into separate DataFrame columns.

    Args:
        df: DataFrame containing order objects
        order_col: Name of column containing order objects (default: 'order')

    Returns:
        DataFrame with order attributes as separate columns
    """
    order_data = []

    for _, row in df.iterrows():
        order = row[order_col]
        if order is None:
            order_data.append({})
            continue

        data = extract_object_attributes(order, clean_numeric=True)

        order_data.append(data)

    order_df = pd.DataFrame(order_data)
    result_df = pd.concat([df.drop(order_col, axis=1).reset_index(drop=True), order_df.reset_index(drop=True)], axis=1)

    return result_df


def expand_order_status_column(df: pd.DataFrame, status_col: str = "orderStatus") -> pd.DataFrame:
    """
    Expand ib_async orderStatus objects into separate DataFrame columns.

    Args:
        df: DataFrame containing orderStatus objects
        status_col: Name of column containing orderStatus objects (default: 'orderStatus')

    Returns:
        DataFrame with orderStatus attributes as separate columns
    """
    status_data = []

    for _, row in df.iterrows():
        status = row[status_col]
        if status is None:
            status_data.append({})
            continue

        data = {
            "status": getattr(status, "status", None),
            "filled": getattr(status, "filled", None),
            "remaining": getattr(status, "remaining", None),
            "avgFillPrice": getattr(status, "avgFillPrice", None),
            "lastFillPrice": getattr(status, "lastFillPrice", None),
        }

        status_data.append(data)

    status_df = pd.DataFrame(status_data)
    result_df = pd.concat([df.drop(status_col, axis=1).reset_index(drop=True), status_df.reset_index(drop=True)], axis=1)

    return result_df


def expand_fills_and_logs(df: pd.DataFrame, fills_col: str = "fills", log_col: str = "log") -> pd.DataFrame:
    """
    Expand both fills and log columns to create one row per fill/log entry.

    This function combines fills (executions) and log entries (trade history) into a single
    expanded DataFrame where each fill or log entry becomes its own row, with all order data duplicated.

    Args:
        df: DataFrame containing fills and log columns
        fills_col: Name of column containing fills list (default: 'fills')
        log_col: Name of column containing log entries list (default: 'log')

    Returns:
        DataFrame with one row per fill/log entry, with attributes as separate columns
    """
    expanded_rows = []

    for idx, row in df.iterrows():
        # Get fills and logs
        fills = row[fills_col] if fills_col in df.columns else []
        logs = row[log_col] if log_col in df.columns else []

        # Get all columns except fills and log
        cols_to_drop = [c for c in [fills_col, log_col] if c in df.columns]
        base_data = row.drop(cols_to_drop).to_dict()

        # Determine the maximum number of entries (fills or logs)
        max_entries = max(len(fills) if fills else 0, len(logs) if logs else 0)

        if max_entries == 0:
            # No fills or logs - create one row with empty data
            expanded_row = base_data.copy()
            expanded_row.update(
                {
                    # Fill metadata
                    "fill_time_direct": None,
                    # Fill execution data
                    "fill_execution_id": None,
                    "fill_execution_time": None,
                    "fill_shares": None,
                    "fill_price": None,
                    "fill_exchange": None,
                    "fill_side": None,
                    "fill_cumQty": None,
                    "fill_avgPrice": None,
                    # Fill commission data
                    "fill_commission": None,
                    "fill_commissionCurrency": None,
                    "fill_realizedPNL": None,
                    # Fill contract data
                    "fill_contract_conId": None,
                    # Log data
                    "log_time": None,
                    "log_status": None,
                    "log_message": None,
                    "log_errorCode": None,
                }
            )
            expanded_rows.append(expanded_row)
        else:
            # Create one row per entry (fills or logs, whichever has more)
            for i in range(max_entries):
                expanded_row = base_data.copy()

                # Extract fill data if available
                if fills and i < len(fills):
                    fill = fills[i]
                    execution = getattr(fill, "execution", None) if fill else None
                    commission_report = getattr(fill, "commissionReport", None) if fill else None
                    fill_contract = getattr(fill, "contract", None) if fill else None

                    expanded_row.update(
                        {
                            # Fill metadata (time is the main attribute we need)
                            # Note: 'index' and 'count' are built-in list methods, not fill attributes
                            "fill_time_direct": getattr(fill, "time", None) if fill else None,
                            # Execution details
                            "fill_execution_id": getattr(execution, "execId", None) if execution else None,
                            "fill_execution_time": getattr(execution, "time", None) if execution else None,
                            "fill_shares": getattr(execution, "shares", None) if execution else None,
                            "fill_price": getattr(execution, "price", None) if execution else None,
                            "fill_exchange": getattr(execution, "exchange", None) if execution else None,
                            "fill_side": getattr(execution, "side", None) if execution else None,
                            "fill_cumQty": getattr(execution, "cumQty", None) if execution else None,
                            "fill_avgPrice": getattr(execution, "avgPrice", None) if execution else None,
                            # Commission details
                            "fill_commission": getattr(commission_report, "commission", None) if commission_report else None,
                            "fill_commissionCurrency": getattr(commission_report, "currency", None) if commission_report else None,
                            "fill_realizedPNL": getattr(commission_report, "realizedPNL", None) if commission_report else None,
                            # Contract details (conId for joining back to contract info)
                            "fill_contract_conId": getattr(fill_contract, "conId", None) if fill_contract else None,
                        }
                    )
                else:
                    # No fill at this index
                    expanded_row.update(
                        {
                            # Fill metadata
                            "fill_time_direct": None,
                            # Execution details
                            "fill_execution_id": None,
                            "fill_execution_time": None,
                            "fill_shares": None,
                            "fill_price": None,
                            "fill_exchange": None,
                            "fill_side": None,
                            "fill_cumQty": None,
                            "fill_avgPrice": None,
                            # Commission details
                            "fill_commission": None,
                            "fill_commissionCurrency": None,
                            "fill_realizedPNL": None,
                            # Contract details
                            "fill_contract_conId": None,
                        }
                    )

                # Extract log data if available
                if logs and i < len(logs):
                    log_entry = logs[i]
                    expanded_row.update(
                        {
                            "log_time": getattr(log_entry, "time", None),
                            "log_status": getattr(log_entry, "status", None),
                            "log_message": getattr(log_entry, "message", None),
                            "log_errorCode": getattr(log_entry, "errorCode", None),
                        }
                    )
                else:
                    # No log at this index
                    expanded_row.update(
                        {
                            "log_time": None,
                            "log_status": None,
                            "log_message": None,
                            "log_errorCode": None,
                        }
                    )

                expanded_rows.append(expanded_row)

    result_df = pd.DataFrame(expanded_rows)
    return result_df


def expand_all_trade_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expand all ib_async trade-related object columns (contract, order, orderStatus).

    Args:
        df: DataFrame containing trade objects

    Returns:
        DataFrame with all object columns expanded
    """
    result = df.copy()

    if "contract" in result.columns:
        result = expand_contract_column(result, "contract")

    if "order" in result.columns:
        result = expand_order_column(result, "order")

    if "orderStatus" in result.columns:
        result = expand_order_status_column(result, "orderStatus")

    return result
