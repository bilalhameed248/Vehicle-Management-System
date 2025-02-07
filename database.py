import sqlite3, traceback
import mysql.connector
import MySQLdb as mdb

class VMS_DB:
    def __init__(self) -> None:
        self.host = "BIlal_PC"
        self.user = "44_AK_HB_DB_User"
        self.password = "Here2enter!123"
        self.database = "44_AK_HB_DB"

    def db_connect(self):
        try:
            conn = mdb.connect(self.host, self.user, self.password, self.database)
            cursor = conn.cursor()
            if conn:
                print("Connected to MySQL database")
            return conn, cursor
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def db_disconnect(self, conn, cursor):
        if conn:
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


    # Function to insert data into all_vehicles
    def insert_vehicle(self, data):
        try:
            """ Inserts vehicle data into MySQL Database """
            conn, cursor = self.db_connect()
            cursor.execute("""
                INSERT INTO all_vehicles (
                    category, ba_no_input, make_type_input, engine_no_input,
                    issue_date_oil_filter, due_date_oil_filter, current_mileage_oil_filter, due_mileage_oil_filter,
                    issue_date_fuel_filter, due_date_fuel_filter, current_mileage_fuel_filter, due_mileage_fuel_filter,
                    issue_date_air_filter, due_date_air_filter, current_mileage_air_filter, due_mileage_air_filter,
                    issue_date_transmission_filter, due_date_transmission_filter, current_mileage_transmission_filter, due_mileage_transmission_filter,
                    issue_date_differential_oil, due_date_differential_oil, current_mileage_differential_oil, due_mileage_differential_oil,
                    battery_issue_date, battery_due_date,
                    flusing_issue_date, flusing_due_date, fuel_tank_flush, radiator_flush,
                    greasing_issue_date, greasing_due_date,
                    trs_and_suspension, engine_part, steering_lever_Pts, wash, oil_level_check, lubrication_of_parts,
                    air_cleaner, fuel_filter, french_chalk, tr_adjustment,
                    overhaul_current_milage, overhaul_due_milage, overhaul_remarks_input,
                    created_by, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(data.values()))
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: insert_vehicle {e}")
            return False




# import sqlite3

# DB_NAME = "vms44AKDB.db"

# class VMS_DB:
#     def __init__(self) -> None:
#         pass

#     def create_connection(self):
#         """Create a database connection."""
#         conn = sqlite3.connect(DB_NAME)
#         cursor = conn.cursor()
#         return conn, cursor

#     def get_user_by_username(self, username):
#         """Fetch a user by username."""
#         conn, cursor = self.create_connection()
#         cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = ?", (username,))
#         user = cursor.fetchone()
#         conn.close()
#         return user  # Returns (id, username, password, is_blocked) or None
    
#     def fetch_users(self):
#         """Fetch a user by username."""
#         conn, cursor = self.create_connection()
#         cursor.execute("SELECT id, name, username, email, is_blocked FROM users ORDER BY created_at ASC")
#         users = cursor.fetchall()
#         conn.close()
#         return users  # Returns (id, username, password, is_blocked) or None
    
#     def insert_user(self, name, email, username, password, is_blocked=0):
#         """ Inserts user into SQLite Database """
#         conn, cursor = self.create_connection()
#         cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
#                        (name, email, username, password, is_blocked))
#         conn.commit()
#         conn.close()

#     def delete_user(self, id):
#         """ Deletes a user from SQLite Database based on user ID """
#         conn, cursor = self.create_connection()
#         cursor.execute("DELETE FROM users WHERE id = ?", (id,))
#         conn.commit()
#         conn.close()

#     def update_user_in_db(self, name, email, username, password, is_blocked, id):
#         """ Update user in the SQLite database """
#         conn, cursor = self.create_connection()
#         cursor.execute("""
#             UPDATE users
#             SET name = ?, email = ?, username = ?, password = ?, is_blocked = ?
#             WHERE id = ?
#         """, (name, email, username, password, is_blocked, id))
#         conn.commit()
#         conn.close()

#     def fetch_user_by_id(self, user_id):
#         conn, cursor = self.create_connection()
#         cursor.execute("SELECT name, username, email, password, is_blocked FROM users WHERE id=?", (user_id,))
#         result = cursor.fetchone()
#         conn.close()
#         return result  # This should return a tuple with user data
