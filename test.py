import random
from datetime import datetime, timedelta, time
from database.model.order import Order
from database.model.orderdetail import OrderDetail
from database.model.menuitem import MenuItem
from database.connection import create_connection, close_connection

def generate_random_orders(start_date, end_date, num_orders):
    """Generates random order data with realistic business patterns and saves it to the database."""

    menu_items = MenuItem.get_all()

    # Get valid employee IDs from the database
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM employees")
    valid_employee_ids = [row[0] for row in cursor.fetchall()]
    close_connection(connection)

    for _ in range(num_orders):
        # Generate random order date with patterns
        order_date = generate_random_date(start_date, end_date)
        day_of_week = order_date.weekday()
        order_multiplier = get_day_of_week_weight(day_of_week)
        num_order_details = int(random.gauss(3, 1))
        num_order_details = max(1, num_order_details)  # Ensure at least one item

        # Create the order
        employee_id = random.choice(valid_employee_ids)
        order = Order(employee_id=employee_id, date=order_date, cost=0.0)
        order.save()

        # Create order details
        order_details = []
        for _ in range(num_order_details):
            menu_item = random.choice(menu_items)
            qty = random.randint(1, 3)
            price = menu_item.price * qty

            order_detail = OrderDetail(order=order, menuitem=menu_item, qty=qty, price=price)
            order_detail.save()

            order_details.append(order_detail)

        # Update the order cost
        order.cost = sum(od.price for od in order_details)
        order.save()

def generate_random_date(start_date, end_date):
    """Generates a random datetime between two given dates, with realistic patterns."""
    time_between_dates = end_date - start_date
    total_seconds = time_between_dates.days * 24 * 3600 + time_between_dates.seconds
    random_seconds = random.randrange(total_seconds)
    random_datetime = start_date + timedelta(seconds=random_seconds)

    # Simulate peak hours (e.g., 11am-2pm, 5pm-8pm)
    peak_hours = [time(hour=h) for h in range(11, 15)] + [time(hour=h) for h in range(17, 21)]
    if random_datetime.time() not in peak_hours:
        # Add a chance to move to a peak hour
        if random.random() < 0.3:
            random_datetime = random_datetime.replace(hour=random.choice(range(11, 15)))
        elif random.random() < 0.3:
            random_datetime = random_datetime.replace(hour=random.choice(range(17, 21)))

    return random_datetime

def get_day_of_week_weight(day_of_week):
    """Returns weight for each day of the week to simulate business cycles."""
    weights = {
        0: 0.8,  # Monday
        1: 0.9,  # Tuesday
        2: 1.0,  # Wednesday
        3: 1.2,  # Thursday
        4: 1.5,  # Friday
        5: 1.8,  # Saturday
        6: 1.5   # Sunday
    }
    return weights.get(day_of_week, 1.0)

# Set the start and end dates for your desired period
start_date = datetime(2024, 6, 28)
end_date = datetime(2024, 8, 27)

# Generate a specific number of random orders
generate_random_orders(start_date, end_date, num_orders=300)
