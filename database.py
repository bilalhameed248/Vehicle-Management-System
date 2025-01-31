import sqlite3

DB_NAME = "vms44AKDB.db"

class VMS_DB:
    def __init__(self) -> None:
        pass

    def create_connection(self):
        """Create a database connection."""
        conn = sqlite3.connect(DB_NAME)
        return conn

    def get_user_by_username(self, username):
        """Fetch a user by username."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user  # Returns (id, username, password, is_blocked) or None
    
    def fetch_users(self):
        """Fetch a user by username."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, is_blocked FROM users")
        users = cursor.fetchall()
        conn.close()
        return users  # Returns (id, username, password, is_blocked) or None
