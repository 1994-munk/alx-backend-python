#!/usr/bin/python3
import sqlite3
import functools

# ---------------------------
# Cache dictionary to store query results
# ---------------------------
query_cache = {}

# ---------------------------
# Task 1: with_db_connection decorator (reuse from before)
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
# Task 4: cache_query decorator
# ---------------------------
def cache_query(func):
    """Decorator to cache query results to avoid redundant DB calls."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # If we've already run this query, return the saved result
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]

        # Otherwise, run the function and save the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result  # Save result in cache
        print("Query executed and cached:", query)
        return result
    return wrapper


# ---------------------------
# Function using both decorators
# ---------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users with caching to avoid redundant queries."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ---------------------------
# Example usage
# ---------------------------

# First call: executes query and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call: uses cached result (does not hit the database again)
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
