from database.connection import create_connection
from mysql.connector import Error

class AuthDAO:
    @staticmethod
    def validate_user(username, password):
        """Validate user credentials and return user details including the username."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT id, name, role, username FROM employees WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                if result:
                    user_id, name, role, username = result
                    return {"id": user_id, "name": name, "role": role, "username": username}
                else:
                    return None
        except Error as e:
            print(f"\033[91mError while validating user: {e}\033[0m")
            return None

    @staticmethod
    def check_if_user_exists(username):
        """Check if a user with the given username exists."""
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                query = "SELECT COUNT(*) FROM employees WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result:
                    count = result[0]
                    return count > 0  # Return True if count > 0, otherwise False
                else:
                    return False
        except Error as e:
            print(f"\033[91mError while checking if user exists: {e}\033[0m")
            return False
