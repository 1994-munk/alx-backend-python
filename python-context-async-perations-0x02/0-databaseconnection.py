#!/usr/bin/python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for handling database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # Give the connection to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection when leaving the context, even if error occurs."""
        if self.conn:
            self.conn.close()


# ---------------------------
# Example usage
# ---------------------------

with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users from DB:", results)
