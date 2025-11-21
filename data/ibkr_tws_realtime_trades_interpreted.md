# DataFrame Schema (Anonymized)

> ⚠️ **Privacy Notice**: All sample values have been anonymized according to [IBKR Sample Data Anonymization Guidelines](../prompts/prompt-ibkr-sample-data.md). Account IDs, transaction IDs, dates, and other personal identifiers have been replaced with generic values. Market data (symbols, exchanges, prices) remains realistic.

## Overview

- **Rows**: 6
- **Columns**: 173
- **Memory Usage**: 0.03 MB

## Column Details

| Column | Data Type | Null Count | Null % | Sample Values (Anonymized) |
|--------|-----------|------------|--------|---------------------------|
| `advancedError` | `object` | 0 | 0.0% | , ,  |
| `conId` | `int64` | 0 | 0.0% | 123456789, 234567900, 345679011 |
| `symbol` | `object` | 0 | 0.0% | MGC, MCL, MGC |
| `secType` | `object` | 0 | 0.0% | FUT, FUT, FUT |
| `exchange` | `object` | 0 | 0.0% | COMEX, NYMEX, COMEX |
| `currency` | `object` | 0 | 0.0% | USD, USD, USD |
| `localSymbol` | `object` | 0 | 0.0% | MGCZ5, MCLF6, MGCZ5 |
| `tradingClass` | `object` | 0 | 0.0% | MGC, MCL, MGC |
| `lastTradeDateOrContractMonth` | `object` | 0 | 0.0% | 20251229, 20251218, 20251229 |
| `multiplier` | `object` | 0 | 0.0% | 10, 100, 10 |
| `strike` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `right` | `object` | 0 | 0.0% | ?, ?, ? |
| `account` | `object` | 0 | 0.0% | U3163206, U3163206, U2888710 |
| `action` | `object` | 0 | 0.0% | SELL, SELL, SELL |
| `activeStartTime` | `object` | 0 | 0.0% | , ,  |
| `activeStopTime` | `object` | 0 | 0.0% | , ,  |
| `adjustableTrailingUnit` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `adjustedOrderType` | `object` | 0 | 0.0% | , ,  |
| `adjustedStopLimitPrice` | `object` | 6 | 100.0% |  |
| `adjustedStopPrice` | `object` | 6 | 100.0% |  |
| `adjustedTrailingAmount` | `object` | 6 | 100.0% |  |
| `advancedErrorOverride` | `object` | 0 | 0.0% | , ,  |
| `algoId` | `object` | 0 | 0.0% | , ,  |
| `algoParams` | `object` | 0 | 0.0% | [], [], [] |
| `algoStrategy` | `object` | 0 | 0.0% | , ,  |
| `allOrNone` | `bool` | 0 | 0.0% | False, False, False |
| `auctionStrategy` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `autoCancelDate` | `object` | 0 | 0.0% | , ,  |
| `autoCancelParent` | `bool` | 0 | 0.0% | False, False, False |
| `auxPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `basisPoints` | `object` | 6 | 100.0% |  |
| `basisPointsType` | `object` | 6 | 100.0% |  |
| `blockOrder` | `bool` | 0 | 0.0% | False, False, False |
| `cashQty` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `clearingAccount` | `object` | 0 | 0.0% | , ,  |
| `clearingIntent` | `object` | 0 | 0.0% | IB, IB, IB |
| `clientId` | `int64` | 0 | 0.0% | 1, 2, 3 |
| `competeAgainstBestOffset` | `object` | 6 | 100.0% |  |
| `conditions` | `object` | 0 | 0.0% | [], [], [] |
| `conditionsCancelOrder` | `bool` | 0 | 0.0% | False, False, False |
| `conditionsIgnoreRth` | `bool` | 0 | 0.0% | False, False, False |
| `continuousUpdate` | `bool` | 0 | 0.0% | False, False, False |
| `delta` | `object` | 6 | 100.0% |  |
| `deltaNeutralAuxPrice` | `object` | 6 | 100.0% |  |
| `deltaNeutralClearingAccount` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralClearingIntent` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralConId` | `int64` | 0 | 0.0% | 456790122, 567901233, 679012344 |
| `deltaNeutralDesignatedLocation` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralOpenClose` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralOrderType` | `object` | 0 | 0.0% | None, None, None |
| `deltaNeutralSettlingFirm` | `object` | 0 | 0.0% | , ,  |
| `deltaNeutralShortSale` | `bool` | 0 | 0.0% | False, False, False |
| `deltaNeutralShortSaleSlot` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `designatedLocation` | `object` | 0 | 0.0% | , ,  |
| `discretionaryAmt` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `discretionaryUpToLimitPrice` | `bool` | 0 | 0.0% | False, False, False |
| `displaySize` | `object` | 6 | 100.0% |  |
| `dontUseAutoPriceForHedge` | `bool` | 0 | 0.0% | True, True, True |
| `duration` | `object` | 6 | 100.0% |  |
| `eTradeOnly` | `bool` | 0 | 0.0% | False, False, False |
| `exemptCode` | `int64` | 0 | 0.0% | -1, -1, -1 |
| `extOperator` | `object` | 0 | 0.0% | , ,  |
| `faGroup` | `object` | 0 | 0.0% | , ,  |
| `faMethod` | `object` | 0 | 0.0% | , ,  |
| `faPercentage` | `object` | 0 | 0.0% | , ,  |
| `faProfile` | `object` | 0 | 0.0% | , ,  |
| `filledQuantity` | `float64` | 0 | 0.0% | 1.0, 0.0, 2.0 |
| `firmQuoteOnly` | `bool` | 0 | 0.0% | False, False, False |
| `goodAfterTime` | `object` | 0 | 0.0% | , ,  |
| `goodTillDate` | `object` | 0 | 0.0% | , ,  |
| `hedgeParam` | `object` | 0 | 0.0% | , ,  |
| `hedgeType` | `object` | 0 | 0.0% | , ,  |
| `hidden` | `bool` | 0 | 0.0% | False, False, False |
| `imbalanceOnly` | `bool` | 0 | 0.0% | False, False, False |
| `isOmsContainer` | `bool` | 0 | 0.0% | False, False, False |
| `isPeggedChangeAmountDecrease` | `bool` | 0 | 0.0% | False, False, False |
| `lmtPrice` | `float64` | 0 | 0.0% | 4049.5, 58.76, 4066.4 |
| `lmtPriceOffset` | `object` | 6 | 100.0% |  |
| `manualOrderTime` | `object` | 0 | 0.0% | , ,  |
| `midOffsetAtHalf` | `object` | 6 | 100.0% |  |
| `midOffsetAtWhole` | `object` | 6 | 100.0% |  |
| `mifid2DecisionAlgo` | `object` | 0 | 0.0% | , ,  |
| `mifid2DecisionMaker` | `object` | 0 | 0.0% | , ,  |
| `mifid2ExecutionAlgo` | `object` | 0 | 0.0% | 0000abcd.12345678.01.01, 0000efgh.12345679.01.01, 0000ijk... |
| `mifid2ExecutionTrader` | `object` | 0 | 0.0% | 1000000001, 1000000002, 1000000003 |
| `minCompeteSize` | `object` | 6 | 100.0% |  |
| `minQty` | `object` | 6 | 100.0% |  |
| `minTradeQty` | `object` | 6 | 100.0% |  |
| `modelCode` | `object` | 0 | 0.0% | , ,  |
| `nbboPriceCap` | `object` | 6 | 100.0% |  |
| `notHeld` | `bool` | 0 | 0.0% | False, False, False |
| `ocaGroup` | `object` | 0 | 0.0% | , ,  |
| `ocaType` | `int64` | 0 | 0.0% | 3, 3, 3 |
| `openClose` | `object` | 0 | 0.0% | , ,  |
| `optOutSmartRouting` | `bool` | 0 | 0.0% | False, False, False |
| `orderComboLegs` | `object` | 0 | 0.0% | [], [], [] |
| `orderId` | `int64` | 0 | 0.0% | 9000000001, 9000000002, 9000000003 |
| `orderMiscOptions` | `object` | 0 | 0.0% | [], [], [] |
| `orderRef` | `object` | 0 | 0.0% | , ,  |
| `orderType` | `object` | 0 | 0.0% | LMT, LMT, LMT |
| `origin` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `outsideRth` | `bool` | 0 | 0.0% | False, False, False |
| `overridePercentageConstraints` | `bool` | 0 | 0.0% | False, False, False |
| `parentId` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `parentPermId` | `int64` | 0 | 0.0% | 8888888, 9999999, 11111110 |
| `peggedChangeAmount` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `percentOffset` | `object` | 6 | 100.0% |  |
| `permId` | `int64` | 0 | 0.0% | 12222221, 13333332, 14444443 |
| `postToAts` | `object` | 6 | 100.0% |  |
| `randomizePrice` | `bool` | 0 | 0.0% | False, False, False |
| `randomizeSize` | `bool` | 0 | 0.0% | False, False, False |
| `refFuturesConId` | `object` | 6 | 100.0% |  |
| `referenceChangeAmount` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `referenceContractId` | `int64` | 0 | 0.0% | 790123455, 901234566, 1012345677 |
| `referenceExchangeId` | `object` | 0 | 0.0% | , ,  |
| `referencePriceType` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `routeMarketableToBbo` | `bool` | 0 | 0.0% | False, False, False |
| `rule80A` | `object` | 0 | 0.0% | 0, 0, 0 |
| `scaleAutoReset` | `bool` | 0 | 0.0% | False, False, False |
| `scaleInitFillQty` | `object` | 6 | 100.0% |  |
| `scaleInitLevelSize` | `object` | 6 | 100.0% |  |
| `scaleInitPosition` | `object` | 6 | 100.0% |  |
| `scalePriceAdjustInterval` | `object` | 6 | 100.0% |  |
| `scalePriceAdjustValue` | `object` | 6 | 100.0% |  |
| `scalePriceIncrement` | `object` | 6 | 100.0% |  |
| `scaleProfitOffset` | `object` | 6 | 100.0% |  |
| `scaleRandomPercent` | `bool` | 0 | 0.0% | False, False, False |
| `scaleSubsLevelSize` | `object` | 6 | 100.0% |  |
| `scaleTable` | `object` | 0 | 0.0% | , ,  |
| `settlingFirm` | `object` | 0 | 0.0% | , ,  |
| `shareholder` | `object` | 0 | 0.0% | Not an insider or substantial , Not an insider or substan... |
| `shortSaleSlot` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `smartComboRoutingParams` | `object` | 0 | 0.0% | [], [], [] |
| `softDollarTier` | `object` | 0 | 0.0% | SoftDollarTier(name='', val='', SoftDollarTier(name='', v... |
| `solicited` | `bool` | 0 | 0.0% | False, False, False |
| `startingPrice` | `object` | 6 | 100.0% |  |
| `stockRangeLower` | `object` | 6 | 100.0% |  |
| `stockRangeUpper` | `object` | 6 | 100.0% |  |
| `stockRefPrice` | `object` | 6 | 100.0% |  |
| `sweepToFill` | `bool` | 0 | 0.0% | False, False, False |
| `tif` | `object` | 0 | 0.0% | GTC, GTC, DAY |
| `totalQuantity` | `float64` | 0 | 0.0% | 0.0, 1.0, 0.0 |
| `trailStopPrice` | `object` | 6 | 100.0% |  |
| `trailingPercent` | `object` | 6 | 100.0% |  |
| `transmit` | `bool` | 0 | 0.0% | True, True, True |
| `triggerMethod` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `triggerPrice` | `object` | 6 | 100.0% |  |
| `usePriceMgmtAlgo` | `bool` | 0 | 0.0% | False, False, False |
| `volatility` | `object` | 6 | 100.0% |  |
| `volatilityType` | `int64` | 0 | 0.0% | 0, 0, 0 |
| `whatIf` | `bool` | 0 | 0.0% | False, False, False |
| `status` | `object` | 0 | 0.0% | Filled, Cancelled, Filled |
| `filled` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `remaining` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `avgFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `lastFillPrice` | `float64` | 0 | 0.0% | 0.0, 0.0, 0.0 |
| `fill_time_direct` | `datetime64[ns, UTC]` | 1 | 16.7% | 2025-01-15 10:30:00+00:00, 2025-01-16 11:45:00+00:00, 202... |
| `fill_execution_id` | `object` | 1 | 16.7% | 0000mnop.12345681.01.01, 0000qrst.12345682.01.01, 0000uvw... |
| `fill_execution_time` | `datetime64[ns, UTC]` | 1 | 16.7% | 2025-01-18 15:30:00+00:00, 2025-01-19 16:15:00+00:00, 202... |
| `fill_shares` | `float64` | 1 | 16.7% | 1.0, 2.0, 1.0 |
| `fill_price` | `float64` | 1 | 16.7% | 4049.5, 4066.4, 58.08 |
| `fill_exchange` | `object` | 1 | 16.7% | COMEX, COMEX, NYMEX |
| `fill_side` | `object` | 1 | 16.7% | SLD, SLD, SLD |
| `fill_cumQty` | `float64` | 1 | 16.7% | 1.0, 2.0, 1.0 |
| `fill_avgPrice` | `float64` | 1 | 16.7% | 4049.5, 4066.4, 58.08 |
| `fill_commission` | `float64` | 1 | 16.7% | 0.87, 1.74, 0.77 |
| `fill_commissionCurrency` | `object` | 1 | 16.7% | USD, USD, USD |
| `fill_realizedPNL` | `float64` | 1 | 16.7% | 80.26, 166.52, -28.54 |
| `fill_contract_conId` | `float64` | 1 | 16.7% | 1123456788, 1234567899, 1345679010 |
| `log_time` | `datetime64[ns, UTC]` | 1 | 16.7% | 2025-01-21 11:45:00+00:00, 2025-01-22 14:15:00+00:00, 202... |
| `log_status` | `object` | 1 | 16.7% | Filled, Filled, Filled |
| `log_message` | `object` | 1 | 16.7% | Fill 1.0@4049.5, Fill 2.0@4066.4, Fill 1.0@58.08 |
| `log_errorCode` | `float64` | 1 | 16.7% | 0.0, 0.0, 0.0 |

