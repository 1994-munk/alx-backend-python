# 3-concurrent.py
import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

# Run both queries concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", users)
    print("Users older than 40:", older_users)

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
