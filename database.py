import sqlite3

DB_NAME = "vms44AKDB.db"

class VMS_DB:
    def __init__(self) -> None:
        pass

    def create_connection(self):
        """Create a database connection."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        return conn, cursor

    def get_user_by_username(self, username):
        """Fetch a user by username."""
        conn, cursor = self.create_connection()
        cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user  # Returns (id, username, password, is_blocked) or None
    
    def fetch_users(self):
        """Fetch a user by username."""
        conn, cursor = self.create_connection()
        cursor.execute("SELECT id, name, username, email, is_blocked FROM users ORDER BY created_at ASC")
        users = cursor.fetchall()
        conn.close()
        return users  # Returns (id, username, password, is_blocked) or None
    
    def insert_user(self, name, email, username, password, is_blocked=0):
        """ Inserts user into SQLite Database """
        conn, cursor = self.create_connection()
        cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
                       (name, email, username, password, is_blocked))
        conn.commit()
        conn.close()

    def delete_user(self, id):
        """ Deletes a user from SQLite Database based on user ID """
        conn, cursor = self.create_connection()
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def update_user_in_db(self, name, email, username, password, is_blocked, id):
        """ Update user in the SQLite database """
        conn, cursor = self.create_connection()
        cursor.execute("""
            UPDATE users
            SET name = ?, email = ?, username = ?, password = ?, is_blocked = ?
            WHERE id = ?
        """, (name, email, username, password, is_blocked, id))
        conn.commit()
        conn.close()

    def fetch_user_by_id(self, user_id):
        conn, cursor = self.create_connection()
        cursor.execute("SELECT name, username, email, password, is_blocked FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result  # This should return a tuple with user data
