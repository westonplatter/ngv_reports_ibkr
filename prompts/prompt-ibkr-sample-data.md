# IBKR Sample Data Anonymization Prompt

When creating or updating sample data documentation for IBKR (Interactive Brokers)
data schemas, **always use anonymized, generic values** instead of real personal
account data.

## Fields to Anonymize

### Account & Identity Information

- **Account IDs**: Use generic formats like `U1234567`, `U9999999`
- **Client IDs**: Use sequential or generic values
- **Trader IDs**: Generic alphanumeric if needed

### Contract & Security Identifiers

- **Contract IDs (conId)**: Use generic sequential IDs
  - Example: `123456789`, `234567890`, `345678901`, `400000001`, etc.
- **Underlying Contract IDs**: Use generic sequential IDs
  - Example: `111111111`, `222222222`, `333333333`
- **Fill Contract IDs**: Use generic sequential with decimals
  - Example: `600000001.0`, `600000002.0`, `600000003.0`

### Transaction & Order Identifiers

- **Trade IDs**: Use generic sequential IDs starting from round numbers
  - Example: `1000000001`, `1000000002`, `1000000003`
- **Transaction IDs**: Use different range for distinction
  - Example: `5000000001`, `5000000002`, `5000000003`
- **Order IDs (ibOrderID)**: Use another distinct range
  - Example: `9000000001`, `9000000002`, `9000000003`
- **Permission IDs (permId)**: Use varied generic values
  - Example: `8888888`, `9999999`, `7777777`

### Execution & Brokerage IDs

- **Execution IDs (ibExecID)**: Use generic hex-like format
  - Example: `0000abcd.12345678.01.01`, `0000efgh.23456789.01.01`, `0000ijkl.34567890.01.01`
  - Alternative: `0000wxyz.abcd1234.01.01`, `0000efgh.5678ijkl.01.01`
- **Brokerage Order IDs**: Use generic hex patterns
  - Example: `00aabbcc.00ddeeff.11223344.000`, `00aabbcc.00ddeeff.55667788.999`
- **External Execution IDs (extExecID)**: Use generic alphanumeric
  - Example: `ABC123XYZ000001`, `DEF456UVW000002`, `GHI789RST000003`

### Dates & Times

- **Use generic dates**: Avoid current/recent dates that could identify trading activity
  - Prefer: `2025-01-15`, `2025-01-16`, `2025-01-20`
  - Avoid: Actual dates of real trades
- **Use generic times**: Round to common hours
  - Example: `10:30:00`, `11:45:00`, `15:30:00`, `16:15:00`
- **Time zones**: Keep accurate (e.g., `US/Eastern`, `UTC`)

## What to Keep Real

These fields should remain realistic and accurate:

### Market Data

- **Symbols**: Keep real ticker symbols (BABA, MES, MNQ, MCL, etc.)
- **Exchanges**: Keep real exchanges (CBOE, CME, NYMEX, NYSE, MEMX, etc.)
- **Security Types**: Keep accurate (OPT, FUT, STK, etc.)
- **Asset Categories**: Keep accurate (OPT, FUT, etc.)
- **Currency**: Keep real (USD, EUR, etc.)

### Trade Details

- **Prices**: Keep realistic price ranges for the security
- **Quantities**: Keep realistic quantities
- **Multipliers**: Keep accurate for contract types
- **Strike prices**: Keep realistic for options
- **Expiration dates**: Keep realistic format

### System & Status Fields

- **Order Types**: Keep real (LMT, MKT, STP, etc.)
- **Actions**: Keep real (BUY, SELL)
- **Status**: Keep real (Filled, Cancelled, etc.)
- **Time in Force**: Keep real (DAY, GTC, etc.)
- **Flags**: Keep accurate (True/False, Y/N)

## Example Patterns

### Before (Example of Data to Anonymize)

```text
accountId: U8675309
conId: 987654321
tradeID: 8888888888
ibExecID: 0000f1a2.b3c4d5e6.01.01
dateTime: 2024-11-18 14:23:17-05:00
```

### After (Anonymized)

```text
accountId: U1234567
conId: 123456789
tradeID: 1000000001
ibExecID: 0000abcd.12345678.01.01
dateTime: 2025-01-15 10:30:00-05:00
```

## Implementation

When generating schema documentation (using `export_dtypes_markdown` or similar):

1. **Never include actual personal data** in sample values
2. **Use sequential generic IDs** for different ID types (use different ranges
   to avoid confusion)
3. **Use generic dates** (prefer January dates, avoid current month)
4. **Preserve data types and formats** exactly
5. **Keep market data realistic** (real symbols, exchanges, prices)
6. **Document null percentages accurately** based on real data structure

## Purpose

This anonymization ensures:

- **Privacy**: No personal trading data exposed
- **Clarity**: Generic patterns easy to understand
- **Realism**: Data structure remains accurate
- **Documentation**: LLM analysis remains effective without real personal data
