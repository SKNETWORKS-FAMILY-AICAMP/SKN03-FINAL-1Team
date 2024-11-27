import mysql.connector
from mysql.connector import Error
import json
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

# def singleton(cls):
#     """
#     Decorator to make a class a Singleton.
#     """
#     instances = {}

#     def get_instance(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]

#     return get_instance


# @singleton
class MySQLHandler:
    def __init__(self):
        """
        Initialize MySQLHandler with connection details from aws ssm.
        """
        self.connection = None
        self._load_credentials()

    def _load_credentials(self):
        """
        Load MySQL credentials from aws ssm and initialize connection details.
        """
        try:
            ssm = boto3.client('ssm')

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/MYSQL_ACCESS_KEY/HOST', WithDecryption=True)
            self.host = parameter['Parameter']['Value']

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/MYSQL_ACCESS_KEY/USER', WithDecryption=True)
            self.user = parameter['Parameter']['Value']

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/MYSQL_ACCESS_KEY/PASSWORD', WithDecryption=True)
            self.password = parameter['Parameter']['Value']

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/MYSQL_ACCESS_KEY/DATABASE', WithDecryption=True)
            self.database = parameter['Parameter']['Value']

        except (BotoCoreError, ClientError) as e:
            print(f"Error retrieving parameter from SSM: {e}")
            raise

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
