"""
SchemaSay Services — Mock AI Generator

Simulates realistic, clean offline SQL query translations.
Provides realistic syntax structures corresponding to seeded suggestions.
"""

import time

def generate_sql(prompt: str) -> str:
    """
    Simulates AI translation delay and returns realistic formatted SQL.
    Supports keywords like 'sales', 'churn', 'customer', 'stock', and 'inventory'.
    """
    # Simulate API roundtrip delay (1.0 second)
    time.sleep(1.0)
    
    prompt_lower = prompt.lower()
    
    if "sales" in prompt_lower or "revenue" in prompt_lower:
        return """-- Calculated Monthly Revenue Trends
SELECT 
    DATE_TRUNC('month', order_date) AS sales_month,
    SUM(total_amount) AS monthly_revenue,
    COUNT(order_id) AS total_orders
FROM orders
WHERE order_status = 'COMPLETED'
  AND order_date >= NOW() - INTERVAL '1 year'
GROUP BY 1
ORDER BY 1 DESC;"""

    elif "customer" in prompt_lower or "churn" in prompt_lower:
        return """-- Segmented Customer Retention & Churn Analysis
WITH customer_purchases AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_purchase_date
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.first_name,
    c.email,
    cp.last_purchase_date
FROM customers c
JOIN customer_purchases cp ON c.customer_id = cp.customer_id
WHERE cp.last_purchase_date < NOW() - INTERVAL '90 days'
ORDER BY cp.last_purchase_date ASC
LIMIT 10;"""

    elif "stock" in prompt_lower or "inventory" in prompt_lower or "product" in prompt_lower:
        return """-- Low Stock Level Alerts (Threshold < 20 units)
SELECT 
    product_id,
    product_name,
    category,
    units_in_stock,
    unit_price
FROM products
WHERE units_in_stock < 20
  AND is_active = TRUE
ORDER BY units_in_stock ASC;"""

    else:
        # Default formatted SQL statement fallback
        return f"""-- Query generated for prompt: "{prompt}"
SELECT 
    id,
    created_at,
    name,
    status
FROM data_records
WHERE status = 'ACTIVE'
ORDER BY created_at DESC
LIMIT 100;"""
