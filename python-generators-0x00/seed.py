import mysql.connector
from mysql.connector import Error

# 1. Connect to MySQL server (not to a specific database yet)
def connect_db():
    """
    Connects to the MySQL server (without selecting a database).
    Returns the connection object if successful, else None.
    """
    try:
        # create a connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",   # where MySQL is running
            user="alxuser",        #  MySQL username
            password="ALXpass123",  #  MySQL password (👉 change this to yours!)
            charset="utf8"  # force plain utf8
        )

        # check if connection is established
        if connection.is_connected():
            print("✅ Connected to MySQL server")
            return connection

    except Error as e:
        # catch and display any errors
        print(f"❌ Error: {e}")
        return None


# 2. Create the ALX_prodev database if it does not exist
def create_database(connection):
    """
    Creates the database ALX_prodev if it doesn't already exist.
    """
    try:
        # get a cursor (like a tool to run SQL commands)
        cursor = connection.cursor()

        # SQL command to create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")

        print("✅ Database ALX_prodev is ready")

        # close the cursor after use
        cursor.close()

    except Error as e:
        # catch and display any errors
        print(f"❌ Error creating database: {e}")



def connect_to_prodev():
    """
    Connects directly to the ALX_prodev database in MySQL.
    Returns the connection object if successful.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alxuser",              # replace with your MySQL username
            password="ALXpass123",  # replace with your MySQL password
            database="ALX_prodev",
            charset="utf8"  # force plain utf8
        )
        if connection.is_connected():
            print("✅ Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """
    Creates the user_data table in ALX_prodev if it does not already exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("✅ Table user_data created successfully (or already exists).")
        cursor.close()
    except Error as e:
        print(f"❌ Error creating table: {e}")

import csv
import uuid
from mysql.connector import Error

def insert_data(connection, csv_file):
    """
    Inserts data from a CSV file into the user_data table.
    Generates a unique user_id for each row.
    """
    try:
        cursor = connection.cursor()

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # expects headers: name,email,age
            for row in reader:
                user_id = str(uuid.uuid4())  # generate a unique ID for each user
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row["name"], row["email"], row["age"]))

        connection.commit()
        print("✅ Data inserted successfully from CSV.")
        cursor.close()

    except Error as e:
        print(f"❌ Error inserting data: {e}")


        

    