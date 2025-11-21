# DataFrame Schema

## Overview

- **Rows**: 154
- **Columns**: 71
- **Memory Usage**: 0.39 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values |
|--------|-----------|------------|--------|---------------|
| `accountId` | `object` | 0 | 0.0% | U1234567, U1234567, U1234567 |
| `acctAlias` | `object` | 0 | 0.0% | , ,  |
| `model` | `object` | 0 | 0.0% | , ,  |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `fxRateToBase` | `int64` | 0 | 0.0% | 1, 1, 1 |
| `assetCategory` | `object` | 0 | 0.0% | OPT, OPT, FUT |
| `symbol` | `object` | 0 | 0.0% | BABA  251031C00185000, SMR   251031C00045000, MCLZ5 |
| `description` | `object` | 0 | 0.0% | BABA 31OCT25 185 C, SMR 31OCT25 45 C, MCL DEC25 |
| `conid` | `int64` | 0 | 0.0% | 123456789, 234567890, 345678901 |
| `securityID` | `object` | 0 | 0.0% | , ,  |
| `securityIDType` | `object` | 0 | 0.0% | , ,  |
| `cusip` | `object` | 0 | 0.0% | , ,  |
| `isin` | `object` | 0 | 0.0% | , ,  |
| `listingExchange` | `object` | 0 | 0.0% | CBOE, CBOE, NYMEX |
| `underlyingConid` | `object` | 0 | 0.0% | 111111111, 222222222, 333333333 |
| `underlyingSymbol` | `object` | 0 | 0.0% | BABA, SMR, MCL |
| `underlyingSecurityID` | `object` | 0 | 0.0% | US01609W1027, US67079K1007,  |
| `underlyingListingExchange` | `object` | 0 | 0.0% | NYSE, NYSE,  |
| `issuer` | `object` | 0 | 0.0% | , ,  |
| `multiplier` | `int64` | 0 | 0.0% | 100, 100, 100 |
| `strike` | `object` | 0 | 0.0% | 185, 45,  |
| `expiry` | `object` | 0 | 0.0% | 2025-10-31, 2025-10-31, 2025-11-19 |
| `tradeID` | `int64` | 0 | 0.0% | 1000000001, 1000000002, 1000000003 |
| `putCall` | `object` | 0 | 0.0% | C, C,  |
| `reportDate` | `object` | 0 | 0.0% | 2025-10-21, 2025-10-21, 2025-10-21 |
| `principalAdjustFactor` | `object` | 0 | 0.0% | , ,  |
| `dateTime` | `datetime64[ns, US/Eastern]` | 0 | 0.0% | 2025-01-15 10:30:00-05:00, 2025-01-15 11:45:00-05:00, 202... |
| `tradeDate` | `object` | 0 | 0.0% | 2025-01-15, 2025-01-15, 2025-01-16 |
| `settleDateTarget` | `object` | 0 | 0.0% | 2025-01-16, 2025-01-16, 2025-01-17 |
| `transactionType` | `object` | 0 | 0.0% | ExchTrade, ExchTrade, ExchTrade |
| `exchange` | `object` | 0 | 0.0% | BOX, PSE, NYMEX |
| `quantity` | `float64` | 0 | 0.0% | 1.0, 1.0, -1.0 |
| `tradePrice` | `float64` | 0 | 0.0% | 1.09, 1.42, 56.86 |
| `tradeMoney` | `float64` | 0 | 0.0% | 109.0, 142.0, -5686.0 |
| `proceeds` | `float64` | 0 | 0.0% | -109.0, -142.0, 5686.0 |
| `taxes` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `ibCommission` | `float64` | 0 | 0.0% | -1.0459, -1.0459, -0.77 |
| `ibCommissionCurrency` | `object` | 0 | 0.0% | USD, USD, USD |
| `netCash` | `float64` | 0 | 0.0% | -110.0459, -143.0459, -38.77 |
| `closePrice` | `float64` | 0 | 0.0% | 1.085, 1.0171, 57.24 |
| `openCloseIndicator` | `object` | 0 | 0.0% | C, C, O |
| `notes` | `object` | 0 | 0.0% | , ,  |
| `cost` | `float64` | 0 | 0.0% | 174.30131, 151.94881, -5685.23 |
| `fifoPnlRealized` | `float64` | 0 | 0.0% | 64.25541, 8.90291, 0.0 |
| `mtmPnl` | `float64` | 0 | 0.0% | -0.5, -40.29, -38.0 |
| `origTradePrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `origTradeDate` | `object` | 0 | 0.0% | , ,  |
| `origTradeID` | `object` | 0 | 0.0% | , ,  |
| `origOrderID` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `clearingFirmID` | `object` | 0 | 0.0% | , ,  |
| `transactionID` | `int64` | 0 | 0.0% | 5000000001, 5000000002, 5000000003 |
| `buySell` | `object` | 0 | 0.0% | BUY, BUY, SELL |
| `ibOrderID` | `int64` | 0 | 0.0% | 9000000001, 9000000002, 9000000003 |
| `ibExecID` | `object` | 0 | 0.0% | 0000abcd.12345678.01.01, 0000efgh.23456789.01.01, 0000ijkl... |
| `brokerageOrderID` | `object` | 0 | 0.0% | 00aabbcc.00ddeeff.11223344.000, 00aabbcc.00ddeeff.55667788... |
| `orderReference` | `object` | 0 | 0.0% | , ,  |
| `volatilityOrderLink` | `object` | 0 | 0.0% | , ,  |
| `exchOrderId` | `object` | 0 | 0.0% | N/A, N/A, N/A |
| `extExecID` | `object` | 0 | 0.0% | ABC123XYZ000001, DEF456UVW000002, GHI789RST000003 |
| `orderTime` | `datetime64[ns, US/Eastern]` | 11 | 7.1% | 2025-01-15 10:30:00-05:00, 2025-01-15 11:45:00-05:00, 202... |
| `openDateTime` | `object` | 0 | 0.0% | , ,  |
| `holdingPeriodDateTime` | `object` | 0 | 0.0% | , ,  |
| `whenRealized` | `object` | 0 | 0.0% | , ,  |
| `whenReopened` | `object` | 0 | 0.0% | , ,  |
| `levelOfDetail` | `object` | 0 | 0.0% | EXECUTION, EXECUTION, EXECUTION |
| `changeInPrice` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `changeInQuantity` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `orderType` | `object` | 0 | 0.0% | LMT, LMT, LMT |
| `traderID` | `object` | 0 | 0.0% | , ,  |
| `isAPIOrder` | `object` | 0 | 0.0% | N, N, N |
| `accruedInt` | `int64` | 0 | 0.0% | 0, 0, 0 |

## Data Type Summary

- **object**: 47 columns
- **int64**: 12 columns
- **float64**: 10 columns
- **datetime64[ns, US/Eastern]**: 2 columns

## Columns with Missing Data

- `orderTime`: 11 nulls (7.1%)
