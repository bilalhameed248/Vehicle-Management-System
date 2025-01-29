import sqlite3

DB_NAME = "vms44AKDB.db"

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def get_user_by_username(username):
    """Fetch a user by username."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns (id, username, password, is_blocked) or None
