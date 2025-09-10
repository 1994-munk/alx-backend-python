#!/usr/bin/python3
import sqlite3
import functools

# ---------------------------
# Task 1: with_db_connection decorator
# ---------------------------
def with_db_connection(func):
    """Decorator to automatically open and close DB connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # Open DB connection
        try:
            # Pass the connection to the decorated function
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # Always close connection
    return wrapper


# ---------------------------
# Task 2: transactional decorator
# ---------------------------
def transactional(func):
    """Decorator to manage DB transactions (commit or rollback)."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if error occurs
            print("Transaction failed, rolled back:", e)
            raise
    return wrapper


# ---------------------------
# Function using both decorators
# ---------------------------
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update user's email with automatic transaction handling."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print("User email updated successfully ✅")
