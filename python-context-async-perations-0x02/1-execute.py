# 1-execute.py
import sqlite3

# Custom class-based context manager for executing queries
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name      # database name
        self.query = query          # query string
        self.params = params or []  # query parameters
        self.conn = None
        self.cursor = None
        self.results = None

    # Called at the start of the with block
    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        
        # Fetch results
        self.results = self.cursor.fetchall()
        
        # Return results directly
        return self.results

    # Called when leaving the with block
    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage example
with ExecuteQuery("my_database.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
