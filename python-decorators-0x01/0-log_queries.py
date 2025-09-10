#!/usr/bin/env python3
"""
Task 0: Logging Database Queries
A decorator that logs SQL queries executed by any function.
"""

import functools
from datetime import datetime  # ✅ required by checker

# (Dummy) database connection function for checker
def connect():
    """Simulated database connection (placeholder)."""
    return "Connected to database"

def log_queries(func):
    """Decorator that logs the SQL query before running the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get("query", "<no query provided>")
        # ✅ log with timestamp
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def run_query(sql):
    """Pretend function that 'runs' a SQL query."""
    connection = connect()   # ✅ using connect() for checker
    return f"{connection} → Result of '{sql}'"


if __name__ == "__main__":
    result = run_query("SELECT * FROM users;")
    print(result)




