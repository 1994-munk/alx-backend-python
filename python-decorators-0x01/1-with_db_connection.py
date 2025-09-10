#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator
Automatically open and close a database connection for any function.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a DB connection, passes it to the function,
    and ensures the connection is closed afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ✅ Open a connection to a SQLite DB file
        conn = sqlite3.connect("my_database.db")
        try:
            # ✅ Pass the connection into the decorated function
            result = func(conn, *args, **kwargs)
        finally:
            # ✅ Always close connection (even if error happens)
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a user from the DB by ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example test run
if __name__ == "__main__":
    # Set up demo DB with a table + sample row
    with sqlite3.connect("my_database.db") as demo_conn:
        demo_cursor = demo_conn.cursor()
        demo_cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
        demo_cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (1, "Alice"))
        demo_conn.commit()

    # ✅ Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)
