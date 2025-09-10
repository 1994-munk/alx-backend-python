#!/usr/bin/python3
import time
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
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # Always close connection
    return wrapper


# ---------------------------
# Task 3: retry_on_failure decorator
# ---------------------------
def retry_on_failure(retries=3, delay=2):
    """Decorator to retry DB operations if they fail."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("All retries failed ❌")
                        raise
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator


# ---------------------------
# Function using both decorators
# ---------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch all users with automatic retry on failure."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Will retry if this fails
    return cursor.fetchall()


# Example usage
users = fetch_users_with_retry()
print("Users fetched successfully ✅")
print(users)
