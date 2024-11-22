import mysql.connector
from mysql.connector import Error
import json


class MySQLHandler:
    def __init__(self, credential_file: str = "../../../.config/mysqlAccessKey.json"):
        """
        Initialize MySQLHandler with connection details from a credential file.
        """
        self.credential_file = credential_file
        self.connection = None
        self._load_credentials()

    def _load_credentials(self):
        """
        Load MySQL credentials from a JSON file and initialize connection details.
        """
        try:
            with open(self.credential_file, "r") as f:
                credentials = json.load(f)

            self.host = credentials.get("host")
            self.user = credentials.get("user")
            self.password = credentials.get("password")
            self.database = credentials.get("database")

        except FileNotFoundError:
            raise FileNotFoundError(f"Credential file '{self.credential_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in credential file '{self.credential_file}'.")

    def connect(self):
        """
        Establish a connection to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL.")
        except Error as e:
            raise ConnectionError(f"Error while connecting to MySQL: {e}")

    def disconnect(self):
        """
        Close the database connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a query (INSERT, UPDATE, DELETE) with optional parameters.
        """
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("No active MySQL connection.")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                print(f"Query executed: {query}")
        except Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Error executing query: {e}")

    def fetch_all(self, query: str, params: tuple = None):
        """
        Execute a SELECT query and fetch all results.
        """
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("No active MySQL connection.")
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Error fetching data: {e}")

    def fetch_one(self, query: str, params: tuple = None):
        """
        Execute a SELECT query and fetch one result.
        """
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("No active MySQL connection.")
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Error as e:
            raise RuntimeError(f"Error fetching data: {e}")


# if __name__ == "__main__":
#     # Initialize and connect to MySQL
#     db_handler = MySQLHandler()
#     db_handler.connect()

#     try:
#         # Example query
#         select_query = "SELECT * FROM paper_tb WHERE paper_doi = %s"
#         user = db_handler.fetch_one(select_query, ("10.18653/v1/2024.acl-long.3",))
#         print(user)
#     finally:
#         # Ensure the connection is closed
#         db_handler.disconnect()
