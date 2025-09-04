# 0-stream_users.py
import mysql.connector
from seed import connect_to_prodev

def stream_users():
    """
    Generator that streams rows one by one from the user_data table.
    """
    connection = connect_to_prodev()  # connect to ALX_prodev
    if not connection:
        return  # stop if connection fails

    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    cursor.execute("SELECT * FROM user_data")   # fetch all rows

    for row in cursor:  # generator yields one row at a time
        yield row
    cursor.close()
    connection.close()
