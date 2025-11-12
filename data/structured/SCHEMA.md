# TechHub Database Schema

**Database:** `techhub.db` (SQLite 3, 156 KB)  
**Purpose:** E-commerce customer support system for workshop scenarios  
**Records:** 50 customers, 25 products, 250 orders, 439 order items

## Tables Overview

```
customers (50)
    ↓ 1:N
orders (250)
    ↓ 1:N
order_items (439)
    ↓ N:1
products (25)
```

---

## 1. customers

Customer account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `customer_id` | TEXT | PRIMARY KEY | Format: `CUST-###` |
| `email` | TEXT | UNIQUE, NOT NULL | Used for verification |
| `name` | TEXT | NOT NULL | Customer's full name |
| `phone` | TEXT | | Format: `###-###-####` |
| `city` | TEXT | NOT NULL | Customer's city |
| `state` | TEXT | NOT NULL | 2-letter US state code |
| `segment` | TEXT | NOT NULL, CHECK | `'Consumer'`, `'Corporate'`, `'Home Office'` |

**Index:** `idx_customers_email` on `email`

**Distribution:**
- Consumer: 40 (80%) - @gmail.com, @yahoo.com, @icloud.com
- Corporate: 8 (16%) - company domain emails
- Home Office: 2 (4%)

---

## 2. products

Product catalog with pricing and availability.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `product_id` | TEXT | PRIMARY KEY | Format: `TECH-XXX-###` |
| `name` | TEXT | NOT NULL | Product name with specs |
| `category` | TEXT | NOT NULL, CHECK | `'Laptops'`, `'Monitors'`, `'Keyboards'`, `'Audio'`, `'Accessories'` |
| `price` | REAL | NOT NULL, CHECK > 0 | Current price in USD |
| `in_stock` | INTEGER | NOT NULL, CHECK IN (0, 1) | 1 = in stock, 0 = out of stock |

**Index:** `idx_products_category` on `category`

**Categories:**
- Laptops (5): $899 - $1,999
- Monitors (4): $199 - $599
- Keyboards/Mice (6): $39 - $149
- Audio (5): $79 - $399
- Accessories (5): $19 - $79

---

## 3. orders

Order records tracking purchases over time.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `order_id` | TEXT | PRIMARY KEY | Format: `ORD-YYYY-####` |
| `customer_id` | TEXT | NOT NULL, FOREIGN KEY | References `customers.customer_id` |
| `order_date` | DATE | NOT NULL | Format: `YYYY-MM-DD` |
| `status` | TEXT | NOT NULL, CHECK | `'Processing'`, `'Shipped'`, `'Delivered'`, `'Cancelled'` |
| `shipped_date` | DATE | | NULL if not shipped |
| `tracking_number` | TEXT | | Format: `1Z999AA1XXXXXXXX`, NULL if not shipped |
| `total_amount` | REAL | NOT NULL, CHECK >= 0 | Sum of all line items |

**Indexes:**
- `idx_orders_customer` on `customer_id`
- `idx_orders_date` on `order_date`
- `idx_orders_status` on `status`

**Status Distribution:**
- Delivered: 200 (80%)
- Shipped: 30 (12%)
- Processing: 17 (7%)
- Cancelled: 3 (1%)

**Date Range:** October 2023 - October 2025

**Key Rules:**
- `shipped_date` >= `order_date` when not NULL
- Processing/Cancelled orders have NULL `shipped_date` and `tracking_number`
- Cancelled orders have `total_amount` = 0 and no items

---

## 4. order_items

Line items for each order.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `order_item_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Auto-generated ID |
| `order_id` | TEXT | NOT NULL, FOREIGN KEY | References `orders.order_id` |
| `product_id` | TEXT | NOT NULL, FOREIGN KEY | References `products.product_id` |
| `quantity` | INTEGER | NOT NULL, CHECK > 0 | Typically 1-5 |
| `price_per_unit` | REAL | NOT NULL, CHECK > 0 | Price at time of order |

**Indexes:**
- `idx_order_items_order` on `order_id`
- `idx_order_items_product` on `product_id`

**Key Rules:**
- Sum of (`quantity` × `price_per_unit`) = `orders.total_amount`
- `price_per_unit` within ±5% of current `products.price`
- Cancelled orders have NO items

---

## Common Queries

### Customer Verification (HITL)
```sql
SELECT customer_id, name, email, segment
FROM customers 
WHERE email = 'sarah.chen@gmail.com';
```

### Order History
```sql
SELECT order_id, order_date, status, tracking_number, total_amount
FROM orders 
WHERE customer_id = 'CUST-001'
ORDER BY order_date DESC;
```

### Order Details
```sql
SELECT 
    o.order_id,
    o.status,
    p.name as product_name,
    oi.quantity,
    oi.price_per_unit,
    (oi.quantity * oi.price_per_unit) as line_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_id = 'ORD-2024-0123';
```

### Product Availability
```sql
SELECT product_id, name, price
FROM products 
WHERE category = 'Laptops' 
AND in_stock = 1
ORDER BY price;
```

### Customer Purchase History
```sql
SELECT DISTINCT
    p.name,
    p.category,
    o.order_date
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.customer_id = 'CUST-001'
AND o.status != 'Cancelled'
ORDER BY o.order_date DESC;
```

### Revenue by Category
```sql
SELECT 
    p.category,
    COUNT(DISTINCT oi.order_id) as num_orders,
    SUM(oi.quantity) as units_sold,
    SUM(oi.quantity * oi.price_per_unit) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'Cancelled'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

---

## Key Constraints

**Foreign Keys:**
- `orders.customer_id` → `customers.customer_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`

**Invariants:**
1. No orphaned records (all foreign keys valid)
2. Date consistency: `shipped_date` >= `order_date`
3. Financial accuracy: order totals match line items
4. Cancelled orders: zero total, no items
5. Price bounds: items within ±5% of product price

**Data Quality:**
- Zero foreign key violations
- Zero date logic errors
- 100% order total accuracy
- All queries execute in <1ms

---

## Query Tips

**For SQL Agents:**
- Use email to look up `customer_id` before querying orders
- Filter out `status = 'Cancelled'` for revenue analysis
- Check for NULL in `shipped_date` and `tracking_number`
- Use explicit JOINs for clarity
- Apply ROUND() for financial calculations

**ID Formats:**
- Customer IDs: `CUST-###`
- Order IDs: `ORD-YYYY-####`
- Product IDs: `TECH-XXX-###`

**Date Functions:**
- Dates stored as `YYYY-MM-DD`
- Use `julianday()` for date arithmetic

---

## Additional Resources

**Data Generation:** `../data_generation/README.md`  
**Document Corpus:** `../documents/DOCUMENTS_OVERVIEW.md`
