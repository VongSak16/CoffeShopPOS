from database.connection import create_connection, close_connection
from mysql.connector import Error

class MenuItem:
    def __init__(self, id=None, name=None, price=None, description=None, image=None):
        self._id = id
        self._name = name
        self._price = price
        self._description = description
        self._image = image

        # Validate the attributes
        self.validate()

    def validate(self):
        """Validate the attributes of the MenuItem."""
        if not self._name or not isinstance(self._name, str):
            raise ValueError("Invalid name: must be a non-empty string.")
        if not isinstance(self._price, (int, float)) or self._price < 0:
            raise ValueError("Invalid price: must be a non-negative number.")
        if self._description and not isinstance(self._description, str):
            raise ValueError("Invalid description: must be a string.")
        if self._image and not isinstance(self._image, str):
            raise ValueError("Invalid image: must be a string.")

    def save(self):
        """Save the menu item to the database."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = """INSERT INTO menuitems (name, price, description, image)
                           VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (self._name, self._price, self._description, self._image))
                connection.commit()  # Commit the transaction
                self._id = cursor.lastrowid  # Update the ID with the last inserted ID
        except Error as e:
            print(f"Error while saving menu item: {e}")
        except ValueError as ve:
            print(f"Validation Error: {ve}")

    @staticmethod
    def get_all():
        """Retrieve all menu items from the database."""
        menu_items = []
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM menuitems"
                cursor.execute(query)
                for (id, name, price, description, image) in cursor:
                    price = float(price)  # Ensure price is converted to float
                    menu_items.append(MenuItem(id, name, price, description, image))
        except Error as e:
            print(f"Error while retrieving menu items: {e}")
        return menu_items

    @staticmethod
    def get_by_id(id):
        """Retrieve a menu item by its ID."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM menuitems WHERE id = %s"
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                if result:
                    id, name, price, description, image = result
                    price = float(price)  # Ensure price is converted to float
                    return MenuItem(id, name, price, description, image)
        except Error as e:
            print(f"Error while retrieving menu item by ID: {e}")
        return None

    def update(self):
        """Update the menu item in the database."""
        if not self._id:
            raise ValueError("Cannot update a menu item without an ID.")
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = """UPDATE menuitems
                           SET name = %s, price = %s, description = %s, image = %s
                           WHERE id = %s"""
                cursor.execute(query, (self._name, self._price, self._description, self._image, self._id))
                connection.commit()  # Commit the transaction
        except Error as e:
            print(f"Error while updating menu item: {e}")

    @staticmethod
    def delete(id):
        """Delete a menu item by its ID."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "DELETE FROM menuitems WHERE id = %s"
                cursor.execute(query, (id,))
                connection.commit()  # Commit the transaction
        except Error as e:
            print(f"Error while deleting menu item: {e}")

    # Getters and setters
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Invalid name: must be a non-empty string.")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Invalid price: must be a non-negative number.")
        self._price = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid description: must be a string.")
        self._description = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid image: must be a string.")
        self._image = value

    def __str__(self):
        """Return a human-readable string representation of the object."""
        return (f"MenuItem(\n"
                f"  id={self._id},\n"
                f"  name={self._name},\n"
                f"  price={self._price},\n"
                f"  description={self._description},\n"
                f"  image={self._image}\n"
                f")")

    def __repr__(self):
        """Return a more detailed string representation, useful for debugging."""
        return (f"MenuItem(\n"
                f"  id={self._id},\n"
                f"  name='{self._name}',\n"
                f"  price={self._price},\n"
                f"  description='{self._description}',\n"
                f"  image='{self._image}'\n"
                f")")
