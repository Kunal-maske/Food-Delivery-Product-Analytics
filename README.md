# Food Delivery Product Analytics

This portfolio project demonstrates how a Product Analyst can use PostgreSQL and SQL to answer business questions for a food delivery company. The goal is to explore customer behavior, restaurant performance, and order trends using simple but realistic datasets.

## Business problem

A food delivery company wants to understand:

- Which cities and restaurants generate the most revenue?
- What is the average order value?
- What percentage of orders are cancelled?
- How many customers are ordering more than once?
- Which restaurants perform best by city?
- How much revenue is growing month over month?
- How long does it take between a customer's consecutive orders?

These are common product analytics questions in an interview. The dataset is intentionally simple, but the logic maps directly to real-world business analysis.

## Project structure

- `data/` — sample CSV files generated for the project
- `scripts/generate_sample_data.py` — Python script that creates realistic data
- `sql/schema.sql` — PostgreSQL table definitions
- `sql/load_data.sql` — CSV import commands
- `sql/analytics_queries.sql` — analytical SQL queries with product analysis examples
- `README.md` — setup and interview guidance

## Database schema

### `users`
Stores customer information.

Columns:
- `id` — unique user ID
- `name` — customer name
- `email` — email address
- `city` — city where the customer lives
- `signup_date` — date of sign-up
- `is_active` — whether the account is active

### `restaurants`
Stores restaurant metadata.

Columns:
- `id` — unique restaurant ID
- `name` — restaurant name
- `city` — city in which it operates
- `cuisine` — cuisine type
- `avg_delivery_time_mins` — typical delivery time
- `is_active` — whether restaurant is active

### `orders`
Stores each order placed.

Columns:
- `id` — unique order ID
- `user_id` — customer who placed the order
- `restaurant_id` — restaurant fulfilling the order
- `order_date` — date of order
- `order_time` — time of order
- `status` — completed, cancelled, or refunded
- `subtotal` — pre-discount order amount
- `delivery_fee` — delivery fee charged
- `discount_amount` — discounts applied
- `order_total` — final order value
- `items_count` — count of items in the order
- `city` — order city

### `order_items`
Stores item-level details for each order.

Columns:
- `id` — unique line-item ID
- `order_id` — order reference
- `item_name` — item name
- `quantity` — number of units purchased
- `unit_price` — price per item

## Setup instructions

### 1) Start PostgreSQL
Make sure PostgreSQL is installed and running locally.

### 2) Create the database
```bash
createdb food_delivery_analytics
```

### 3) Create schema
```bash
echo "Create tables..."
psql -d food_delivery_analytics -f sql/schema.sql
```

### 4) Generate sample data
```bash
python scripts/generate_sample_data.py
```

### 5) Load data into PostgreSQL
```bash
psql -d food_delivery_analytics -f sql/load_data.sql
```

### 6) Run analytics queries
```bash
psql -d food_delivery_analytics -f sql/analytics_queries.sql
```

## Key SQL concepts covered

This project intentionally demonstrates the core SQL patterns used in business analysis:

- `JOIN` — connect orders to restaurants and users
- `GROUP BY` — aggregate by city, restaurant, status, or month
- `HAVING` — filter aggregate results such as repeat customers or high-revenue restaurants
- `CTE` — create reusable intermediate results for monthly revenue and growth calculations
- `RANK` and `DENSE_RANK` — rank restaurants within each city
- `ROW_NUMBER` — create order sequence per user
- `LAG` — compare current month or order against the previous value
- `LEAD` — look ahead to the next period

## Suggested interview explanations

### Revenue query
The revenue query uses a `JOIN` between `orders` and `restaurants`, then groups the data by city and restaurant. This helps answer: "Which restaurants and cities are generating the most value?"

### Average order value
AOV is calculated as average `order_total` for only completed orders. This avoids counting cancelled or refunded orders in the metric.

### Cancellation rate
We count cancelled orders and divide by total orders. This is a common product KPI because cancellations often signal friction in the ordering experience.

### Repeat customer analysis
A customer is considered repeat if they have placed at least two orders. This helps measure retention and loyalty.

### Time between orders
Using `LAG`, we compare each order to the previous order for the same user. This helps answer: "How often are users returning, and how long between orders?"

### Monthly growth
A `CTE` calculates monthly revenue, and `LAG` measures month-over-month change. This is a strong product analytics technique for trend analysis.

## Example key findings from the sample data

The generated sample dataset is realistic but synthetic. In a typical run, you may expect to see patterns such as:

- Revenue concentrated in a few top cities and restaurants
- A modest cancellation rate between 5% and 15%
- Repeat customers forming a meaningful share of total orders
- Some restaurants performing consistently better than others within the same city
- Monthly growth fluctuating with seasonality, promotions, or campaign periods

These insights are what you would explain in a Product Analyst interview when presenting SQL output to stakeholders.

## Why this is a strong portfolio project

This project is beginner-friendly because it keeps the logic transparent and easy to explain. It also mirrors real analytics work:

- data modeling with relational tables
- business KPI calculation
- product insights from customer and order data
- use of window functions for trend and ranking analysis

It is the kind of SQL project you can confidently discuss in an interview, especially if asked to explain how you used SQL to answer business questions.
