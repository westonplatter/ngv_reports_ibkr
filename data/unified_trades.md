# Unified Trades: TWS + Flex Report

Strategy for creating a unified trades list that combines IBKR TWS realtime trades with Flex Report trades.

## Overview

**Goal**: Create a single unified trades DataFrame that can accept trades from both TWS realtime API and Flex reports, using execution ID as the primary key for deduplication.

**Key Insight**: Both sources provide execution-level data that can be joined on `fill_execution_id` (TWS) = `ibExecID` (Flex).

**Use Cases**:
1. Real-time trade tracking via TWS, backfilled/verified with daily Flex reports
2. Augment Flex report data with real-time TWS fields (order status, limit prices)
3. Detect discrepancies between what TWS reports and what Flex settles

## Unified Schema Strategy

### Primary Key: Execution ID

| Source | Field | Type | Notes |
|--------|-------|------|-------|
| TWS | `fill_execution_id` | string | Format: `00001234.abcd5678.01.01` |
| Flex | `ibExecID` | string | Format: `00001234.abcd5678.01.01` |
| **Unified** | `ib_execution_id` | string | ✅ Use this as primary key |

**Deduplication Strategy**:
```python
# When inserting from either source, check if ib_execution_id already exists
df_unified = pd.concat([tws_df, flex_df]).drop_duplicates(subset=['ib_execution_id'], keep='last')
```

### Source Tracking

Add a `_data_source` column to track origin:
```python
tws_df['_data_source'] = 'TWS'
flex_df['_data_source'] = 'FLEX'
```

### Order ID (Source-Specific)

**Important**: `permId` (TWS) and `ibOrderID` (Flex) are **NOT** equivalent:
- TWS `permId`: ~1.4 billion range (e.g., 1400000000)
- Flex `ibOrderID`: ~800 million - 4 billion range (e.g., 900000000)

**Strategy**: Keep both in separate columns, do not attempt to unify:
```python
# In unified schema
'tws_perm_id': from TWS permId (null for Flex-only trades)
'flex_order_id': from Flex ibOrderID (null for TWS-only trades)
```

## Complete Field Mapping

### Core Identifiers

| Unified Field | Flex Report | TWS Realtime | Type | Transform |
|---------------|-------------|--------------|------|-----------|
| `ib_execution_id` | `ibExecID` | `fill_execution_id` | string | Primary key |
| `account_id` | `accountId` | `account` | string | Direct |
| `contract_id` | `conid` | `conId` | int64 | Direct |
| `flex_order_id` | `ibOrderID` | null | int64 | Flex-only |
| `tws_perm_id` | null | `permId` | int64 | TWS-only |
| `_data_source` | 'FLEX' | 'TWS' | string | Tag source |

### Contract Details

| Unified Field | Flex Report | TWS Realtime | Type | Transform |
|---------------|-------------|--------------|------|-----------|
| `symbol` | `symbol` | `symbol` | string | Direct |
| `asset_type` | `assetCategory` | `secType` | string | Direct (STK/OPT/FOP/FUT) |
| `currency` | `currency` | `currency` | string | Direct |
| `exchange` | `exchange` | `fill_exchange` | string | Direct |
| `multiplier` | `multiplier` | `multiplier` | float64 | Cast both to float64 |
| `strike` | `strike` | `strike` | float64 | Cast to float, NaN for non-options |
| `expiry` | `expiry` | `lastTradeDateOrContractMonth` | string | Format: YYYYMMDD |
| `right` | `putCall` | `right` | string | C/P/null |

### Execution Details

| Unified Field | Flex Report | TWS Realtime | Type | Transform |
|---------------|-------------|--------------|------|-----------|
| `side` | `buySell` | `action` | string | Normalize to BUY/SELL |
| `quantity` | `quantity` | `fill_shares` | float64 | Direct |
| `price` | `tradePrice` | `fill_price` | float64 | Direct |
| `execution_time` | `dateTime` | `fill_execution_time` | datetime64[ns, UTC] | Convert both to UTC |
| `commission` | `ibCommission` | `fill_commission` | float64 | Standardize sign (suggest negative) |
| `commission_currency` | `ibCommissionCurrency` | `fill_commissionCurrency` | string | Direct |
| `realized_pnl` | `fifoPnlRealized` | `fill_realizedPNL` | float64 | Direct |

