# DataFrame Schema (Anonymized)

> ⚠️ **Privacy Notice**: All sample values have been anonymized according to [IBKR Sample Data Anonymization Guidelines](../prompts/prompt-ibkr-sample-data.md). Account IDs, transaction IDs, dates, and other personal identifiers have been replaced with generic values. Market data (symbols, exchanges, prices) remains realistic.

## Overview

- **Rows**: 14
- **Columns**: 173
- **Memory Usage**: 0.06 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values |
|--------|-----------|------------|--------|---------------|
| `advancedError` | `object` | 0 | 0.0% | , ,  |
| `conId` | `int64` | 0 | 0.0% | 123456789, 234567890, 345678901 |
| `symbol` | `object` | 0 | 0.0% | CL, USAR, MES |
| `secType` | `object` | 0 | 0.0% | FOP, STK, FUT |
| `exchange` | `object` | 0 | 0.0% | NYMEX, SMART, CME |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `localSymbol` | `object` | 0 | 0.0% | LO5F6 P5500, USAR, MESH6 |
| `tradingClass` | `object` | 0 | 0.0% | LO5, NMS, MES |
| `lastTradeDateOrContractMonth` | `object` | 0 | 0.0% | 20260130, , 20260320 |
| `multiplier` | `object` | 0 | 0.0% | 1000, , 5 |
| `strike` | `float64` | 0 | 0.0% | 55.0, 0.0, 0.0 |
| `right` | `object` | 0 | 0.0% | P, ?, ? |
| `account` | `object` | 0 | 0.0% | U1234567, U1234567, U2345678 |
| `action` | `object` | 0 | 0.0% | BUY, BUY, SELL |
| `activeStartTime` | `object` | 0 | 0.0% | , ,  |
| `activeStopTime` | `object` | 0 | 0.0% | , ,  |
| `adjustableTrailingUnit` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `adjustedOrderType` | `object` | 0 | 0.0% | , ,  |
| `adjustedStopLimitPrice` | `object` | 14 | 100.0% |  |
| `adjustedStopPrice` | `object` | 14 | 100.0% |  |
| `adjustedTrailingAmount` | `object` | 14 | 100.0% |  |
| `advancedErrorOverride` | `object` | 0 | 0.0% | , ,  |
| `algoId` | `object` | 0 | 0.0% | , ,  |
| `algoParams` | `object` | 0 | 0.0% | [], [], [] |
| `algoStrategy` | `object` | 0 | 0.0% | , ,  |
| `allOrNone` | `bool` | 0 | 0.0% | False, False, False |
| `auctionStrategy` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `autoCancelDate` | `object` | 0 | 0.0% | , ,  |
| `autoCancelParent` | `bool` | 0 | 0.0% | False, False, False |
| `auxPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `basisPoints` | `object` | 14 | 100.0% |  |
| `basisPointsType` | `object` | 14 | 100.0% |  |
| `blockOrder` | `bool` | 0 | 0.0% | False, False, False |
| `cashQty` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `clearingAccount` | `object` | 0 | 0.0% | , ,  |
| `clearingIntent` | `object` | 0 | 0.0% | IB, IB, IB |
| `clientId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `competeAgainstBestOffset` | `object` | 14 | 100.0% |  |
| `conditions` | `object` | 0 | 0.0% | [], [], [] |
| `conditionsCancelOrder` | `bool` | 0 | 0.0% | False, False, False |
| `conditionsIgnoreRth` | `bool` | 0 | 0.0% | False, False, False |
| `continuousUpdate` | `bool` | 0 | 0.0% | False, False, False |
| `delta` | `object` | 14 | 100.0% |  |
| `deltaNeutralAuxPrice` | `object` | 14 | 100.0% |  |
| `deltaNeutralClearingAccount` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralClearingIntent` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralConId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `deltaNeutralDesignatedLocation` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralOpenClose` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralOrderType` | `object` | 0 | 0.0% | None, None, None |
| `deltaNeutralSettlingFirm` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralShortSale` | `bool` | 0 | 0.0% | False, False, False |
| `deltaNeutralShortSaleSlot` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `designatedLocation` | `object` | 0 | 0.0% | , ,  |
| `discretionaryAmt` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `discretionaryUpToLimitPrice` | `bool` | 0 | 0.0% | False, False, False |
| `displaySize` | `object` | 14 | 100.0% |  |
| `dontUseAutoPriceForHedge` | `bool` | 0 | 0.0% | True, True, True |
| `duration` | `object` | 14 | 100.0% |  |
| `eTradeOnly` | `bool` | 0 | 0.0% | False, False, False |
| `exemptCode` | `int64` | 0 | 0.0% | -1, -1, -1 |
| `extOperator` | `object` | 0 | 0.0% | , ,  |
| `faGroup` | `object` | 0 | 0.0% | , ,  |
| `faMethod` | `object` | 0 | 0.0% | , ,  |
| `faPercentage` | `object` | 0 | 0.0% | , ,  |
| `faProfile` | `object` | 0 | 0.0% | , ,  |
| `filledQuantity` | `float64` | 0 | 0.0% | 1.0, 100.0, 1.0 |
| `firmQuoteOnly` | `bool` | 0 | 0.0% | False, False, False |
| `goodAfterTime` | `object` | 0 | 0.0% | , ,  |
| `goodTillDate` | `object` | 0 | 0.0% | , ,  |
| `hedgeParam` | `object` | 0 | 0.0% | , ,  |
| `hedgeType` | `object` | 0 | 0.0% | , ,  |
| `hidden` | `bool` | 0 | 0.0% | False, False, False |
| `imbalanceOnly` | `bool` | 0 | 0.0% | False, False, False |
| `isOmsContainer` | `bool` | 0 | 0.0% | False, False, False |
| `isPeggedChangeAmountDecrease` | `bool` | 0 | 0.0% | False, False, False |
| `lmtPrice` | `float64` | 0 | 0.0% | 0.04, 28.96, 6979.5 |
| `lmtPriceOffset` | `object` | 14 | 100.0% |  |
| `manualOrderTime` | `object` | 0 | 0.0% | , ,  |
| `midOffsetAtHalf` | `object` | 14 | 100.0% |  |
| `midOffsetAtWhole` | `object` | 14 | 100.0% |  |
| `mifid2DecisionAlgo` | `object` | 0 | 0.0% | , ,  |
| `mifid2DecisionMaker` | `object` | 0 | 0.0% | , ,  |
| `mifid2ExecutionAlgo` | `object` | 0 | 0.0% | , ,  |
| `mifid2ExecutionTrader` | `object` | 0 | 0.0% | , ,  |
| `minCompeteSize` | `object` | 14 | 100.0% |  |
| `minQty` | `object` | 14 | 100.0% |  |
| `minTradeQty` | `object` | 14 | 100.0% |  |
| `modelCode` | `object` | 0 | 0.0% | , ,  |
| `nbboPriceCap` | `object` | 14 | 100.0% |  |
| `notHeld` | `bool` | 0 | 0.0% | False, False, False |
| `ocaGroup` | `object` | 0 | 0.0% | , ,  |
| `ocaType` | `int64` | 0 | 0.0% | 3, 3, 3 |
| `openClose` | `object` | 0 | 0.0% | , ,  |
| `optOutSmartRouting` | `bool` | 0 | 0.0% | False, False, False |
| `orderComboLegs` | `object` | 0 | 0.0% | [], [], [] |
| `orderId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `orderMiscOptions` | `object` | 0 | 0.0% | [], [], [] |
| `orderRef` | `object` | 0 | 0.0% | , ,  |
| `orderType` | `object` | 0 | 0.0% | LMT, LMT, LMT |
| `origin` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `outsideRth` | `bool` | 0 | 0.0% | False, False, False |
| `overridePercentageConstraints` | `bool` | 0 | 0.0% | False, False, False |
| `parentId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `parentPermId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `peggedChangeAmount` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `percentOffset` | `object` | 14 | 100.0% |  |
| `permId` | `int64` | 0 | 0.0% | 888888888, 999999999, 777777777 |
| `postToAts` | `object` | 14 | 100.0% |  |
| `randomizePrice` | `bool` | 0 | 0.0% | False, False, False |
| `randomizeSize` | `bool` | 0 | 0.0% | False, False, False |
| `refFuturesConId` | `object` | 14 | 100.0% |  |
| `referenceChangeAmount` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `referenceContractId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `referenceExchangeId` | `object` | 0 | 0.0% | , ,  |
| `referencePriceType` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `routeMarketableToBbo` | `bool` | 0 | 0.0% | False, False, False |
| `rule80A` | `object` | 0 | 0.0% | 0, 0, 0 |
| `scaleAutoReset` | `bool` | 0 | 0.0% | False, False, False |
| `scaleInitFillQty` | `object` | 14 | 100.0% |  |
| `scaleInitLevelSize` | `object` | 14 | 100.0% |  |
| `scaleInitPosition` | `object` | 14 | 100.0% |  |
| `scalePriceAdjustInterval` | `object` | 14 | 100.0% |  |
| `scalePriceAdjustValue` | `object` | 14 | 100.0% |  |
| `scalePriceIncrement` | `object` | 14 | 100.0% |  |
| `scaleProfitOffset` | `object` | 14 | 100.0% |  |
| `scaleRandomPercent` | `bool` | 0 | 0.0% | False, False, False |
| `scaleSubsLevelSize` | `object` | 14 | 100.0% |  |
| `scaleTable` | `object` | 0 | 0.0% | , ,  |
| `settlingFirm` | `object` | 0 | 0.0% | , ,  |
| `shareholder` | `object` | 0 | 0.0% | Not an insider or substantial , Not an insider or substan... |
| `shortSaleSlot` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `smartComboRoutingParams` | `object` | 0 | 0.0% | [], [], [] |
| `softDollarTier` | `object` | 0 | 0.0% | SoftDollarTier(name='', val='', SoftDollarTier(name='', v... |
| `solicited` | `bool` | 0 | 0.0% | False, False, False |
| `startingPrice` | `object` | 14 | 100.0% |  |
| `stockRangeLower` | `object` | 14 | 100.0% |  |
| `stockRangeUpper` | `object` | 14 | 100.0% |  |
| `stockRefPrice` | `object` | 14 | 100.0% |  |
| `sweepToFill` | `bool` | 0 | 0.0% | False, False, False |
| `tif` | `object` | 0 | 0.0% | DAY, DAY, DAY |
| `totalQuantity` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `trailStopPrice` | `object` | 14 | 100.0% |  |
| `trailingPercent` | `object` | 14 | 100.0% |  |
| `transmit` | `bool` | 0 | 0.0% | True, True, True |
| `triggerMethod` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `triggerPrice` | `object` | 14 | 100.0% |  |
| `usePriceMgmtAlgo` | `bool` | 0 | 0.0% | False, False, False |
| `volatility` | `object` | 14 | 100.0% |  |
| `volatilityType` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `whatIf` | `bool` | 0 | 0.0% | False, False, False |
| `status` | `object` | 0 | 0.0% | Filled, Filled, Filled |
| `filled` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `remaining` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `avgFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `lastFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `fill_time_direct` | `datetime64[ns, UTC]` | 0 | 0.0% | 2025-01-15 10:30:00+00:00, 2025-01-15 11:45:00+00:00, 202... |
| `fill_execution_id` | `object` | 0 | 0.0% | 0000abcd.12345678.01.01, 0000efgh.23456789.01.01, 0000ijk... |
| `fill_execution_time` | `datetime64[ns, UTC]` | 0 | 0.0% | 2025-01-15 10:30:00+00:00, 2025-01-15 11:45:00+00:00, 202... |
| `fill_shares` | `float64` | 0 | 0.0% | 1.0, 100.0, 1.0 |
| `fill_price` | `float64` | 0 | 0.0% | 0.04, 28.85, 6979.5 |
| `fill_exchange` | `object` | 0 | 0.0% | NYMEX, DARK, CME |
| `fill_side` | `object` | 0 | 0.0% | BOT, BOT, SLD |
| `fill_cumQty` | `float64` | 0 | 0.0% | 1.0, 100.0, 1.0 |
| `fill_avgPrice` | `float64` | 0 | 0.0% | 0.04, 28.85, 6979.5 |
| `fill_commission` | `float64` | 0 | 0.0% | 2.37, 1.0, 0.62 |
| `fill_commissionCurrency` | `object` | 0 | 0.0% | USD, USD, USD |
| `fill_realizedPNL` | `float64` | 0 | 0.0% | 0.0, 0.0, 293.76 |
| `fill_contract_conId` | `float64` | 0 | 0.0% | 123456789.0, 234567890.0, 345678901.0 |
| `log_time` | `datetime64[ns, UTC]` | 0 | 0.0% | 2025-01-15 10:30:00+00:00, 2025-01-15 11:45:00+00:00, 202... |
| `log_status` | `object` | 0 | 0.0% | Filled, Filled, Filled |
| `log_message` | `object` | 0 | 0.0% | Fill 1.0@0.04, Fill 100.0@28.85, Fill 1.0@6979.5 |
| `log_errorCode` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |

## Data Type Summary

- **object**: 102 columns
- **bool**: 29 columns
- **float64**: 21 columns
- **int64**: 18 columns
- **datetime64[ns, UTC]**: 3 columns

## Columns with Missing Data

- `adjustedStopLimitPrice`: 14 nulls (100.0%)
- `adjustedStopPrice`: 14 nulls (100.0%)
- `adjustedTrailingAmount`: 14 nulls (100.0%)
- `basisPoints`: 14 nulls (100.0%)
- `basisPointsType`: 14 nulls (100.0%)
- `competeAgainstBestOffset`: 14 nulls (100.0%)
- `delta`: 14 nulls (100.0%)
- `deltaNeutralAuxPrice`: 14 nulls (100.0%)
- `displaySize`: 14 nulls (100.0%)
- `duration`: 14 nulls (100.0%)
- `lmtPriceOffset`: 14 nulls (100.0%)
- `midOffsetAtHalf`: 14 nulls (100.0%)
- `midOffsetAtWhole`: 14 nulls (100.0%)
- `minCompeteSize`: 14 nulls (100.0%)
- `minQty`: 14 nulls (100.0%)
- `minTradeQty`: 14 nulls (100.0%)
- `nbboPriceCap`: 14 nulls (100.0%)
- `percentOffset`: 14 nulls (100.0%)
- `postToAts`: 14 nulls (100.0%)
- `refFuturesConId`: 14 nulls (100.0%)
- `scaleInitFillQty`: 14 nulls (100.0%)
- `scaleInitLevelSize`: 14 nulls (100.0%)
- `scaleInitPosition`: 14 nulls (100.0%)
- `scalePriceAdjustInterval`: 14 nulls (100.0%)
- `scalePriceAdjustValue`: 14 nulls (100.0%)
- `scalePriceIncrement`: 14 nulls (100.0%)
- `scaleProfitOffset`: 14 nulls (100.0%)
- `scaleSubsLevelSize`: 14 nulls (100.0%)
- `startingPrice`: 14 nulls (100.0%)
- `stockRangeLower`: 14 nulls (100.0%)
- `stockRangeUpper`: 14 nulls (100.0%)
- `stockRefPrice`: 14 nulls (100.0%)
- `trailStopPrice`: 14 nulls (100.0%)
- `trailingPercent`: 14 nulls (100.0%)
- `triggerPrice`: 14 nulls (100.0%)
- `volatility`: 14 nulls (100.0%)

## Anonymization Notes

This schema documentation uses anonymized sample data:

- **Account/Transaction IDs**: Replaced with sequential generic IDs
- **Dates/Times**: Replaced with generic January 2025 dates and round times
- **Personal Identifiers**: All replaced with non-identifying values
- **Market Data**: Preserved real symbols, exchanges, and realistic prices
- **Data Structure**: Exact types, null percentages, and formats maintained

**This documentation is safe to share publicly and with LLMs for schema analysis.**
