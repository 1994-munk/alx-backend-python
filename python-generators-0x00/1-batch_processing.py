# 1-batch_processing.py
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches of `batch_size`.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # yield full batch
            batch = []  # reset batch

    if batch:  # yield remaining rows if any
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes batches to filter users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:  # loop 3
            if user["age"] > 25:
                yield user