### Flex-Only Fields (keep for enrichment)

| Unified Field | Flex Report | Type | Notes |
|---------------|-------------|------|-------|
| `trade_id` | `tradeID` | int64 | Flex trade identifier |
| `transaction_id` | `transactionID` | int64 | Flex transaction identifier |
| `trade_date` | `tradeDate` | date | Settlement date |
| `trade_money` | `tradeMoney` | float64 | Total trade value |
| `proceeds` | `proceeds` | float64 | Net proceeds |
| `net_cash` | `netCash` | float64 | Cash impact |
| `cost` | `cost` | float64 | Cost basis |
| `close_price` | `closePrice` | float64 | Closing price |
| `mtm_pnl` | `mtmPnl` | float64 | Mark-to-market P&L |
| `cusip` | `cusip` | string | Security identifier |
| `isin` | `isin` | string | Security identifier |

### TWS-Only Fields (keep for real-time tracking)

| Unified Field | TWS Realtime | Type | Notes |
|---------------|--------------|------|-------|
| `order_type` | `orderType` | string | LMT, MKT, STP, etc. |
| `tif` | `tif` | string | Time in force (DAY, GTC) |
| `limit_price` | `lmtPrice` | float64 | Limit order price |
| `aux_price` | `auxPrice` | float64 | Stop price |
| `total_quantity` | `totalQuantity` | float64 | Order quantity |
| `order_status` | `status` | string | Submitted, Filled, etc. |
| `filled` | `filled` | float64 | Cumulative filled |
| `remaining` | `remaining` | float64 | Remaining quantity |
| `avg_fill_price` | `avgFillPrice` | float64 | Average fill price |

## Data Transformations

### 1. Side Normalization

```python
def normalize_side(tws_df, flex_df):
    """Normalize buy/sell side to BUY/SELL."""
    # TWS: action is already BUY/SELL
    tws_df['side'] = tws_df['action']

    # Flex: buySell is already BUY/SELL
    flex_df['side'] = flex_df['buySell']

    return tws_df, flex_df
```

### 2. Timezone Normalization

```python
def normalize_execution_time(tws_df, flex_df):
    """Convert execution times to UTC."""
    # TWS: already in UTC
    tws_df['execution_time'] = tws_df['fill_execution_time']

    # Flex: convert US/Eastern to UTC
    flex_df['execution_time'] = pd.to_datetime(flex_df['dateTime'], utc=True)

    return tws_df, flex_df
```

### 3. Commission Sign Standardization

```python
def normalize_commission(tws_df, flex_df):
    """Standardize commission to negative (cost)."""
    # TWS: positive values, make negative
    tws_df['commission'] = -tws_df['fill_commission'].abs()

    # Flex: already negative
    flex_df['commission'] = flex_df['ibCommission']

    return tws_df, flex_df
```

### 4. Strike/Multiplier Type Casting

```python
def normalize_numeric_fields(tws_df, flex_df):
    """Cast strike and multiplier to float64."""
    # Strike: convert empty strings to NaN, cast to float
    flex_df['strike'] = pd.to_numeric(flex_df['strike'], errors='coerce')
    tws_df['strike'] = tws_df['strike'].astype(float)

    # Multiplier: cast both to float
    flex_df['multiplier'] = pd.to_numeric(flex_df['multiplier'], errors='coerce')
    tws_df['multiplier'] = pd.to_numeric(tws_df['multiplier'], errors='coerce')

    return tws_df, flex_df
```

## Implementation Example

### Step 1: Prepare TWS Data

