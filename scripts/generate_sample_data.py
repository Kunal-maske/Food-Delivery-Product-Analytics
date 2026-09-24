from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

CITIES = [
    "New York",
    "Chicago",
    "Boston",
    "Seattle",
    "Austin",
    "Miami",
    "San Francisco",
    "Denver",
    "Atlanta",
    "Los Angeles",
]

CUISINES = [
    "Italian",
    "Indian",
    "Mexican",
    "Japanese",
    "American",
    "Chinese",
    "Thai",
    "Mediterranean",
    "Vietnamese",
    "Burgers",
]

FIRST_NAMES = [
    "Ava", "Lucas", "Olivia", "Noah", "Emma", "Liam", "Sophia", "Mason", "Mia", "Ethan",
    "Isabella", "James", "Charlotte", "Benjamin", "Amelia", "Henry", "Harper", "Alexander",
    "Ella", "Daniel", "Grace", "Michael", "Chloe", "Jack", "Lily", "Leo", "Scarlett", "Owen",
    "Nora", "Samuel", "Zoe", "David", "Hannah", "William", "Layla", "Joseph", "Aria", "Gabriel",
    "Stella", "Christopher", "Paisley", "John", "Ruby", "Nathan", "Avery", "Elijah", "Hazel",
    "Isaac", "Bella", "Joshua", "Aurora", "Andrew", "Violet", "Ryan", "Skylar", "Nathaniel", "Diana"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Clark", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
    "Carter", "Mitchell", "Perez", "Campbell", "Torres", "Powell", "Flores", "Russell", "Brooks",
    "Coleman", "Foster", "Murphy", "Price", "Long", "Butler", "Simmons", "Ward", "Barnes", "Ross"
]

RESTAURANT_NAMES = {
    "New York": ["Brooklyn Bites", "Upper East Eats", "Manhattan Masti", "Hudson Grill", "Empire Noodles"],
    "Chicago": ["Windy City Wraps", "Loop Pizzeria", "Lakefront Kitchen", "Café Northside", "Deep Dish District"],
    "Boston": ["Beacon Bowls", "North End Naan", "Harbor Kebabs", "Copley Cravings", "Boston Bistro"],
    "Seattle": ["Pike Place Grill", "Rain City Ramen", "Space Needle Sushi", "Mariner Meals", "Market Street Tacos"],
    "Austin": ["South Congress Pizza", "Live Oak Tacos", "Hill Country Grill", "Luna Burritos", "Texas Table"],
    "Miami": ["Ocean View Cuban", "Little Havana Fresh", "Sunset Sushi", "Bayside Burgers", "Coral Kitchen"],
    "San Francisco": ["Bayview Bites", "Golden Gate Grill", "Mission Miso", "Cable Car Curry", "Sourdough Social"],
    "Denver": ["Rocky Mountain BBQ", "Peak Peri Peri", "Union Station Wok", "Highland Harvest", "Summit Sandwiches"],
    "Atlanta": ["Peachtree Pizza", "Midtown Momo", "Skyline Samosa", "Beltline Burgers", "Southern Spice"],
    "Los Angeles": ["Sunset Sushi Club", "Westside Waffles", "Pacific Pasta", "Melrose Grill", "Angeleno Tacos"],
}

MENU_ITEMS = {
    "Italian": ["Margherita Pizza", "Pesto Pasta", "Lasagna", "Caprese Salad", "Garlic Bread"],
    "Indian": ["Butter Chicken", "Paneer Tikka", "Biryani", "Masala Dosa", "Chana Masala"],
    "Mexican": ["Burrito Bowl", "Tacos", "Quesadilla", "Guacamole Chips", "Chicken Enchiladas"],
    "Japanese": ["Salmon Roll", "Teriyaki Bowl", "Sushi Combo", "Miso Soup", "Tempura Udon"],
    "American": ["Classic Burger", "Chicken Sandwich", "Loaded Fries", "Caesar Salad", "BBQ Wings"],
    "Chinese": ["Kung Pao Chicken", "Veggie Dumplings", "Fried Rice", "General Tso Bowl", "Spring Rolls"],
    "Thai": ["Pad Thai", "Green Curry", "Tom Yum Soup", "Satay Skewers", "Thai Basil Noodles"],
    "Mediterranean": ["Falafel Wrap", "Hummus Platter", "Greek Bowl", "Shawarma Plate", "Cucumber Salad"],
    "Vietnamese": ["Pho Bowl", "Banh Mi", "Spring Rolls", "Vietnamese Iced Coffee", "Rice Noodles"],
    "Burgers": ["Cheeseburger", "Smash Burger", "Loaded Burger", "Onion Rings", "Chicken Burger"],
}


