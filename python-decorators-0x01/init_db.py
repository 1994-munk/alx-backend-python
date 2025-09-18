import sqlite3

# Connect to the database (creates users.db if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT
);
""")

# Insert some sample users
cursor.executemany("""
INSERT INTO users (name, age, email) VALUES (?, ?, ?)
""", [
    ("Alice", 30, "alice@example.com"),
    ("Bob", 25, "bob@example.com"),
    ("Charlie", 40, "charlie@example.com")
])

conn.commit()
conn.close()

print("✅ users.db created with sample data!")