```python
from ngv_reports_ibkr.transforms import Transforms
from ngv_reports_ibkr.expand_contract_columns import expand_all_trade_columns, expand_fills_and_logs

# Process TWS trades
tws_df = util.df(tws_trade_objects)
tws_df = expand_all_trade_columns(tws_df)
tws_df = expand_fills_and_logs(tws_df, fills_col="fills", log_col="log")
tws_df = Transforms.filter_to_executions(tws_df)  # Keep only fills

# Map to unified schema
tws_unified = pd.DataFrame({
    'ib_execution_id': tws_df['fill_execution_id'],
    'account_id': tws_df['account'],
    'contract_id': tws_df['conId'],
    'tws_perm_id': tws_df['permId'],
    'flex_order_id': None,
    'symbol': tws_df['symbol'],
    'asset_type': tws_df['secType'],
    'currency': tws_df['currency'],
    'exchange': tws_df['fill_exchange'],
    'multiplier': pd.to_numeric(tws_df['multiplier'], errors='coerce'),
    'strike': tws_df['strike'].astype(float),
    'expiry': tws_df['lastTradeDateOrContractMonth'],
    'right': tws_df['right'].replace('?', None),
    'side': tws_df['action'],
    'quantity': tws_df['fill_shares'],
    'price': tws_df['fill_price'],
    'execution_time': tws_df['fill_execution_time'],
    'commission': -tws_df['fill_commission'].abs(),
    'commission_currency': tws_df['fill_commissionCurrency'],
    'realized_pnl': tws_df['fill_realizedPNL'],
    # TWS-specific fields
    'order_type': tws_df['orderType'],
    'tif': tws_df['tif'],
    'limit_price': tws_df['lmtPrice'],
    'order_status': tws_df['status'],
    '_data_source': 'TWS'
})
```

### Step 2: Prepare Flex Data

```python
from ngv_reports_ibkr.download_trades import fetch_report

# Fetch Flex report
report = fetch_report(flex_token, query_id, cache_report_on_disk=True)
flex_df = report.trades_by_account_id(account_id)

# Map to unified schema
flex_unified = pd.DataFrame({
    'ib_execution_id': flex_df['ibExecID'],
    'account_id': flex_df['accountId'],
    'contract_id': flex_df['conid'],
    'tws_perm_id': None,
    'flex_order_id': flex_df['ibOrderID'],
    'symbol': flex_df['symbol'],
    'asset_type': flex_df['assetCategory'],
    'currency': flex_df['currency'],
    'exchange': flex_df['exchange'],
    'multiplier': pd.to_numeric(flex_df['multiplier'], errors='coerce'),
    'strike': pd.to_numeric(flex_df['strike'], errors='coerce'),
    'expiry': flex_df['expiry'],
    'right': flex_df['putCall'],
    'side': flex_df['buySell'],
    'quantity': flex_df['quantity'],
    'price': flex_df['tradePrice'],
    'execution_time': pd.to_datetime(flex_df['dateTime'], utc=True),
    'commission': flex_df['ibCommission'],
    'commission_currency': flex_df['ibCommissionCurrency'],
    'realized_pnl': flex_df['fifoPnlRealized'],
    # Flex-specific fields
    'trade_id': flex_df['tradeID'],
    'transaction_id': flex_df['transactionID'],
    'trade_date': flex_df['tradeDate'],
    'trade_money': flex_df['tradeMoney'],
    'proceeds': flex_df['proceeds'],
    'net_cash': flex_df['netCash'],
    'cost': flex_df['cost'],
    'cusip': flex_df['cusip'],
    'isin': flex_df['isin'],
    '_data_source': 'FLEX'
})
```

### Step 3: Merge and Deduplicate

```python
# Combine both sources
unified_trades = pd.concat([tws_unified, flex_unified], ignore_index=True)

# Deduplicate by ib_execution_id (keep Flex as source of truth if duplicate)
unified_trades = unified_trades.sort_values('_data_source')  # FLEX comes before TWS alphabetically
unified_trades = unified_trades.drop_duplicates(subset=['ib_execution_id'], keep='first')

# Sort by execution time
unified_trades = unified_trades.sort_values('execution_time').reset_index(drop=True)

print(f"Total unified trades: {len(unified_trades)}")
print(f"  From TWS: {(unified_trades['_data_source'] == 'TWS').sum()}")
print(f"  From Flex: {(unified_trades['_data_source'] == 'FLEX').sum()}")
```

### Step 4: Validation

