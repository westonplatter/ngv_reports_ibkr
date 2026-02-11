"""
Manual Test: Unified Trades - TWS Realtime to Flex Report Reconciliation

Test Case: Trade something at CME Sunday open, verify permId matches ibOrderID in Flex report.

CME Sunday Open: 5:00 PM CT (6:00 PM ET)

Steps:
1. Sunday evening: Execute a trade (e.g., MES micro futures) via TWS
2. Sunday evening: Run ibkr_tws_realtime.ipynb to capture trades and save snapshot
3. Monday: Download Flex report via existing code:
     from ngv_reports_ibkr.download_trades import execute_csv_for_accounts
     execute_csv_for_accounts('annual', cache=True)
   This saves CSVs to: data/{account_id}_trades.csv
4. Run reconciliation below to verify permId == ibOrderID
"""

import pickle
from datetime import datetime
from pathlib import Path

import pandas as pd
from ib_async import util

# Paths
SNAPSHOTS_DIR = Path(__file__).parent.parent / "data" / "snapshots"
FLEX_REPORTS_DIR = Path(__file__).parent.parent / "data"


# =============================================================================
# Step 1: Capture TWS Realtime Trade (run Sunday evening after trade)
# =============================================================================


def capture_tws_trade_by_symbol(trades_snapshot_path: Path, symbol: str) -> pd.DataFrame:
    """
    Load TWS snapshot and filter to trades for a specific symbol.
    Returns DataFrame with key fields for reconciliation.
    """
    from ngv_reports_ibkr.expand_contract_columns import (
        expand_all_trade_columns,
        expand_fills_and_logs,
    )
    from ngv_reports_ibkr.transforms import Transforms

    # Load snapshot
    with open(trades_snapshot_path, "rb") as f:
        trades = pickle.load(f)
    print(f"Loaded {len(trades)} trades from {trades_snapshot_path.name}")

    # Convert to DataFrame and expand
    df = util.df(trades)
    df = expand_all_trade_columns(df)
    df = expand_fills_and_logs(df, fills_col="fills", log_col="log")
    df = Transforms.filter_to_executions(df)

    # Filter to symbol
    mask = df["symbol"] == symbol
    result = df[mask][
        [
            "permId",
            "symbol",
            "secType",
            "strike",
            "right",
            "lastTradeDateOrContractMonth",
            "action",
            "fill_shares",
            "fill_price",
            "fill_execution_id",
            "fill_execution_time",
            "fill_commission",
            "conId",
        ]
    ].copy()

    print(f"Found {len(result)} executions for {symbol}")
    return result


# =============================================================================
# Step 2: Download Flex Report and Save Snapshot
#
# Download and save timestamped copy:
#   from tests.test_unified_trades_manual import download_flex_report_snapshot
#   download_flex_report_snapshot()
#
# Output: data/snapshots/flex_trades_{account_id}_{timestamp}.csv
# =============================================================================


