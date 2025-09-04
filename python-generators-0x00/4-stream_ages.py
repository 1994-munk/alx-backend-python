from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # loop 1
        yield row["age"]

    cursor.close()
    connection.close()

def average_age():
    """
    Calculates the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    avg = total / count
    print(f"Average age of users: {avg:.2f}")
