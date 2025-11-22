# DataFrame Schema (Anonymized)

> ⚠️ **Privacy Notice**: All sample values have been anonymized according to [IBKR Sample Data Anonymization Guidelines](../prompts/prompt-ibkr-sample-data.md). Account IDs, transaction IDs, dates, and other personal identifiers have been replaced with generic values. Market data (symbols, exchanges, prices) remains realistic.

## Overview

- **Rows**: 1,962
- **Columns**: 72
- **Memory Usage**: 4.99 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values (Anonymized) |
|--------|-----------|------------|--------|---------------------------|
| `accountId` | `object` | 0 | 0.0% | U1234567, U1234568, U1234569 |
| `acctAlias` | `object` | 0 | 0.0% | , ,  |
| `model` | `object` | 0 | 0.0% | , ,  |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `fxRateToBase` | `float64` | 0 | 0.0% | 1.0, 1.0, 1.0 |
| `assetCategory` | `object` | 0 | 0.0% | STK, STK, STK |
| `symbol` | `object` | 0 | 0.0% | BABA, BABA, BABA |
| `description` | `object` | 0 | 0.0% | ALIBABA GROUP HOLDING-SP ADR, ALIBABA GROUP HOLDING-SP AD... |
| `conid` | `int64` | 0 | 0.0% | 123456789, 234567900, 345679011 |
| `securityID` | `object` | 0 | 0.0% | US01609W1027, US01609W1027, US01609W1027 |
| `securityIDType` | `object` | 0 | 0.0% | ISIN, ISIN, ISIN |
| `cusip` | `object` | 0 | 0.0% | 01609W102, 01609W102, 01609W102 |
| `isin` | `object` | 0 | 0.0% | US01609W1027, US01609W1027, US01609W1027 |
| `listingExchange` | `object` | 0 | 0.0% | NYSE, NYSE, NYSE |
| `underlyingConid` | `object` | 0 | 0.0% | 456790122, 567901233, 679012344 |
| `underlyingSymbol` | `object` | 0 | 0.0% | BABA, BABA, BABA |
| `underlyingSecurityID` | `object` | 0 | 0.0% | , ,  |
| `underlyingListingExchange` | `object` | 0 | 0.0% | , ,  |
| `issuer` | `object` | 0 | 0.0% | , ,  |
| `multiplier` | `float64` | 0 | 0.0% | 1.0, 1.0, 1.0 |
| `strike` | `object` | 0 | 0.0% | , ,  |
| `expiry` | `object` | 0 | 0.0% | , ,  |
| `tradeID` | `int64` | 0 | 0.0% | 1000000001, 1000000002, 1000000003 |
| `putCall` | `object` | 0 | 0.0% | , ,  |
| `reportDate` | `object` | 0 | 0.0% | 2025-01-15, 2025-01-16, 2025-01-17 |
| `principalAdjustFactor` | `object` | 0 | 0.0% | , ,  |
| `dateTime` | `datetime64[ns, US/Eastern]` | 0 | 0.0% | 2025-01-18 15:30:00-04:00, 2025-01-19 16:15:00-04:00, 202... |
| `tradeDate` | `object` | 0 | 0.0% | 2025-01-21, 2025-01-22, 2025-01-23 |
| `settleDateTarget` | `object` | 0 | 0.0% | 2025-01-24, 2025-01-25, 2025-01-26 |
| `transactionType` | `object` | 0 | 0.0% | ExchTrade, ExchTrade, ExchTrade |
| `exchange` | `object` | 0 | 0.0% | DARK, DARK, IBDRIPUS |
| `quantity` | `float64` | 0 | 0.0% | 100.0, 25.0, 1.1085 |
| `tradePrice` | `float64` | 0 | 0.0% | 124.8, 124.9088, 107.12 |
| `tradeMoney` | `float64` | 0 | 0.0% | 12480.0, 3122.72, 118.74252 |
| `proceeds` | `float64` | 0 | 0.0% | -12480.0, -3122.72, -118.74252 |
| `taxes` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `ibCommission` | `float64` | 0 | 0.0% | -1.0046, -1.00115, -0.11877245 |
| `ibCommissionCurrency` | `object` | 0 | 0.0% | USD, USD, USD |
| `netCash` | `float64` | 0 | 0.0% | -12481.0046, -3123.72115, -118.86129245 |
| `closePrice` | `float64` | 0 | 0.0% | 125.16, 125.16, 106.72 |
| `openCloseIndicator` | `object` | 0 | 0.0% | O, O, O |
| `notes` | `object` | 0 | 0.0% | IA, IA, R |
| `cost` | `float64` | 0 | 0.0% | 12481.0046, 3123.72115, 118.86129245 |
| `fifoPnlRealized` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `fxPnl` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `mtmPnl` | `float64` | 0 | 0.0% | 36.0, 6.28, -0.4434 |
| `origTradePrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `origTradeDate` | `object` | 0 | 0.0% | , ,  |
| `origTradeID` | `object` | 0 | 0.0% | 1000000004, 1000000005, 1000000006 |
| `origOrderID` | `int64` | 0 | 0.0% | 9000000001, 9000000002, 9000000003 |
| `clearingFirmID` | `object` | 0 | 0.0% | , ,  |
| `transactionID` | `int64` | 0 | 0.0% | 5000000001, 5000000002, 5000000003 |
| `buySell` | `object` | 0 | 0.0% | BUY, BUY, BUY |
| `ibOrderID` | `int64` | 0 | 0.0% | 9000000004, 9000000005, 9000000006 |
| `ibExecID` | `object` | 0 | 0.0% | 0000abcd.12345678.01.01, 0000efgh.12345679.01.01, 0000ijk... |
| `brokerageOrderID` | `object` | 0 | 0.0% | 9000000007, 9000000008, 9000000009 |
| `orderReference` | `object` | 0 | 0.0% | , ,  |
| `volatilityOrderLink` | `object` | 0 | 0.0% | , ,  |
| `exchOrderId` | `object` | 0 | 0.0% | 9000000010, 9000000011, 9000000012 |
| `extExecID` | `object` | 0 | 0.0% | 0000mnop.12345681.01.01, 0000qrst.12345682.01.01, 0000uvw... |
| `orderTime` | `datetime64[ns, US/Eastern]` | 184 | 9.4% | 2025-01-27 14:15:00-04:00, 2025-01-28 15:30:00-04:00, 202... |
| `openDateTime` | `object` | 0 | 0.0% | , ,  |
| `holdingPeriodDateTime` | `object` | 0 | 0.0% | , ,  |
| `whenRealized` | `object` | 0 | 0.0% | , ,  |
| `whenReopened` | `object` | 0 | 0.0% | , ,  |
| `levelOfDetail` | `object` | 0 | 0.0% | EXECUTION, EXECUTION, EXECUTION |
| `changeInPrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `changeInQuantity` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `orderType` | `object` | 0 | 0.0% | LMT, LMT,  |
| `traderID` | `object` | 0 | 0.0% | 1000000007, 1000000008, 1000000009 |
| `isAPIOrder` | `object` | 0 | 0.0% | N, N, N |
| `accruedInt` | `int64` | 0 | 0.0% | 0, 0, 0 |

## Data Type Summary

- **object**: 47 columns
- **float64**: 12 columns
- **int64**: 11 columns
- **datetime64[ns, US/Eastern]**: 2 columns

## Columns with Missing Data

- `orderTime`: 184 nulls (9.4%)

## Anonymization Notes

This schema documentation uses anonymized sample data:

- **Account/Transaction IDs**: Replaced with sequential generic IDs
- **Dates/Times**: Replaced with generic January 2025 dates and round times
- **Personal Identifiers**: All replaced with non-identifying values
- **Market Data**: Preserved real symbols, exchanges, and realistic prices
- **Data Structure**: Exact types, null percentages, and formats maintained

**This documentation is safe to share publicly and with LLMs for schema analysis.**