def download_flex_report_snapshot(account_id: str = None, snapshots_dir: Path = None):
    """
    Download Flex report and save a timestamped copy to data/snapshots/.
    Also saves via the standard adapter to data/{account_id}_trades.csv.
    """
    from ngv_reports_ibkr.config_helpers import get_config, get_ib_json
    from ngv_reports_ibkr.download_trades import fetch_report

    if snapshots_dir is None:
        snapshots_dir = SNAPSHOTS_DIR
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    configs = get_config(".env")
    data = get_ib_json(configs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for account in data.get("accounts", []):
        acct_name = account["name"]
        if account_id and acct_name != account_id:
            continue

        query_id = int(account.get("annual", 0))
        if query_id <= 0:
            print(f"Skipping {acct_name}: no annual query_id")
            continue

        flex_token = account["flex_token"]
        report = fetch_report(flex_token, query_id, cache_report_on_disk=True)

        for aid in report.account_ids():
            trades_df = report.trades_by_account_id(aid)
            if trades_df is not None:
                csv_path = snapshots_dir / f"flex_trades_{aid}_{timestamp}.csv"
                trades_df.to_csv(csv_path)
                print(f"Saved Flex report snapshot: {csv_path.name}")


def find_flex_csv(account_id: str, snapshots_dir: Path = None) -> Path:
    """Find the most recent Flex report CSV for a given account in snapshots/."""
    if snapshots_dir is None:
        snapshots_dir = SNAPSHOTS_DIR
    csvs = sorted(snapshots_dir.glob(f"flex_trades_{account_id}_*.csv"))
    if not csvs:
        # Fall back to data/ folder
        fallback = Path(__file__).parent.parent / "data" / f"{account_id}_trades.csv"
        if fallback.exists():
            return fallback
        raise FileNotFoundError(f"No Flex CSV found for {account_id}. Run download_flex_report_snapshot() first.")
    print(f"Loading most recent Flex snapshot: {csvs[-1].name}")
    return csvs[-1]


def load_flex_trade_by_order_id(flex_csv_path: Path, ib_order_id: int) -> pd.DataFrame:
    """
    Load Flex report CSV and filter to trades matching ibOrderID.
    Returns DataFrame with key fields for reconciliation.
    """
    df = pd.read_csv(flex_csv_path, low_memory=False)

    # Filter to order ID
    mask = df["ibOrderID"] == ib_order_id
    result = df[mask][
        [
            "ibOrderID",
            "symbol",
            "assetCategory",
            "strike",
            "putCall",
            "expiry",
            "buySell",
            "quantity",
            "tradePrice",
            "ibExecID",
            "dateTime",
            "ibCommission",
            "conid",
        ]
    ].copy()

    print(f"Found {len(result)} executions for ibOrderID {ib_order_id}")
    return result


# =============================================================================
# Step 3: Reconcile TWS and Flex Data
# =============================================================================


def reconcile_trades(tws_df: pd.DataFrame, flex_df: pd.DataFrame) -> pd.DataFrame:
    """
    Join TWS and Flex data on execution ID and compare fields.
    """
    # Rename columns for clarity
    tws_renamed = tws_df.rename(
        columns={
            "permId": "tws_permId",
            "fill_shares": "tws_quantity",
            "fill_price": "tws_price",
            "fill_execution_id": "tws_exec_id",
            "fill_execution_time": "tws_exec_time",
            "fill_commission": "tws_commission",
            "conId": "tws_conId",
        }
    )

    flex_renamed = flex_df.rename(
        columns={
            "ibOrderID": "flex_ibOrderID",
            "quantity": "flex_quantity",
            "tradePrice": "flex_price",
            "ibExecID": "flex_exec_id",
            "dateTime": "flex_exec_time",
            "ibCommission": "flex_commission",
            "conid": "flex_conid",
        }
    )

    # Join on execution ID
    merged = pd.merge(
        tws_renamed,
        flex_renamed,
        left_on="tws_exec_id",
        right_on="flex_exec_id",
        how="outer",
        indicator=True,
    )

    return merged


def validate_reconciliation(merged_df: pd.DataFrame) -> dict:
    """
    Validate that key fields match between TWS and Flex.
    """
    results = {
        "total_rows": len(merged_df),
        "matched": len(merged_df[merged_df["_merge"] == "both"]),
        "tws_only": len(merged_df[merged_df["_merge"] == "left_only"]),
        "flex_only": len(merged_df[merged_df["_merge"] == "right_only"]),
        "field_checks": {},
    }

    matched = merged_df[merged_df["_merge"] == "both"]

    if len(matched) > 0:
        # Check permId == ibOrderID
        results["field_checks"]["permId_matches_ibOrderID"] = (matched["tws_permId"] == matched["flex_ibOrderID"]).all()

        # Check conId == conid
        results["field_checks"]["conId_matches"] = (matched["tws_conId"] == matched["flex_conid"]).all()

        # Check quantity matches
        results["field_checks"]["quantity_matches"] = (matched["tws_quantity"] == matched["flex_quantity"]).all()

        # Check price matches (within tolerance for float)
        results["field_checks"]["price_matches"] = ((matched["tws_price"] - matched["flex_price"]).abs() < 0.0001).all()

    return results


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Unified Trades Reconciliation Test")
    print("=" * 60)

    # Example: Find most recent snapshot
    snapshots = sorted(SNAPSHOTS_DIR.glob("tws_trades_*.pkl"))
    if snapshots:
        print(f"\nAvailable TWS snapshots:")
        for s in snapshots[-5:]:  # Show last 5
            print(f"  {s.name}")

        # Load most recent and show symbols
        latest = snapshots[-1]
        print(f"\nLoading {latest.name}...")

        with open(latest, "rb") as f:
            trades = pickle.load(f)

        if trades:
            df = util.df(trades)
            if "contract" in df.columns:
                symbols = df["contract"].apply(lambda c: getattr(c, "symbol", None) if c else None)
                print(f"Symbols in snapshot: {symbols.unique().tolist()}")
    else:
        print("\nNo TWS snapshots found. Run the notebook with TWS connected first.")

    # List available Flex snapshots
    flex_csvs = sorted(SNAPSHOTS_DIR.glob("flex_trades_*.csv")) if SNAPSHOTS_DIR.exists() else []
    if flex_csvs:
        print(f"\nAvailable Flex snapshots:")
        for c in flex_csvs[-5:]:
            print(f"  {c.name}")

    print("\n" + "=" * 60)
    print("To run the full test:")
    print("=" * 60)
    print(
        """
1. Sunday 6 PM ET: Execute a CME trade (e.g., MES, MNQ)

2. Sunday evening: Save TWS snapshot
   - Run ibkr_tws_realtime.ipynb (saves to data/snapshots/tws_trades_YYYYMMDD_HHMMSS.pkl)
   - Note the permId from the reconciliation view

3. Monday: Download Flex report snapshot
   from tests.test_unified_trades_manual import download_flex_report_snapshot
   download_flex_report_snapshot()
   # Saves to data/snapshots/flex_trades_{account_id}_{timestamp}.csv

4. Run reconciliation:

   from pathlib import Path
   from tests.test_unified_trades_manual import (
       capture_tws_trade_by_symbol,
       find_flex_csv,
       load_flex_trade_by_order_id,
       reconcile_trades,
       validate_reconciliation,
   )

   # Load TWS trade
   tws_df = capture_tws_trade_by_symbol(
       Path("data/snapshots/tws_trades_YYYYMMDD_HHMMSS.pkl"),
       symbol="MES"
   )

   # Load Flex trade by permId
   flex_csv = find_flex_csv("U1234567")  # Your account ID
   flex_df = load_flex_trade_by_order_id(
       flex_csv,
       ib_order_id=tws_df["permId"].iloc[0]
   )

   # Reconcile and validate
   merged = reconcile_trades(tws_df, flex_df)
   results = validate_reconciliation(merged)
   print(results)
"""
    )
