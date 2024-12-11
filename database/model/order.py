from datetime import datetime
from database.connection import create_connection, close_connection

class Order:
    def __init__(self, id=None, employee_id=None, date=None, cost=None):
        self._id = id
        self._employee_id = employee_id
        self._date = date
        self._cost = cost

        # Validate the attributes
        self.validate()

    def validate(self):
        """Validate the attributes of the Order."""
        if not isinstance(self._employee_id, int):
            raise ValueError("Invalid employee_id: must be an integer.")

        if not isinstance(self._date, datetime):
            raise ValueError("Invalid date: must be a datetime object.")

        if self._cost is not None and not isinstance(self._cost, (int, float)):
            raise ValueError("Invalid cost: must be a numeric value (int or float).")

    def save(self):
        """Save the Order object to the database.

        If the order already exists (i.e., has an ID), update it.
        Otherwise, insert a new record.

        Returns:
            int: The ID of the saved Order.
        """
        connection = create_connection()
        try:
            cursor = connection.cursor()

            if self._id is None:  # Insert new record
                insert_query = """INSERT INTO Orders (employee_id, date, cost)
                                  VALUES (%s, %s, %s)"""
                cursor.execute(insert_query, (self._employee_id, self._date, self._cost))
                connection.commit()
                # Retrieve the ID of the newly inserted record
                self._id = cursor.lastrowid
            else:  # Update existing record
                update_query = """UPDATE Orders
                                  SET employee_id = %s, date = %s, cost = %s
                                  WHERE id = %s"""
                cursor.execute(update_query, (self._employee_id, self._date, self._cost, self._id))
                connection.commit()

            return self._id

        except Exception as e:
            print(f"Database error: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_all():
        """Retrieve all Order records from the database.

        Returns:
            list: A list of Order objects.
        """
        connection = create_connection()
        cursor = None
        orders = []

        try:
            cursor = connection.cursor()
            select_query = "SELECT id, employee_id, date, cost FROM Orders"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            for row in rows:
                id, employee_id, date, cost = row

                # Debugging: Print raw data
                print(f"Raw data from database: id={id}, employee_id={employee_id}, date={date}, cost={cost}")

                # Convert cost to a numeric type, handle possible conversion errors
                try:
                    cost = float(cost)  # Ensure cost is converted to float
                except (ValueError, TypeError) as e:
                    print(f"Invalid cost value: {cost}. Error: {e}")
                    continue  # Skip this entry if conversion fails

                # Create Order object and append to list
                order = Order(id=id, employee_id=employee_id, date=date, cost=cost)
                orders.append(order)

        except Exception as e:
            print(f"Database error: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                close_connection(connection)

        if not orders:
            print("No orders found.")
        else:
            print(f"{len(orders)} orders retrieved successfully.")

        return orders

    @staticmethod
    def get_by_id(order_id):
        """Retrieve a single Order record by its ID.

        Args:
            order_id (int): The ID of the Order to retrieve.

        Returns:
            Order: The Order object with the specified ID, or None if not found.
        """
        connection = create_connection()
        try:
            cursor = connection.cursor()
            select_query = """SELECT id, employee_id, date, cost FROM Orders WHERE id = %s"""
            cursor.execute(select_query, (order_id,))
            row = cursor.fetchone()

            if row:
                return Order(id=row[0], employee_id=row[1], date=row[2], cost=row[3])
            else:
                return None

        except Exception as e:
            print(f"Database error: {e}")
            raise
        finally:
            cursor.close()
            close_connection(connection)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid employee_id: must be an integer.")
        self._employee_id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime):
            raise ValueError("Invalid date: must be a datetime object.")
        self._date = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("Invalid cost: must be a numeric value (int or float).")
        self._cost = value

    def __str__(self):
        """Return a human-readable string representation of the object."""
        return (f"Order(\n"
                f"  id={self._id},\n"
                f"  employee_id={self._employee_id},\n"
                f"  date={self._date},\n"
                f"  cost={self._cost}\n"
                f")")

    def __repr__(self):
        """Return a more detailed string representation, useful for debugging."""
        return (f"Order(\n"
                f"  id={self._id},\n"
                f"  employee_id={self._employee_id},\n"
                f"  date={self._date},\n"
                f"  cost={self._cost}\n"
                f")")
