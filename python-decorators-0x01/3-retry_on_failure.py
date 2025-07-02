import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connection opening and closing"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs): 
        conn = sqlite3.connect('users.db')
        try: 
            result = func(conn, *args, **kwargs)
            return result
        finally: 
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    """Decorator that retries a function if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)