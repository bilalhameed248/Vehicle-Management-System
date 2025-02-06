import sqlite3
import mysql.connector

DB_NAME = "vms44AKDB.db"

class VMS_DB:
    def __init__(self) -> None:
        pass

    def db_connect(self):
        try:
            conn = mysql.connector.connect(
                host="192.168.100.28",
                user="44_AK_HB_DB_User",
                password="Here2enter!123",
                database="44_AK_HB_DB"
            )
            cursor = conn.cursor()
            if conn.is_connected():
                print("Connected to MySQL database")
            return conn, cursor
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def db_disconnect(self, conn, cursor):
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

    def get_user_by_username(self, username):
        """Fetch a user by username."""
        conn, cursor = self.db_connect()
        cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        self.db_disconnect(conn, cursor)
        return user
    
    def fetch_users(self):
        """Fetch a user by username."""
        conn, cursor = self.db_connect()
        cursor.execute("SELECT id, name, username, email, is_blocked FROM users ORDER BY created_at ASC")
        users = cursor.fetchall()
        self.db_disconnect(conn, cursor)
        return users  # Returns (id, username, password, is_blocked) or None
    
    def insert_user(self, name, email, username, password, is_blocked=0):
        """ Inserts user into SQLite Database """
        conn, cursor = self.db_connect()
        cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (%s, %s, %s, %s, %s)", 
                       (name, email, username, password, is_blocked))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def delete_user(self, id):
        """ Deletes a user from SQLite Database based on user ID """
        conn, cursor = self.db_connect()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def update_user_in_db(self, name, email, username, password, is_blocked, id):
        """ Update user in the SQLite database """
        conn, cursor = self.db_connect()
        cursor.execute("""
            UPDATE users
            SET name = %s, email = %s, username = %s, password = %s, is_blocked = %s
            WHERE id = %s
        """, (name, email, username, password, is_blocked, id))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def fetch_user_by_id(self, user_id):
        conn, cursor = self.db_connect()
        cursor.execute("SELECT name, username, email, password, is_blocked FROM users WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        self.db_disconnect(conn, cursor)
        return result  # This should return a tuple with user data


if __name__ =="__main__":
    db_obj = VMS_DB()
    conn, cursor = db_obj.db_connect()
    if conn:
        print("🎉 Connection to MySQL is working!")
        conn.close()
    else:
        print("⚠️ Failed to connect. Check the error above!")