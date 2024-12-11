from database.connection import create_connection, close_connection
from mysql.connector import Error

class Employee:
    def __init__(self, id=None, name=None, role=None, phone=None, username=None, password=None, image=None):
        self._id = id
        self._name = name
        self._role = role
        self._phone = phone
        self._username = username
        self._password = password
        self._image = image

        # Validate the attributes
        self.validate()

    def validate(self):
        """Validate the attributes of the Employee."""
        if not self._name or not isinstance(self._name, str):
            raise ValueError("Invalid name: must be a non-empty string.")
        if self._role and not isinstance(self._role, str):
            raise ValueError("Invalid role: must be a string.")
        if self._phone and not isinstance(self._phone, str):
            raise ValueError("Invalid phone: must be a string.")
        if self._username and not isinstance(self._username, str):
            raise ValueError("Invalid username: must be a string.")
        if self._password and not isinstance(self._password, str):
            raise ValueError("Invalid password: must be a string.")
        if self._image and not isinstance(self._image, str):
            raise ValueError("Invalid image: must be a string.")

    def save(self):
        """Save the employee to the database."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                if self._id:
                    # Update existing employee
                    query = """UPDATE employees 
                               SET name=%s, role=%s, phone=%s, username=%s, password=%s, image=%s 
                               WHERE id=%s"""
                    cursor.execute(query, (self._name, self._role, self._phone,
                                           self._username, self._password, self._image, self._id))
                else:
                    # Insert new employee
                    query = """INSERT INTO employees (name, role, phone, username, password, image)
                               VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query, (self._name, self._role, self._phone,
                                           self._username, self._password, self._image))
                    self._id = cursor.lastrowid  # Update the ID with the last inserted ID
                connection.commit()
        except Error as e:
            print(f"Error while saving employee: {e}")
            raise e


        except ValueError as ve:
            print(f"Validation Error: {ve}")

    @staticmethod
    def get_all():
        """Retrieve all employees from the database."""
        employees = []
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM employees"
                cursor.execute(query)
                for (id, name, role, phone, username, password, image) in cursor:
                    employees.append(Employee(id, name, role, phone, username, password, image))
        except Error as e:
            print(f"Error while retrieving employees: {e}")
        return employees

    @staticmethod
    def get_by_id(id):
        """Retrieve an employee by their ID."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM employees WHERE id = %s"
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                if result:
                    id, name, role, phone, username, password, image = result
                    return Employee(id, name, role, phone, username, password, image)
        except Error as e:
            print(f"Error while retrieving employee by ID: {e}")
        return None

    @staticmethod
    def delete(id):
        """Delete an employee by their ID."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "DELETE FROM employees WHERE id = %s"
                cursor.execute(query, (id,))
                connection.commit()
        except Error as e:
            print(f"Error while deleting employee: {e}")

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
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid role: must be a string.")
        self._role = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid phone: must be a string.")
        self._phone = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid username: must be a string.")
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Invalid password: must be a string.")
        self._password = value

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
        return (f"Employee(\n"
                f"  id={self._id},\n"
                f"  name={self._name},\n"
                f"  role={self._role},\n"
                f"  phone={self._phone},\n"
                f"  username={self._username},\n"
                f"  password={self._password},\n" 
                f"  image={self._image}\n"
                f")")

    def __repr__(self):
        """Return a more detailed string representation, useful for debugging."""
        return (f"Employee(\n"
                f"  id={self._id},\n"
                f"  name='{self._name}',\n"
                f"  role={self._role},\n"
                f"  phone='{self._phone}',\n"
                f"  username='{self._username}',\n"
                f"  password='{self._password}',\n"
                f"  image='{self._image}'\n"
                f")")