def random_date(start, end):
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def generate_users(count: int = 350):
    users = []
    for user_id in range(1, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city = random.choice(CITIES)
        signup_date = random_date(datetime(2022, 1, 1), datetime(2025, 8, 1))
        email = f"{first_name.lower()}.{last_name.lower()}{user_id}@example.com"
        is_active = random.choice([True, True, True, False])
        users.append(
            {
                "id": user_id,
                "name": f"{first_name} {last_name}",
                "email": email,
                "city": city,
                "signup_date": signup_date.strftime("%Y-%m-%d"),
                "is_active": "true" if is_active else "false",
            }
        )
    return users


def generate_restaurants():
    restaurants = []
    restaurant_id = 1
    for city in CITIES:
        for name in RESTAURANT_NAMES[city]:
            cuisine = random.choice(CUISINES)
            avg_delivery_time = random.randint(18, 42)
            is_active = random.choice([True, True, True, False])
            restaurants.append(
                {
                    "id": restaurant_id,
                    "name": name,
                    "city": city,
                    "cuisine": cuisine,
                    "avg_delivery_time_mins": avg_delivery_time,
                    "is_active": "true" if is_active else "false",
                }
            )
            restaurant_id += 1
    return restaurants


def generate_orders(users, restaurants, completed_orders_target: int = 1800):
    orders = []
    order_id = 1
    completed = 0
    while completed < completed_orders_target:
        user_id = random.randint(1, len(users))
        restaurant = random.choice(restaurants)
        restaurant_id = restaurant["id"]
        order_date = random_date(datetime(2023, 1, 1), datetime(2025, 8, 31))
        order_time = datetime.strptime(
            f"{random.randint(10, 23):02d}:{random.randint(0, 59):02d}:00",
            "%H:%M:%S",
        )
        status = random.choices(
            ["completed", "cancelled", "refunded"],
            weights=[80, 12, 8],
            k=1,
        )[0]
        if status == "completed":
            subtotal = round(random.uniform(18.00, 92.00), 2)
            delivery_fee = round(random.uniform(2.50, 7.50), 2)
            discount_amount = round(random.uniform(0.00, 12.00), 2)
            order_total = round(subtotal + delivery_fee - discount_amount, 2)
            items_count = random.randint(1, 6)
            completed += 1
        else:
            subtotal = 0.00
            delivery_fee = 0.00
            discount_amount = 0.00
            order_total = 0.00
            items_count = 0

        orders.append(
            {
                "id": order_id,
                "user_id": user_id,
                "restaurant_id": restaurant_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "order_time": order_time.strftime("%H:%M:%S"),
                "status": status,
                "subtotal": f"{subtotal:.2f}",
                "delivery_fee": f"{delivery_fee:.2f}",
                "discount_amount": f"{discount_amount:.2f}",
                "order_total": f"{order_total:.2f}",
                "items_count": items_count,
                "city": restaurant["city"],
            }
        )
        order_id += 1

    return orders


def generate_order_items(orders, restaurants):
    order_items = []
    item_id = 1
    menu_by_cuisine = {restaurant["id"]: MENU_ITEMS[restaurant["cuisine"]] for restaurant in restaurants}

    for order in orders:
        if order["status"] != "completed":
            continue
        restaurant_id = order["restaurant_id"]
        menu_options = menu_by_cuisine.get(restaurant_id, ["House Special"])
        item_count = max(1, min(order["items_count"], 6))

        for _ in range(item_count):
            item_name = random.choice(menu_options)
            quantity = random.randint(1, 3)
            unit_price = round(random.uniform(7.50, 21.90), 2)
            order_items.append(
                {
                    "id": item_id,
                    "order_id": order["id"],
                    "item_name": item_name,
                    "quantity": quantity,
                    "unit_price": f"{unit_price:.2f}",
                }
            )
            item_id += 1

    return order_items


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


users = generate_users(350)
restaurants = generate_restaurants()
orders = generate_orders(users, restaurants, completed_orders_target=1800)
order_items = generate_order_items(orders, restaurants)

write_csv(DATA_DIR / "users.csv", ["id", "name", "email", "city", "signup_date", "is_active"], users)
write_csv(
    DATA_DIR / "restaurants.csv",
    ["id", "name", "city", "cuisine", "avg_delivery_time_mins", "is_active"],
    restaurants,
)
write_csv(
    DATA_DIR / "orders.csv",
    [
        "id",
        "user_id",
        "restaurant_id",
        "order_date",
        "order_time",
        "status",
        "subtotal",
        "delivery_fee",
        "discount_amount",
        "order_total",
        "items_count",
        "city",
    ],
    orders,
)
write_csv(
    DATA_DIR / "order_items.csv",
    ["id", "order_id", "item_name", "quantity", "unit_price"],
    order_items,
)

print(f"Generated {len(users)} users")
print(f"Generated {len(restaurants)} restaurants")
print(f"Generated {len(orders)} orders")
print(f"Generated {len(order_items)} order_items")
print(f"All files saved to: {DATA_DIR}")
