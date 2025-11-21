"""
Tests for extract_object_attributes helper function.

This test file uses realistic IBKR order data to verify the generic
attribute extraction works correctly.
"""

import pandas as pd

from ngv_reports_ibkr.expand_contract_columns import (
    UNSET_DOUBLE,
    expand_order_column,
    extract_object_attributes,
)


class MockOrder:
    """
    Simplified version of ib_async Order object.

    Represents a real stock order for Apple (AAPL) with common attributes
    that a Wall Street analyst would see in their trading data.
    """

    def __init__(self, order_id, action, quantity, price=None, order_type="MKT"):
        # Order identifiers
        self.orderId = order_id
        self.permId = order_id * 10  # Permanent ID (typically larger)
        self.parentId = 0
        self.clientId = 1

        # Basic order details
        self.action = action  # "BUY" or "SELL"
        self.orderType = order_type  # "MKT", "LMT", etc.
        self.totalQuantity = quantity
        self.filledQuantity = 0

        # Pricing (use UNSET values when not applicable)
        self.lmtPrice = price if price else UNSET_DOUBLE
        self.auxPrice = UNSET_DOUBLE
        self.trailStopPrice = UNSET_DOUBLE

        # Time in force
        self.tif = "DAY"  # Day order
        self.account = "DU123456"
        self.transmit = True
        self.hidden = False

    def place_order(self):
        """Example method that should be filtered out."""
        return f"Placing order {self.orderId}"


def test_extract_basic_attributes():
    """
    Test extracting basic order attributes without numeric cleaning.

    Real-world scenario: Market order to buy 100 shares of AAPL
    """
    order = MockOrder(order_id=1001, action="BUY", quantity=100)

    data = extract_object_attributes(order, clean_numeric=False)

    # Check that we got the key attributes
    assert data["orderId"] == 1001
    assert data["action"] == "BUY"
    assert data["orderType"] == "MKT"
    assert data["totalQuantity"] == 100
    assert data["account"] == "DU123456"

    # Check that methods are NOT included
    assert "place_order" not in data

    # Check that private attributes are NOT included
    assert "__dict__" not in data
    assert "__class__" not in data


def test_extract_with_numeric_cleaning():
    """
    Test that IBKR's UNSET values get cleaned to None.

    Real-world scenario: Market order where limit price doesn't apply,
    so IBKR sets it to sys.float_info.max (UNSET_DOUBLE)
    """
    order = MockOrder(order_id=1002, action="SELL", quantity=50)

    data = extract_object_attributes(order, clean_numeric=True)

    # UNSET values should be cleaned to None
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
    order = MockOrder(order_id=1003, action="BUY", quantity=200, price=150.25, order_type="LMT")

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
    # Create realistic test data
    orders = [
        MockOrder(order_id=2001, action="BUY", quantity=100),
        None,  # Cancelled or missing order
        MockOrder(order_id=2003, action="SELL", quantity=50, price=155.75, order_type="LMT"),
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
    order = MockOrder(order_id=3001, action="BUY", quantity=75)

    data = extract_object_attributes(order, clean_numeric=True, exclude_attrs=["permId", "clientId", "parentId"])

    # Excluded attributes should not be present
    assert "permId" not in data
    assert "clientId" not in data
    assert "parentId" not in data

    # Other attributes should still be there
    assert "orderId" in data
    assert "action" in data
