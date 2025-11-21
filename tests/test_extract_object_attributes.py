"""
Tests for extract_object_attributes helper function.

This test file uses real ib_async Order objects to verify the generic
attribute extraction works correctly with actual IBKR API objects.
"""

import pandas as pd
from ib_async import LimitOrder, MarketOrder

from ngv_reports_ibkr.expand_contract_columns import (
    expand_order_column,
    extract_object_attributes,
)


def test_extract_basic_attributes():
    """
    Test extracting basic order attributes without numeric cleaning.

    Real-world scenario: Market order to buy 100 shares of AAPL
    """
    order = MarketOrder("BUY", 100)
    order.orderId = 1001
    order.account = "DU123456"

    data = extract_object_attributes(order, clean_numeric=False)

    # Check that we got the key attributes
    assert data["orderId"] == 1001
    assert data["action"] == "BUY"
    assert data["orderType"] == "MKT"
    assert data["totalQuantity"] == 100
    assert data["account"] == "DU123456"

    # Check that methods are NOT included (ib_async Order has many methods)
    assert "dict" not in data  # dict() method
    assert "tuple" not in data  # tuple() method

    # Check that private attributes are NOT included
    assert "__dict__" not in data
    assert "__class__" not in data


def test_extract_with_numeric_cleaning():
    """
    Test that IBKR's UNSET values get cleaned to None.

    Real-world scenario: Market order where limit price doesn't apply,
    so IBKR sets it to sys.float_info.max (UNSET_DOUBLE)
    """
    order = MarketOrder("SELL", 50)
    order.orderId = 1002

    data = extract_object_attributes(order, clean_numeric=True)

    # UNSET values should be cleaned to None
    # ib_async sets unused numeric fields to UNSET_DOUBLE by default
    assert data["lmtPrice"] is None
    assert data["auxPrice"] is None
    assert data["trailStopPrice"] is None

    # Regular numeric values should remain
    assert data["orderId"] == 1002
    assert data["totalQuantity"] == 50


def test_extract_limit_order_with_price():
    """
    Test limit order with actual price set.

    Real-world scenario: Limit order to buy AAPL at $150.25
    """
    order = LimitOrder("BUY", 200, 150.25)
    order.orderId = 1003

    data = extract_object_attributes(order, clean_numeric=True)

    assert data["orderType"] == "LMT"
    assert data["lmtPrice"] == 150.25  # Real price should NOT be cleaned
    assert data["auxPrice"] is None  # UNSET value should be None


def test_extract_none_order():
    """
    Test handling of None order object.

    Real-world scenario: Some rows in DataFrame might have no order data
    """
    data = extract_object_attributes(None)

    assert data == {}


def test_expand_order_column_with_dataframe():
    """
    Integration test: Expand multiple orders in a DataFrame.

    Real-world scenario: Analyst has 3 trades to analyze:
    1. Buy 100 AAPL at market
    2. Empty row (cancelled order)
    3. Sell 50 AAPL with limit price
    """
    # Create realistic test data using real ib_async Order objects
    order1 = MarketOrder("BUY", 100)
    order1.orderId = 2001

    order2 = LimitOrder("SELL", 50, 155.75)
    order2.orderId = 2003

    orders = [
        order1,
        None,  # Cancelled or missing order
        order2,
    ]

    df = pd.DataFrame(
        {
            "order": orders,
            "trade_date": ["2024-01-15", "2024-01-16", "2024-01-17"],
        }
    )

    # Expand the order column
    result = expand_order_column(df)

    # Check structure
    assert len(result) == 3
    assert "trade_date" in result.columns
    assert "orderId" in result.columns
    assert "action" in result.columns

    # Check first row (market buy)
    assert result.iloc[0]["orderId"] == 2001
    assert result.iloc[0]["action"] == "BUY"
    assert result.iloc[0]["totalQuantity"] == 100

    # Check second row (None order)
    assert pd.isna(result.iloc[1]["orderId"])

    # Check third row (limit sell)
    assert result.iloc[2]["orderId"] == 2003
    assert result.iloc[2]["action"] == "SELL"
    assert result.iloc[2]["lmtPrice"] == 155.75


def test_exclude_specific_attributes():
    """
    Test excluding specific attributes from extraction.

    Real-world scenario: Analyst wants to exclude certain fields
    for simplified reporting.
    """
    order = MarketOrder("BUY", 75)
    order.orderId = 3001
    order.permId = 30010
    order.clientId = 1
    order.parentId = 0

    data = extract_object_attributes(order, clean_numeric=True, exclude_attrs=["permId", "clientId", "parentId"])

    # Excluded attributes should not be present
    assert "permId" not in data
    assert "clientId" not in data
    assert "parentId" not in data

    # Other attributes should still be there
    assert "orderId" in data
    assert "action" in data