```python
def validate_unified_trades(df):
    """Run validation checks on unified trades."""
    checks = {
        'no_null_execution_ids': df['ib_execution_id'].notna().all(),
        'no_duplicate_execution_ids': df['ib_execution_id'].duplicated().sum() == 0,
        'valid_sides': df['side'].isin(['BUY', 'SELL']).all(),
        'positive_quantities': (df['quantity'] > 0).all(),
        'positive_prices': (df['price'] >= 0).all(),
        'valid_execution_times': df['execution_time'].notna().all(),
    }

    print("Validation Results:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")

    return all(checks.values())

validate_unified_trades(unified_trades)
```

## Reconciliation Workflow

### Daily Process

1. **Morning**: Download Flex report (captures T-1 trades)
2. **All Day**: Collect TWS realtime trades as they happen
3. **Evening**: Merge TWS and Flex, deduplicate on ib_execution_id
4. **Result**: Unified trades list with:
   - Today's trades from TWS (real-time)
   - Yesterday's trades from Flex (verified)
   - Optional: TWS trades older than 1 day can be dropped (already in Flex)

### Backfill Strategy

```python
# For historical analysis: Use Flex as primary source
# For recent trades (< 1 day): Use TWS for real-time tracking
cutoff_date = datetime.now(timezone.utc) - timedelta(days=1)

# Keep TWS trades from last 24 hours
recent_tws = tws_unified[tws_unified['execution_time'] > cutoff_date]

# Keep all Flex trades
all_flex = flex_unified.copy()

# Combine
unified = pd.concat([all_flex, recent_tws], ignore_index=True)
unified = unified.drop_duplicates(subset=['ib_execution_id'], keep='first')
```

## Verification Tests

### Test 1: Sunday CME → Monday Flex

See `notebooks/ibkr_tws_realtime.ipynb` for interactive reconciliation.

**Steps**:
1. Sunday 6 PM ET: Execute trade at CME open
2. Sunday evening: Save TWS snapshot
3. Monday: Download Flex report
4. Monday: Run reconciliation cell

**Expected Results**:
- ✅ Execution IDs match
- ✅ Contract IDs match
- ✅ Quantities match
- ✅ Prices match within tolerance
- ⚠️ Order IDs do NOT match (different systems)

### Test 2: Field Completeness

```python
def check_field_coverage(unified_df):
    """Check which fields are populated by source."""
    tws_only = unified_df[unified_df['_data_source'] == 'TWS']
    flex_only = unified_df[unified_df['_data_source'] == 'FLEX']

    print("Field Coverage:")
    print(f"\nTWS fields (n={len(tws_only)}):")
    print(f"  order_type: {tws_only['order_type'].notna().sum()}")
    print(f"  limit_price: {tws_only['limit_price'].notna().sum()}")

    print(f"\nFlex fields (n={len(flex_only)}):")
    print(f"  trade_id: {flex_only['trade_id'].notna().sum()}")
    print(f"  cost: {flex_only['cost'].notna().sum()}")
```

## Notes and Gotchas

1. **Order ID Mismatch**: `permId` ≠ `ibOrderID` - these are different ID spaces managed by TWS vs IB backend
2. **Execution ID is Reliable**: Format like `00001234.abcd5678.01.01` is consistent across both systems
3. **1-Day Delay**: Flex reports have ~24hr delay, use TWS for same-day tracking
4. **Commission Sign**: Standardize to negative (commission as a cost)
5. **Timezone**: Always convert to UTC for consistency
6. **orderRef Does Not Propagate**: TWS `orderRef` field does NOT appear in Flex `orderReference`
7. **Partial Fills**: Each partial fill gets its own ib_execution_id, properly handled by this schema

## Related Files

- Implementation: `notebooks/ibkr_tws_realtime.ipynb`
- Test Cases: `tests/test_unified_trades_manual.py`
- TWS Schema: `ngv_reports_ibkr/schemas/ibkr_tws_trades.py`
- Flex Schema: `ngv_reports_ibkr/schemas/ibkr_flex_report.py`
- Transforms: `ngv_reports_ibkr/transforms.py`
