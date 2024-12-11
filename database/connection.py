import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',         # Database host
            user='root',     # Your MySQL username
            password='root', # Your MySQL password
            database='cafe' # Your database name
        )
        if connection.is_connected():
            #print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """Close the database connection."""
    if connection.is_connected():
        connection.close()
        print("Database connection closed")