## Data Type Summary

- **object**: 102 columns
- **bool**: 29 columns
- **float64**: 21 columns
- **int64**: 18 columns
- **datetime64[ns, UTC]**: 3 columns

## Columns with Missing Data

- `adjustedStopLimitPrice`: 6 nulls (100.0%)
- `adjustedStopPrice`: 6 nulls (100.0%)
- `adjustedTrailingAmount`: 6 nulls (100.0%)
- `basisPoints`: 6 nulls (100.0%)
- `basisPointsType`: 6 nulls (100.0%)
- `competeAgainstBestOffset`: 6 nulls (100.0%)
- `delta`: 6 nulls (100.0%)
- `deltaNeutralAuxPrice`: 6 nulls (100.0%)
- `displaySize`: 6 nulls (100.0%)
- `duration`: 6 nulls (100.0%)
- `lmtPriceOffset`: 6 nulls (100.0%)
- `midOffsetAtHalf`: 6 nulls (100.0%)
- `midOffsetAtWhole`: 6 nulls (100.0%)
- `minCompeteSize`: 6 nulls (100.0%)
- `minQty`: 6 nulls (100.0%)
- `minTradeQty`: 6 nulls (100.0%)
- `nbboPriceCap`: 6 nulls (100.0%)
- `percentOffset`: 6 nulls (100.0%)
- `postToAts`: 6 nulls (100.0%)
- `refFuturesConId`: 6 nulls (100.0%)
- `scaleInitFillQty`: 6 nulls (100.0%)
- `scaleInitLevelSize`: 6 nulls (100.0%)
- `scaleInitPosition`: 6 nulls (100.0%)
- `scalePriceAdjustInterval`: 6 nulls (100.0%)
- `scalePriceAdjustValue`: 6 nulls (100.0%)
- `scalePriceIncrement`: 6 nulls (100.0%)
- `scaleProfitOffset`: 6 nulls (100.0%)
- `scaleSubsLevelSize`: 6 nulls (100.0%)
- `startingPrice`: 6 nulls (100.0%)
- `stockRangeLower`: 6 nulls (100.0%)
- `stockRangeUpper`: 6 nulls (100.0%)
- `stockRefPrice`: 6 nulls (100.0%)
- `trailStopPrice`: 6 nulls (100.0%)
- `trailingPercent`: 6 nulls (100.0%)
- `triggerPrice`: 6 nulls (100.0%)
- `volatility`: 6 nulls (100.0%)
- `fill_time_direct`: 1 nulls (16.7%)
- `fill_execution_id`: 1 nulls (16.7%)
- `fill_execution_time`: 1 nulls (16.7%)
- `fill_shares`: 1 nulls (16.7%)
- `fill_price`: 1 nulls (16.7%)
- `fill_exchange`: 1 nulls (16.7%)
- `fill_side`: 1 nulls (16.7%)
- `fill_cumQty`: 1 nulls (16.7%)
- `fill_avgPrice`: 1 nulls (16.7%)
- `fill_commission`: 1 nulls (16.7%)
- `fill_commissionCurrency`: 1 nulls (16.7%)
- `fill_realizedPNL`: 1 nulls (16.7%)
- `fill_contract_conId`: 1 nulls (16.7%)
- `log_time`: 1 nulls (16.7%)
- `log_status`: 1 nulls (16.7%)
- `log_message`: 1 nulls (16.7%)
- `log_errorCode`: 1 nulls (16.7%)

## Anonymization Notes

This schema documentation uses anonymized sample data:

- **Account/Transaction IDs**: Replaced with sequential generic IDs
- **Dates/Times**: Replaced with generic January 2025 dates and round times
- **Personal Identifiers**: All replaced with non-identifying values
- **Market Data**: Preserved real symbols, exchanges, and realistic prices
- **Data Structure**: Exact types, null percentages, and formats maintained

**This documentation is safe to share publicly and with LLMs for schema analysis.**
