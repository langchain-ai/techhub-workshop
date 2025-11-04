"""
Database tools for querying the TechHub e-commerce database.

These tools provide a simple interface for customer support agents to:
- Look up customer order history
- Get detailed information about specific orders
- Query product pricing and availability

Design note: Database connections are configured at the module level rather than
as tool parameters. This follows LangChain best practices where infrastructure
concerns (database paths, API keys, etc.) are managed via static runtime context,
not exposed to the LLM as tool parameters.
"""

import sqlite3
from pathlib import Path

from langchain.tools import ToolRuntime, tool

# Database path - configured at module level (infrastructure concern)
DEFAULT_DB_PATH = Path(__file__).parent.parent / "data" / "structured" / "techhub.db"


@tool
def get_order_status(order_id: str) -> str:
    """Get status, dates, and tracking information for a specific order.

    Args:
        order_id: The order ID (e.g., "ORD-2024-0123")

    Returns:
        Formatted string with order status, dates, tracking number, and total amount.
    """
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT order_id, order_date, status, shipped_date, tracking_number, total_amount
        FROM orders
        WHERE order_id = ?
    """,
        (order_id,),
    )

    result = cursor.fetchone()
    conn.close()

    if not result:
        return f"Order {order_id} not found."

    order_id, order_date, status, shipped_date, tracking_number, total = result

    response = f"Order {order_id}:\n"
    response += f"- Status: {status}\n"
    response += f"- Order Date: {order_date}\n"
    response += f"- Total Amount: ${total:.2f}\n"

    if shipped_date:
        response += f"- Shipped Date: {shipped_date}\n"
    if tracking_number:
        response += f"- Tracking Number: {tracking_number}\n"

    return response


@tool
def get_order_items(order_id: str) -> str:
    """Get list of items in a specific order with product IDs, quantities, and prices.

    Args:
        order_id: The order ID (e.g., "ORD-2024-0123")

    Returns:
        Formatted string with product IDs, quantities, and prices for each item.
        Note: Returns product IDs only - use get_product_info() to get product names.
    """
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id, quantity, price_per_unit
        FROM order_items
        WHERE order_id = ?
    """,
        (order_id,),
    )

    items = cursor.fetchall()
    conn.close()

    if not items:
        return f"No items found for order {order_id}."

    response = f"Items in order {order_id}:\n"
    for product_id, quantity, price in items:
        response += (
            f"- Product ID: {product_id}, Quantity: {quantity}, Price: ${price:.2f}\n"
        )

    return response


@tool
def get_product_info(product_identifier: str) -> str:
    """Get product details by product name or product ID.

    Args:
        product_identifier: Product name (e.g., "MacBook Air") or product ID (e.g., "TECH-LAP-001")

    Returns:
        Formatted string with product name, category, price, and stock status.
    """
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    # Try exact ID match first
    cursor.execute(
        """
        SELECT product_id, name, category, price, in_stock
        FROM products
        WHERE product_id = ?
    """,
        (product_identifier,),
    )

    result = cursor.fetchone()

    # If no exact match, try fuzzy name search
    if not result:
        cursor.execute(
            """
            SELECT product_id, name, category, price, in_stock
            FROM products
            WHERE name LIKE ?
            LIMIT 1
        """,
            (f"%{product_identifier}%",),
        )

        result = cursor.fetchone()

    conn.close()

    if not result:
        return f"Product '{product_identifier}' not found."

    product_id, name, category, price, in_stock = result
    stock_status = "In Stock" if in_stock else "Out of Stock"

    return f"{name} ({product_id})\n- Category: {category}\n- Price: ${price:.2f}\n- Status: {stock_status}"


@tool
def get_customer_orders(runtime: ToolRuntime) -> str:
    """Get recent orders for a verified customer.

    Automatically injects the customer_id from the agent's state into the query
    so you don't need to ask the customer for their ID or email address to use this tool.

    Args:
        runtime: Runtime context (provides access to state)

    Returns:
        Formatted list of recent orders with order ID, date, status, and total.
    """
    # Get customer_id from state (populated by HITL verification in Section 4)
    state_customer_id = runtime.state.get("customer_id")
    if not state_customer_id:
        return "Customer verification required. Please provide your email."

    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT order_id, order_date, status, total_amount
        FROM orders
        WHERE customer_id = ?
        ORDER BY order_date DESC
    """,
        (state_customer_id,),
    )

    orders = cursor.fetchall()
    conn.close()

    if not orders:
        return f"No orders found for customer {state_customer_id}."

    response = "Recent orders:\n"
    for order_id, order_date, status, total in orders:
        response += f"- {order_id}: {order_date}, {status}, ${total:.2f}\n"

    return response
