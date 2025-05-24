import seed

def stream_users_in_batches(batch_size):
    """Yields users one by one from the DB, in batches."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as total FROM user_data")
        total_rows = cursor.fetchone()['total']
        
        for offset in range(0, total_rows, batch_size):
            cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
            batch = cursor.fetchall()
            for user in batch:
                yield user
                
        return
        
    finally:
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    """Processes users over age 25."""
    print("Processing users in batches...")
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            print(user)