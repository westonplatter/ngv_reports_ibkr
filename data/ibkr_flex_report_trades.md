# DataFrame Schema (Anonymized)

> ⚠️ **Privacy Notice**: All sample values have been anonymized according to [IBKR Sample Data Anonymization Guidelines](../prompts/prompt-ibkr-sample-data.md). Account IDs, transaction IDs, dates, and other personal identifiers have been replaced with generic values. Market data (symbols, exchanges, prices) remains realistic.

## Overview

- **Rows**: 222
- **Columns**: 85
- **Memory Usage**: 0.69 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values (Anonymized) |
|--------|-----------|------------|--------|---------------------------|
| `accountId` | `object` | 0 | 0.0% | U1234567, U1234568, U1234569 |
| `acctAlias` | `object` | 0 | 0.0% | , ,  |
| `model` | `object` | 0 | 0.0% | , ,  |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `fxRateToBase` | `float64` | 0 | 0.0% | 1.0, 1.0, 1.0 |
| `assetCategory` | `object` | 0 | 0.0% | OPT, OPT, OPT |
| `symbol` | `object` | 0 | 0.0% | GLD   251231C00404000, GLD   260105C00400000, SLV   26010... |
| `description` | `object` | 0 | 0.0% | GLD 31DEC25 404 C, GLD 05JAN26 400 C, SLV 09JAN26 70 C |
| `conid` | `int64` | 0 | 0.0% | 123456789, 234567900, 345679011 |
| `securityID` | `object` | 0 | 0.0% | , ,  |
| `securityIDType` | `object` | 0 | 0.0% | , ,  |
| `cusip` | `object` | 0 | 0.0% | , ,  |
| `isin` | `object` | 0 | 0.0% | , ,  |
| `listingExchange` | `object` | 0 | 0.0% | CBOE, CBOE, CBOE |
| `underlyingConid` | `object` | 0 | 0.0% | 456790122, 567901233, 679012344 |
| `underlyingSymbol` | `object` | 0 | 0.0% | GLD, GLD, SLV |
| `underlyingSecurityID` | `object` | 0 | 0.0% | US78463V1070, US78463V1070, US46428Q1094 |
| `underlyingListingExchange` | `object` | 0 | 0.0% | ARCA, ARCA, ARCA |
| `issuer` | `object` | 0 | 0.0% | , ,  |
| `multiplier` | `float64` | 0 | 0.0% | 100.0, 100.0, 100.0 |
| `strike` | `object` | 0 | 0.0% | 404, 400, 70 |
| `expiry` | `object` | 0 | 0.0% | 2025-12-31, 2026-01-05, 2026-01-09 |
| `tradeID` | `int64` | 0 | 0.0% | 1000000001, 1000000002, 1000000003 |
| `putCall` | `object` | 0 | 0.0% | C, C, C |
| `reportDate` | `object` | 0 | 0.0% | 2025-01-15, 2025-01-16, 2025-01-17 |
| `principalAdjustFactor` | `object` | 0 | 0.0% | , ,  |
| `dateTime` | `datetime64[ns, America/New_York]` | 0 | 0.0% | 2025-01-18 15:30:00-05:00, 2025-01-19 16:15:00-05:00, 202... |
| `tradeDate` | `object` | 0 | 0.0% | 2025-01-21, 2025-01-22, 2025-01-23 |
| `settleDateTarget` | `object` | 0 | 0.0% | 2025-01-24, 2025-01-25, 2025-01-26 |
| `transactionType` | `object` | 0 | 0.0% | BookTrade, ExchTrade, ExchTrade |
| `exchange` | `object` | 0 | 0.0% | --, GEMINI, CBOE2 |
| `quantity` | `float64` | 0 | 0.0% | 1.0, -1.0, 1.0 |
| `tradePrice` | `float64` | 0 | 0.0% | 0.0, 1.33, 1.72 |
| `tradeMoney` | `float64` | 0 | 0.0% | 0.0, -133.0, 172.0 |
| `proceeds` | `float64` | 0 | 0.0% | 0.0, 133.0, -172.0 |
| `taxes` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `ibCommission` | `float64` | 0 | 0.0% | 0.0, -0.66689, -0.6641 |
| `ibCommissionCurrency` | `object` | 0 | 0.0% | USD, USD, USD |
| `netCash` | `float64` | 0 | 0.0% | 0.0, 132.33311, -172.6641 |
| `closePrice` | `float64` | 0 | 0.0% | 0.0, 1.43, 1.0972 |
| `openCloseIndicator` | `object` | 0 | 0.0% | C, O, C |
| `notes` | `object` | 0 | 0.0% | Ep, ,  |
| `cost` | `float64` | 0 | 0.0% | 177.98311, -132.33311, 298.98061 |
| `fifoPnlRealized` | `float64` | 0 | 0.0% | 177.98311, 0.0, 126.31651 |
| `mtmPnl` | `float64` | 0 | 0.0% | 0.0, -10.0, -62.28 |
| `origTradePrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `origTradeDate` | `object` | 0 | 0.0% | , ,  |
| `origTradeID` | `object` | 0 | 0.0% | 1000000004, 1000000005, 1000000006 |
| `origOrderID` | `int64` | 0 | 0.0% | 9000000001, 9000000002, 9000000003 |
| `clearingFirmID` | `object` | 0 | 0.0% | , ,  |
| `transactionID` | `int64` | 0 | 0.0% | 5000000001, 5000000002, 5000000003 |
| `buySell` | `object` | 0 | 0.0% | BUY, SELL, BUY |
| `ibOrderID` | `int64` | 0 | 0.0% | 9000000004, 9000000005, 9000000006 |
| `ibExecID` | `object` | 0 | 0.0% | 0000abcd.12345678.01.01, 0000efgh.12345679.01.01, 0000ijk... |
| `brokerageOrderID` | `object` | 0 | 0.0% | 9000000007, 9000000008, 9000000009 |
| `orderReference` | `object` | 0 | 0.0% | , ,  |
| `volatilityOrderLink` | `object` | 0 | 0.0% | , 2146127093.0, 194299678.0 |
| `exchOrderId` | `object` | 0 | 0.0% | 9000000010, 9000000011, 9000000012 |
| `extExecID` | `object` | 0 | 0.0% | 0000mnop.12345681.01.01, 0000qrst.12345682.01.01, 0000uvw... |
| `orderTime` | `datetime64[ns, America/New_York]` | 18 | 8.1% | 2025-01-27 14:15:00-05:00, 2025-01-28 15:30:00-05:00, 202... |
| `openDateTime` | `object` | 0 | 0.0% | , ,  |
| `holdingPeriodDateTime` | `object` | 0 | 0.0% | , ,  |
| `whenRealized` | `object` | 0 | 0.0% | , ,  |
| `whenReopened` | `object` | 0 | 0.0% | , ,  |
| `levelOfDetail` | `object` | 0 | 0.0% | EXECUTION, EXECUTION, EXECUTION |
| `changeInPrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `changeInQuantity` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `orderType` | `object` | 0 | 0.0% | , LMT, LMT |
| `traderID` | `object` | 0 | 0.0% | 1000000007, 1000000008, 1000000009 |
| `isAPIOrder` | `object` | 0 | 0.0% | N, N, N |
| `accruedInt` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `subCategory` | `object` | 0 | 0.0% | C, C, C |
| `figi` | `object` | 0 | 0.0% | BBG01Y115941, , BBG01YTJ1ZP5 |
| `issuerCountryCode` | `object` | 0 | 0.0% | , ,  |
| `relatedTradeID` | `object` | 0 | 0.0% | 1000000010, 1000000011, 1000000012 |
| `origTransactionID` | `int64` | 0 | 0.0% | 5000000004, 5000000005, 5000000006 |
| `relatedTransactionID` | `object` | 0 | 0.0% | 5000000007, 5000000008, 5000000009 |
| `rtn` | `object` | 0 | 0.0% | , 1121213, 1567283303158B |
| `initialInvestment` | `object` | 0 | 0.0% | , ,  |
| `positionActionID` | `object` | 0 | 0.0% | 104784610, ,  |
| `serialNumber` | `object` | 0 | 0.0% | , ,  |
| `deliveryType` | `object` | 0 | 0.0% | , ,  |
| `commodityType` | `object` | 0 | 0.0% | , ,  |
| `fineness` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `weight` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |

## Data Type Summary

- **object**: 58 columns
- **float64**: 14 columns
- **int64**: 11 columns
- **datetime64[ns, America/New_York]**: 2 columns

## Columns with Missing Data

- `orderTime`: 18 nulls (8.1%)

## Anonymization Notes

This schema documentation uses anonymized sample data:

- **Account/Transaction IDs**: Replaced with sequential generic IDs
- **Dates/Times**: Replaced with generic January 2025 dates and round times
- **Personal Identifiers**: All replaced with non-identifying values
- **Market Data**: Preserved real symbols, exchanges, and realistic prices
- **Data Structure**: Exact types, null percentages, and formats maintained

**This documentation is safe to share publicly and with LLMs for schema analysis.**
