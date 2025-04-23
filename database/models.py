from database.db import get_db_connection

def add_user(user_id, name=None):
    conn = get_db_connection()
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)",
            (user_id, name)
        )

def get_all_users():
    conn = get_db_connection()
    with conn:
        return conn.execute("SELECT * FROM users").fetchall()
    
def get_user_messages(user_id):
    print(f"Fetching messages for User ID: {user_id}")  # Debug log
    conn = get_db_connection()
    with conn:
        return conn.execute(
            "SELECT * FROM messages WHERE user_id = ? ORDER BY timestamp",
            (user_id,)
        ).fetchall()
    
def save_message(user_id, message, is_admin):
    print(f"Saving message: User ID: {user_id}, Message: {message}, Is Admin: {is_admin}")  # Debug log
    conn = get_db_connection()
    with conn:
        conn.execute(
            "INSERT INTO messages (user_id, message, is_admin) VALUES (?, ?, ?)",
            (user_id, message, is_admin)
        )

def debug_users():
    conn = get_db_connection()
    with conn:
        users = conn.execute("SELECT * FROM users").fetchall()
        print("Users Table:", users)

def debug_messages():
    conn = get_db_connection()
    with conn:
        messages = conn.execute("SELECT * FROM messages").fetchall()
        print("Messages Table:", messages)