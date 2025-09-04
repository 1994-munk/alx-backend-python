from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database with given page_size and offset.
    """
    connection = connect_to_prodev()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()  # fetch the page
    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that lazily fetches users page by page.
    """
    offset = 0
    while True:  # loop 1 (only loop allowed)
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop when no more rows
        yield page  # yield one page
        offset += page_size  # move to next page
