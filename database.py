import sqlite3, traceback
import mysql.connector
import MySQLdb as mdb
import sys, os

class VMS_DB1:
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
        except Exception as err:
            print(f"Error: {err}")
            return None, None


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
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
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
                    created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = tuple(data.values())
            cursor.execute(sql, values)
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: insert_vehicle {e}")
            return False
        
    # Function to insert data into all_vehicles
    def update_vehicle(self, data, vehicle_id):
        try:
            """ Inserts vehicle data into MySQL Database """
            conn, cursor = self.db_connect()
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
                UPDATE all_vehicles
                SET 
                    category = %s, ba_no_input = %s, make_type_input = %s, engine_no_input = %s,
                    issue_date_oil_filter = %s, due_date_oil_filter = %s, current_mileage_oil_filter = %s, due_mileage_oil_filter = %s,
                    issue_date_fuel_filter = %s, due_date_fuel_filter = %s, current_mileage_fuel_filter = %s, due_mileage_fuel_filter = %s,
                    issue_date_air_filter = %s, due_date_air_filter = %s, current_mileage_air_filter = %s, due_mileage_air_filter = %s,
                    issue_date_transmission_filter = %s, due_date_transmission_filter = %s, current_mileage_transmission_filter = %s, due_mileage_transmission_filter = %s,
                    issue_date_differential_oil = %s, due_date_differential_oil = %s, current_mileage_differential_oil = %s, due_mileage_differential_oil = %s,
                    battery_issue_date = %s, battery_due_date = %s,
                    flusing_issue_date = %s, flusing_due_date = %s, fuel_tank_flush = %s, radiator_flush = %s,
                    greasing_issue_date = %s, greasing_due_date = %s,
                    trs_and_suspension = %s, engine_part = %s, steering_lever_Pts = %s, wash = %s, oil_level_check = %s, lubrication_of_parts = %s,
                    air_cleaner = %s, fuel_filter = %s, french_chalk = %s, tr_adjustment = %s,
                    overhaul_current_milage = %s, overhaul_due_milage = %s, overhaul_remarks_input = %s,
                    updated_by = %s, updated_at = %s
                WHERE id = %s
            """
            vehicle_data_with_id = tuple(data.values()) + (vehicle_id,)
            cursor.execute(sql, vehicle_data_with_id)
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: insert_vehicle {e}")
            return False
        
    # Function to insert data into all_vehicles
    def get_all_vehicle(self):
        try:
            all_vehicles = ()
            """ Inserts vehicle data into MySQL Database """
            conn, cursor = self.db_connect()
            sql = """SELECT 
                    av.id, av.category, av.ba_no_input, av.make_type_input, av.engine_no_input,
                    av.issue_date_oil_filter, av.due_date_oil_filter, av.current_mileage_oil_filter, av.due_mileage_oil_filter,
                    av.issue_date_fuel_filter, av.due_date_fuel_filter, av.current_mileage_fuel_filter, av.due_mileage_fuel_filter,
                    av.issue_date_air_filter, av.due_date_air_filter, av.current_mileage_air_filter, av.due_mileage_air_filter,
                    av.issue_date_transmission_filter, av.due_date_transmission_filter, av.current_mileage_transmission_filter, av.due_mileage_transmission_filter,
                    av.issue_date_differential_oil, av.due_date_differential_oil, av.current_mileage_differential_oil, av.due_mileage_differential_oil,
                    av.battery_issue_date, av.battery_due_date,
                    av.flusing_issue_date, av.flusing_due_date, av.fuel_tank_flush, av.radiator_flush,
                    av.greasing_issue_date, av.greasing_due_date,
                    av.trs_and_suspension, av.engine_part, av.steering_lever_Pts, av.wash, av.oil_level_check, av.lubrication_of_parts,
                    av.air_cleaner, av.fuel_filter, av.french_chalk, av.tr_adjustment,
                    av.overhaul_current_milage, av.overhaul_due_milage, av.overhaul_remarks_input,
                    u.name AS created_by,
                    av.created_at
                FROM all_vehicles av
                LEFT JOIN users u ON av.created_by = u.id  -- Joining users table to get the name
                WHERE av.is_deleted = 0 
                ORDER BY av.created_at DESC;"""
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()
            all_vehicles = [dict(zip(columns, row)) for row in rows]
            self.db_disconnect(conn, cursor)
            return all_vehicles
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_all_vehicle {e}")
            return all_vehicles

    def delete_vehicle(self, vehicle_id):
        try:
            conn, cursor = self.db_connect()
            cursor.execute("""
                UPDATE all_vehicles
                SET is_deleted = %s
                WHERE id = %s
            """, (1, vehicle_id))
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_all_vehicle {e}")
            return False





import sqlite3
DB_NAME = "vms44AKDB.db"
class VMS_DB:
    def __init__(self) -> None:
        self.db_path = self.get_database_path()

    def get_database_path(self):
        """Returns the correct database path, whether running as script or executable."""
        if getattr(sys, 'frozen', False):  # If running as an executable (PyInstaller)
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))  # Normal script execution
        
        return os.path.join(base_path, "vms44AKDB.db") 

    def db_connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if conn:
                print("Connected to MySQL database")
            return conn, cursor
        except Exception as err:
            print(f"Error: {err}")
            return None, None

    def db_disconnect(self, conn, cursor):
        if conn:
            cursor.close()
            conn.close()
            print("Connection closed.")
        
    def get_user_by_username(self, username):
        """Fetch a user by username."""
        conn, cursor = self.db_connect()
        cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        self.db_disconnect(conn, cursor)
        return user  # Returns (id, username, password, is_blocked) or None
    
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
        cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
                       (name, email, username, password, is_blocked))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def delete_user(self, id):
        """ Deletes a user from SQLite Database based on user ID """
        conn, cursor = self.db_connect()
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def update_user_in_db(self, name, email, username, password, is_blocked, id):
        """ Update user in the SQLite database """
        conn, cursor = self.db_connect()
        cursor.execute("""
            UPDATE users
            SET name = ?, email = ?, username = ?, password = ?, is_blocked = ?
            WHERE id = ?
        """, (name, email, username, password, is_blocked, id))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def fetch_user_by_id(self, user_id):
        conn, cursor = self.db_connect()
        cursor.execute("SELECT name, username, email, password, is_blocked FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        self.db_disconnect(conn, cursor)
        return result
    
    def get_all_vehicle(self):
        try:
            all_vehicles = []
            conn, cursor = self.db_connect()
            sql = """SELECT 
                    av.id, av.category, av.ba_no_input, av.make_type_input, av.engine_no_input,
                    av.issue_date_oil_filter, av.due_date_oil_filter, av.current_mileage_oil_filter, av.due_mileage_oil_filter,
                    av.issue_date_fuel_filter, av.due_date_fuel_filter, av.current_mileage_fuel_filter, av.due_mileage_fuel_filter,
                    av.issue_date_air_filter, av.due_date_air_filter, av.current_mileage_air_filter, av.due_mileage_air_filter,
                    av.issue_date_transmission_filter, av.due_date_transmission_filter, av.current_mileage_transmission_filter, av.due_mileage_transmission_filter,
                    av.issue_date_differential_oil, av.due_date_differential_oil, av.current_mileage_differential_oil, av.due_mileage_differential_oil,
                    av.battery_issue_date, av.battery_due_date,
                    av.flusing_issue_date, av.flusing_due_date, av.fuel_tank_flush, av.radiator_flush,
                    av.greasing_issue_date, av.greasing_due_date,
                    av.trs_and_suspension, av.engine_part, av.steering_lever_Pts, av.wash, av.oil_level_check, av.lubrication_of_parts,
                    av.air_cleaner, av.fuel_filter, av.french_chalk, av.tr_adjustment,
                    av.overhaul_current_milage, av.overhaul_due_milage, av.overhaul_remarks_input,
                    u.name AS created_by,
                    av.created_at
                FROM all_vehicles av
                LEFT JOIN users u ON av.created_by = u.id  -- Joining users table to get the name
                WHERE av.is_deleted = 0 
                ORDER BY av.created_at DESC;"""
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()
            all_vehicles = [dict(zip(columns, row)) for row in rows]
            self.db_disconnect(conn, cursor)
            return all_vehicles
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_all_vehicle {e}")
            return all_vehicles
        
    def delete_vehicle(self, vehicle_id):
        try:
            conn, cursor = self.db_connect()
            cursor.execute("""
                UPDATE all_vehicles
                SET is_deleted = ?
                WHERE id = ?
            """, (1, vehicle_id))
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: delete_vehicle {e}")
            return False

    def insert_vehicle(self, data):
        try:
            """ Inserts vehicle data into SQLite Database """
            conn, cursor = self.db_connect()
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
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
                    created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            values = tuple(data.values())
            cursor.execute(sql, values)
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: insert_vehicle {e}")
            return False
        
    def update_vehicle(self, data, vehicle_id):
        try:
            """ Updates vehicle data in SQLite Database """
            conn, cursor = self.db_connect()
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
                UPDATE all_vehicles
                SET 
                    category = ?, ba_no_input = ?, make_type_input = ?, engine_no_input = ?,
                    issue_date_oil_filter = ?, due_date_oil_filter = ?, current_mileage_oil_filter = ?, due_mileage_oil_filter = ?,
                    issue_date_fuel_filter = ?, due_date_fuel_filter = ?, current_mileage_fuel_filter = ?, due_mileage_fuel_filter = ?,
                    issue_date_air_filter = ?, due_date_air_filter = ?, current_mileage_air_filter = ?, due_mileage_air_filter = ?,
                    issue_date_transmission_filter = ?, due_date_transmission_filter = ?, current_mileage_transmission_filter = ?, due_mileage_transmission_filter = ?,
                    issue_date_differential_oil = ?, due_date_differential_oil = ?, current_mileage_differential_oil = ?, due_mileage_differential_oil = ?,
                    battery_issue_date = ?, battery_due_date = ?,
                    flusing_issue_date = ?, flusing_due_date = ?, fuel_tank_flush = ?, radiator_flush = ?,
                    greasing_issue_date = ?, greasing_due_date = ?,
                    trs_and_suspension = ?, engine_part = ?, steering_lever_Pts = ?, wash = ?, oil_level_check = ?, lubrication_of_parts = ?,
                    air_cleaner = ?, fuel_filter = ?, french_chalk = ?, tr_adjustment = ?,
                    overhaul_current_milage = ?, overhaul_due_milage = ?, overhaul_remarks_input = ?,
                    updated_by = ?, updated_at = ?
                WHERE id = ?"""
            vehicle_data_with_id = tuple(data.values()) + (vehicle_id,)
            cursor.execute(sql, vehicle_data_with_id)
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: update_vehicle {e}")
            return False