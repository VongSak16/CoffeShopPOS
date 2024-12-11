from database.connection import create_connection, close_connection
from mysql.connector import Error
from database.model.menuitem import MenuItem
from database.model.order import Order

class OrderDetail:
    def __init__(self, id=None, order=None, menuitem=None, qty=None, price=None):
        self._id = id
        self._order = order
        self._menuitem = menuitem
        self._qty = qty
        self._price = price

        # Validate the attributes
        self.validate()

    def validate(self):
        """Validate the attributes of the OrderDetail."""
        if self._order is not None and not isinstance(self._order, Order):
            raise ValueError("Invalid order: must be an instance of Order or None.")

        if not isinstance(self._menuitem, MenuItem):
            raise ValueError("Invalid item menu: must be an instance of MenuItem.")

        if not isinstance(self._qty, int) or self._qty <= 0:
            raise ValueError("Invalid quantity: must be a positive integer.")

        if not isinstance(self._price, (int, float)) or self._price < 0:
            raise ValueError("Invalid price: must be a non-negative number.")

    def save(self):
        """Save the OrderDetail object to the database.

        If the OrderDetail already exists (i.e., has an ID), update it.
        Otherwise, insert a new record.

        Returns:
            int: The ID of the saved OrderDetail.
        """
        connection = create_connection()
        try:
            cursor = connection.cursor()

            if self._id is None:  # Insert new record
                insert_query = """INSERT INTO OrderDetails (order_id, menuitem_id, qty, price)
                                  VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_query, (self._order.id, self._menuitem.id, self._qty, self._price))
                connection.commit()
                # Retrieve the ID of the newly inserted record
                self._id = cursor.lastrowid
            else:  # Update existing record
                update_query = """UPDATE OrderDetails
                                  SET order_id = %s, menuitem_id = %s, qty = %s, price = %s
                                  WHERE id = %s"""
                cursor.execute(update_query, (self._order.id, self._menuitem.id, self._qty, self._price, self._id))
                connection.commit()

            return self._id

        except Error as e:
            print(f"Database error: {e}")
            connection.rollback()
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
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if not value or not isinstance(value, Order):
            raise ValueError("Invalid order: must be an instance of Order.")
        self._order = value

    @property
    def menuitem(self):
        return self._menuitem

    @menuitem.setter
    def menuitem(self, value):
        if not value or not isinstance(value, MenuItem):
            raise ValueError("Invalid menu item: must be an instance of MenuItem.")
        self._menuitem = value

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Invalid quantity: must be a positive integer.")
        self._qty = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Invalid price: must be a non-negative number.")
        self._price = value

    def __str__(self):
        """Return a human-readable string representation of the object."""
        return (f"OrderDetail(\n"
                f"  id={self._id},\n"
                f"  order={self._order},\n"
                f"  menuitem={self._menuitem},\n"
                f"  qty={self._qty},\n"
                f"  price={self._price}\n"
                f")")

    def __repr__(self):
        """Return a more detailed string representation, useful for debugging."""
        return (f"OrderDetail(\n"
                f"  id={self._id},\n"
                f"  order={repr(self._order)},\n"
                f"  menuitem={repr(self._menuitem)},\n"
                f"  qty={self._qty},\n"
                f"  price={self._price}\n"
                f")")
