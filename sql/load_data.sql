-- Load sample data into PostgreSQL from CSV files
-- Run from the project root, or update paths accordingly.

\copy users(id, name, email, city, signup_date, is_active)
FROM 'data/users.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy restaurants(id, name, city, cuisine, avg_delivery_time_mins, is_active)
FROM 'data/restaurants.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy orders(id, user_id, restaurant_id, order_date, order_time, status, subtotal, delivery_fee, discount_amount, order_total, items_count, city)
FROM 'data/orders.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy order_items(id, order_id, item_name, quantity, unit_price)
FROM 'data/order_items.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');
