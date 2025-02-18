# import sqlite3, traceback
# import mysql.connector
# import MySQLdb as mdb
# import sys, os

# class VMS_DB1:
#     def __init__(self) -> None:
#         self.host = "BIlal_PC"
#         self.user = "44_AK_HB_DB_User"
#         self.password = "Here2enter!123"
#         self.database = "44_AK_HB_DB"

#     def db_connect(self):
#         try:
#             conn = mdb.connect(self.host, self.user, self.password, self.database)
#             cursor = conn.cursor()
#             if conn:
#                 print("Connected to MySQL database")
#             return conn, cursor
#         except Exception as err:
#             print(f"Error: {err}")
#             return None, None


#     def db_disconnect(self, conn, cursor):
#         if conn:
#             cursor.close()
#             conn.close()
#             print("Connection closed.")

#     def get_user_by_username(self, username):
#         """Fetch a user by username."""
#         conn, cursor = self.db_connect()
#         cursor.execute("SELECT id, username, password, is_blocked FROM users WHERE username = %s", (username,))
#         user = cursor.fetchone()
#         self.db_disconnect(conn, cursor)
#         return user
    
#     def fetch_users(self):
#         """Fetch a user by username."""
#         conn, cursor = self.db_connect()
#         cursor.execute("SELECT id, name, username, email, is_blocked FROM users ORDER BY created_at ASC")
#         users = cursor.fetchall()
#         self.db_disconnect(conn, cursor)
#         return users  # Returns (id, username, password, is_blocked) or None
    
#     def insert_user(self, name, email, username, password, is_blocked=0):
#         """ Inserts user into SQLite Database """
#         conn, cursor = self.db_connect()
#         cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (%s, %s, %s, %s, %s)", 
#                        (name, email, username, password, is_blocked))
#         conn.commit()
#         self.db_disconnect(conn, cursor)
#         return True

#     def delete_user(self, id):
#         """ Deletes a user from SQLite Database based on user ID """
#         conn, cursor = self.db_connect()
#         cursor.execute("DELETE FROM users WHERE id = %s", (id,))
#         conn.commit()
#         self.db_disconnect(conn, cursor)
#         return True

#     def update_user_in_db(self, name, email, username, password, is_blocked, id):
#         """ Update user in the SQLite database """
#         conn, cursor = self.db_connect()
#         cursor.execute("""
#             UPDATE users
#             SET name = %s, email = %s, username = %s, password = %s, is_blocked = %s
#             WHERE id = %s
#         """, (name, email, username, password, is_blocked, id))
#         conn.commit()
#         self.db_disconnect(conn, cursor)
#         return True

#     def fetch_user_by_id(self, user_id):
#         conn, cursor = self.db_connect()
#         cursor.execute("SELECT name, username, email, password, is_blocked FROM users WHERE id=%s", (user_id,))
#         result = cursor.fetchone()
#         self.db_disconnect(conn, cursor)
#         return result  # This should return a tuple with user data


#     # Function to insert data into all_vehicles
#     def insert_vehicle(self, data):
#         try:
#             """ Inserts vehicle data into MySQL Database """
#             conn, cursor = self.db_connect()
#             data = {k: (v if v != "" else None) for k, v in data.items()}
#             sql = """
#                 INSERT INTO all_vehicles (
#                     category, ba_no_input, make_type_input, engine_no_input,
#                     issue_date_oil_filter, due_date_oil_filter, current_mileage_oil_filter, due_mileage_oil_filter,
#                     issue_date_fuel_filter, due_date_fuel_filter, current_mileage_fuel_filter, due_mileage_fuel_filter,
#                     issue_date_air_filter, due_date_air_filter, current_mileage_air_filter, due_mileage_air_filter,
#                     issue_date_transmission_filter, due_date_transmission_filter, current_mileage_transmission_filter, due_mileage_transmission_filter,
#                     issue_date_differential_oil, due_date_differential_oil, current_mileage_differential_oil, due_mileage_differential_oil,
#                     battery_issue_date, battery_due_date,
#                     flusing_issue_date, flusing_due_date, fuel_tank_flush, radiator_flush,
#                     greasing_issue_date, greasing_due_date,
#                     trs_and_suspension, engine_part, steering_lever_Pts, wash, oil_level_check, lubrication_of_parts,
#                     air_cleaner, fuel_filter, french_chalk, tr_adjustment,
#                     overhaul_current_milage, overhaul_due_milage, overhaul_remarks_input,
#                     created_by
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             values = tuple(data.values())
#             cursor.execute(sql, values)
#             conn.commit()
#             self.db_disconnect(conn, cursor)
#             return True
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception: insert_vehicle {e}")
#             return False
        
#     # Function to insert data into all_vehicles
#     def update_vehicle(self, data, vehicle_id):
#         try:
#             """ Inserts vehicle data into MySQL Database """
#             conn, cursor = self.db_connect()
#             data = {k: (v if v != "" else None) for k, v in data.items()}
#             sql = """
#                 UPDATE all_vehicles
#                 SET 
#                     category = %s, ba_no_input = %s, make_type_input = %s, engine_no_input = %s,
#                     issue_date_oil_filter = %s, due_date_oil_filter = %s, current_mileage_oil_filter = %s, due_mileage_oil_filter = %s,
#                     issue_date_fuel_filter = %s, due_date_fuel_filter = %s, current_mileage_fuel_filter = %s, due_mileage_fuel_filter = %s,
#                     issue_date_air_filter = %s, due_date_air_filter = %s, current_mileage_air_filter = %s, due_mileage_air_filter = %s,
#                     issue_date_transmission_filter = %s, due_date_transmission_filter = %s, current_mileage_transmission_filter = %s, due_mileage_transmission_filter = %s,
#                     issue_date_differential_oil = %s, due_date_differential_oil = %s, current_mileage_differential_oil = %s, due_mileage_differential_oil = %s,
#                     battery_issue_date = %s, battery_due_date = %s,
#                     flusing_issue_date = %s, flusing_due_date = %s, fuel_tank_flush = %s, radiator_flush = %s,
#                     greasing_issue_date = %s, greasing_due_date = %s,
#                     trs_and_suspension = %s, engine_part = %s, steering_lever_Pts = %s, wash = %s, oil_level_check = %s, lubrication_of_parts = %s,
#                     air_cleaner = %s, fuel_filter = %s, french_chalk = %s, tr_adjustment = %s,
#                     overhaul_current_milage = %s, overhaul_due_milage = %s, overhaul_remarks_input = %s,
#                     updated_by = %s, updated_at = %s
#                 WHERE id = %s
#             """
#             vehicle_data_with_id = tuple(data.values()) + (vehicle_id,)
#             cursor.execute(sql, vehicle_data_with_id)
#             conn.commit()
#             self.db_disconnect(conn, cursor)
#             return True
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception: insert_vehicle {e}")
#             return False
        
#     # Function to insert data into all_vehicles
#     def get_all_vehicle(self):
#         try:
#             all_vehicles = ()
#             """ Inserts vehicle data into MySQL Database """
#             conn, cursor = self.db_connect()
#             sql = """SELECT 
#                     av.id, av.category, av.ba_no_input, av.make_type_input, av.engine_no_input,
#                     av.issue_date_oil_filter, av.due_date_oil_filter, av.current_mileage_oil_filter, av.due_mileage_oil_filter,
#                     av.issue_date_fuel_filter, av.due_date_fuel_filter, av.current_mileage_fuel_filter, av.due_mileage_fuel_filter,
#                     av.issue_date_air_filter, av.due_date_air_filter, av.current_mileage_air_filter, av.due_mileage_air_filter,
#                     av.issue_date_transmission_filter, av.due_date_transmission_filter, av.current_mileage_transmission_filter, av.due_mileage_transmission_filter,
#                     av.issue_date_differential_oil, av.due_date_differential_oil, av.current_mileage_differential_oil, av.due_mileage_differential_oil,
#                     av.battery_issue_date, av.battery_due_date,
#                     av.flusing_issue_date, av.flusing_due_date, av.fuel_tank_flush, av.radiator_flush,
#                     av.greasing_issue_date, av.greasing_due_date,
#                     av.trs_and_suspension, av.engine_part, av.steering_lever_Pts, av.wash, av.oil_level_check, av.lubrication_of_parts,
#                     av.air_cleaner, av.fuel_filter, av.french_chalk, av.tr_adjustment,
#                     av.overhaul_current_milage, av.overhaul_due_milage, av.overhaul_remarks_input,
#                     u.name AS created_by,
#                     av.created_at
#                 FROM all_vehicles av
#                 LEFT JOIN users u ON av.created_by = u.id  -- Joining users table to get the name
#                 WHERE av.is_deleted = 0 
#                 ORDER BY av.created_at DESC;"""
#             cursor.execute(sql)
#             columns = [desc[0] for desc in cursor.description]  # Get column names
#             rows = cursor.fetchall()
#             all_vehicles = [dict(zip(columns, row)) for row in rows]
#             self.db_disconnect(conn, cursor)
#             return all_vehicles
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception: get_all_vehicle {e}")
#             return all_vehicles

#     def delete_vehicle(self, vehicle_id):
#         try:
#             conn, cursor = self.db_connect()
#             cursor.execute("""
#                 UPDATE all_vehicles
#                 SET is_deleted = %s
#                 WHERE id = %s
#             """, (1, vehicle_id))
#             conn.commit()
#             self.db_disconnect(conn, cursor)
#             return True
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception: get_all_vehicle {e}")
#             return False

#************************************************************************************************************

import sqlite3, sys, os, traceback, shutil
DB_NAME = "vms44AKDB.db"
class VMS_DB:
    def __init__(self) -> None:
        self.db_path = self.get_database_path()

    def get_writable_directory(self, app_name="MyApp"):
        # Choose a directory that is writable by the current user.
        if sys.platform == "win32":
            # For Windows, use the APPDATA folder
            base_dir = os.getenv("APPDATA")
        elif sys.platform == "darwin":
            # For macOS, use the user's Application Support folder
            base_dir = os.path.expanduser("~/Library/Application Support")
        else:
            # For Linux and other UNIX systems, use ~/.local/share
            base_dir = os.path.expanduser("~/.local/share")
        print("base_dir:",base_dir)
        app_dir = os.path.join(base_dir, app_name)
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        print("app_dir:",app_dir)
        return app_dir
    

    def get_database_path(self):
        db_filename = "vms44AKDB.db"
        
        if getattr(sys, 'frozen', False):
            # When frozen, the bundled database is located in sys._MEIPASS.
            bundled_db_path = os.path.join(sys._MEIPASS, db_filename)
            # Define a permanent (writable) directory for the database.
            permanent_dir = self.get_writable_directory("44_AK_VMS")  # change "MyApp" to your app name
            permanent_db_path = os.path.join(permanent_dir, db_filename)
            # If the permanent copy doesn't exist, copy it from the bundled location.
            if not os.path.exists(permanent_db_path):
                try:
                    shutil.copy2(bundled_db_path, permanent_db_path)
                except Exception as e:
                    raise RuntimeError(f"Failed to copy database file: {e}")
            return permanent_db_path
        else:
            # Running in development mode—use the local file.
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), db_filename)


    # def get_database_path(self):
    #     """Returns the correct database path, whether running as script or executable."""
    #     if getattr(sys, 'frozen', False):  # If running as an executable (PyInstaller)
    #         base_path = sys._MEIPASS
    #     else:
    #         base_path = os.path.dirname(os.path.abspath(__file__))  # Normal script execution
        
    #     return os.path.join(base_path, "vms44AKDB.db") 

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
        """Fetch all users"""
        conn, cursor = self.db_connect()
        cursor.execute("SELECT id, name, username, is_blocked FROM users ORDER BY created_at ASC")
        users = cursor.fetchall()
        self.db_disconnect(conn, cursor)
        return users  # Returns (id, username, password, is_blocked) or None
    
    def insert_user(self, name, username, password, is_blocked=0):
        """ Inserts user into SQLite Database """
        conn, cursor = self.db_connect()
        cursor.execute("INSERT INTO users (name, username, password, is_blocked) VALUES (?, ?, ?, ?)", 
                       (name, username, password, is_blocked))
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

    def update_user_in_db(self, name, username, password, is_blocked, id):
        """ Update user in the SQLite database """
        conn, cursor = self.db_connect()
        cursor.execute("""
            UPDATE users
            SET name = ?, username = ?, password = ?, is_blocked = ?
            WHERE id = ?
        """, (name, username, password, is_blocked, id))
        conn.commit()
        self.db_disconnect(conn, cursor)
        return True

    def fetch_user_by_id(self, user_id):
        conn, cursor = self.db_connect()
        cursor.execute("SELECT name, username, password, is_blocked FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        self.db_disconnect(conn, cursor)
        return result
    
    def get_all_vehicle(self, page=0, page_size=10):
        try:
            all_vehicles = []
            conn, cursor = self.db_connect()
            if page_size:
                offset = page * page_size
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
                    ORDER BY av.created_at DESC
                    LIMIT ? OFFSET ?;"""
                cursor.execute(sql, (page_size, offset))
            else:
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
            return []
        
    def get_vehicle_summary(self, page=0, page_size=10):
        try:
            all_vehicles = []
            conn, cursor = self.db_connect()
            offset = page * page_size
            sql = """SELECT 
                    av.id, av.category, av.ba_no_input, av.make_type_input, av.overhaul_remarks_input
                FROM all_vehicles av
                WHERE av.is_deleted = 0 
                ORDER BY av.created_at DESC
                LIMIT ? OFFSET ?;"""
            cursor.execute(sql, (page_size, offset))
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()
            all_vehicles = [dict(zip(columns, row)) for row in rows]
            self.db_disconnect(conn, cursor)
            return all_vehicles
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_all_vehicle {e}")
            return []
        
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
        
    def get_vehicle_count(self):
        try:
            conn, cursor = self.db_connect()
            sql = """
                SELECT 
                    COUNT(*) AS total_count,
                    SUM(CASE WHEN category = 'A' THEN 1 ELSE 0 END) AS category_a_count,
                    SUM(CASE WHEN category = 'B' THEN 1 ELSE 0 END) AS category_b_count,
                    SUM(CASE WHEN overhaul_remarks_input = 'Fit' THEN 1 ELSE 0 END) AS status_fit_count,
                    SUM(CASE WHEN overhaul_remarks_input = 'Unfit' THEN 1 ELSE 0 END) AS status_unfit_count
                FROM all_vehicles 
                WHERE is_deleted = 0;
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            counts = {
                "total": result[0],
                "category_A": result[1],
                "category_B": result[2],
                "fit_vehicle": result[3],
                "unfit_vehicle": result[4],
            }
            self.db_disconnect(conn, cursor)
            return counts
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_vehicle_count {e}")
            return 0

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
        
    #******************************************************************************************************************************************************
    
    def get_all_weapons(self, page=0, page_size=10):
        try:
            all_vehicles = []
            conn, cursor = self.db_connect()
            if page_size:
                offset = page * page_size
                sql = """SELECT 
                        av.ID as id, av.Wpn_No,
                        av.T_Pod_Leg_lock_handle, av.T_Pod_Anchor_claw, av.T_Pod_Leveling_Bubbles, av.T_Pod_Lubrication, av.T_Pod_Pull_tube, 
                        av.T_Pod_Detent_stop_lever, av.T_Pod_Foot_pad_legs_body_condition,
                        av.T_Unit_Traversing_Lock, av.T_Unit_Elevation_lock_check, av.T_Unit_Elevation_lock_handle, av.T_Unit_Viscosity_of_Viscos_damper,
                        av.T_Unit_Azimuth_lock_check, av.T_Unit_Lubrication, av.T_Unit_Protective_cover, av.T_Unit_Coil_Card,
                        av.OS_Eye_Shield, av.OS_Focusing_knob, av.OS_Sillica_gel_condition, av.OS_Reticle_lamp, av.OS_Body_condition,
                        av.OS_N2_purg_filling_connection, av.OS_Reticle_switch, av.OS_Cable_connector, av.OS_Locking_device, av.OS_Lens_cover, av.OS_Objective_lens,
                        av.DMGS_Meter_indicator_AZ_Elev, av.DMGS_Sockets, av.DMGS_MGS_DMGS_case, av.DMGS_Protective_cover, av.DMGS_Cable,
                        av.DMGS_Bty_connector, av.DMGS_Self_test, av.L_Tube_Body_Condition, av.TVPC_Body_Condition, av.TVPC_Fly_Net, av.TVPC_On_Off_Switch,
                        av.TVPC_Indicator_It, av.TVPC_Connector, av.TVPC_Voltage, av.Bty_BB_287_Bty_connector, av.Bty_BB_287_Voltage_24V_sec, av.Bty_BB_287_Voltage_50V,
                        av.Bty_BB_287_Voltage_50V_sec, av.Bty_BB_287_Bty_condition, av.Bty_BB_287_Bty_Tvpc, av.Bty_BB_287_Power_cable_condition, av.NVS_Coolant_unit,
                        av.NVS_Eye_piece, av.NVS_Cable_connector, av.NVS_Lens_assy, av.NVS_Power_cable_condition, av.BPC_Body, av.BPC_Cables,
                        av.BPC_On_Off_Switch, av.VPC_Body, av.VPC_Switch, av.VPC_VPC_Power_Cable, av.L_Bty_Bty_Voltage, av.Doc_6_Monthly_verification_record,
                        av.Doc_Last_ATI_pts_has_been_killed, av.Doc_Bty_charging_record, av.Doc_Storage_temp_Humidity_record, av.Doc_Firing_record_check,
                        av.Doc_Svc_ability_Completeness_of_tools_accy, av.Doc_Self_test_record_check, av.Doc_Is_eARMS_fully_func, av.Doc_Complete_eqpt_inventory_update_on_eARMS,
                        av.Doc_DRWO_work_order_being_processed_on_eARMS, av.Doc_Are_Log_book_maintain_properly,
                        av.Status, u.name AS created_by, av.created_at
                    FROM all_weapons av 
                    LEFT JOIN users u ON av.created_by = u.id
                    WHERE av.is_deleted = 0 
                    ORDER BY av.created_at DESC
                    LIMIT ? OFFSET ?;"""
                cursor.execute(sql, (page_size, offset))
            else:
                sql = """SELECT 
                        av.ID as id, av.Wpn_No,
                        av.T_Pod_Leg_lock_handle, av.T_Pod_Anchor_claw, av.T_Pod_Leveling_Bubbles, av.T_Pod_Lubrication, av.T_Pod_Pull_tube, 
                        av.T_Pod_Detent_stop_lever, av.T_Pod_Foot_pad_legs_body_condition,
                        av.T_Unit_Traversing_Lock, av.T_Unit_Elevation_lock_check, av.T_Unit_Elevation_lock_handle, av.T_Unit_Viscosity_of_Viscos_damper,
                        av.T_Unit_Azimuth_lock_check, av.T_Unit_Lubrication, av.T_Unit_Protective_cover, av.T_Unit_Coil_Card,
                        av.OS_Eye_Shield, av.OS_Focusing_knob, av.OS_Sillica_gel_condition, av.OS_Reticle_lamp, av.OS_Body_condition,
                        av.OS_N2_purg_filling_connection, av.OS_Reticle_switch, av.OS_Cable_connector, av.OS_Locking_device, av.OS_Lens_cover, av.OS_Objective_lens,
                        av.DMGS_Meter_indicator_AZ_Elev, av.DMGS_Sockets, av.DMGS_MGS_DMGS_case, av.DMGS_Protective_cover, av.DMGS_Cable,
                        av.DMGS_Bty_connector, av.DMGS_Self_test, av.L_Tube_Body_Condition, av.TVPC_Body_Condition, av.TVPC_Fly_Net, av.TVPC_On_Off_Switch,
                        av.TVPC_Indicator_It, av.TVPC_Connector, av.TVPC_Voltage, av.Bty_BB_287_Bty_connector, av.Bty_BB_287_Voltage_24V_sec, av.Bty_BB_287_Voltage_50V,
                        av.Bty_BB_287_Voltage_50V_sec, av.Bty_BB_287_Bty_condition, av.Bty_BB_287_Bty_Tvpc, av.Bty_BB_287_Power_cable_condition, av.NVS_Coolant_unit,
                        av.NVS_Eye_piece, av.NVS_Cable_connector, av.NVS_Lens_assy, av.NVS_Power_cable_condition, av.BPC_Body, av.BPC_Cables,
                        av.BPC_On_Off_Switch, av.VPC_Body, av.VPC_Switch, av.VPC_VPC_Power_Cable, av.L_Bty_Bty_Voltage, av.Doc_6_Monthly_verification_record,
                        av.Doc_Last_ATI_pts_has_been_killed, av.Doc_Bty_charging_record, av.Doc_Storage_temp_Humidity_record, av.Doc_Firing_record_check,
                        av.Doc_Svc_ability_Completeness_of_tools_accy, av.Doc_Self_test_record_check, av.Doc_Is_eARMS_fully_func, av.Doc_Complete_eqpt_inventory_update_on_eARMS,
                        av.Doc_DRWO_work_order_being_processed_on_eARMS, av.Doc_Are_Log_book_maintain_properly,
                        av.Status, u.name AS created_by, av.created_at
                    FROM all_weapons av 
                    LEFT JOIN users u ON av.created_by = u.id
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
            print(f"Exception: get_all_weapons {e}")
            return []


    def insert_weapon(self, data):
        try:
            """ Inserts vehicle data into SQLite Database """
            conn, cursor = self.db_connect()
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
                INSERT INTO all_weapons (
                Wpn_No,
                T_Pod_Leg_lock_handle, T_Pod_Anchor_claw, T_Pod_Leveling_Bubbles, T_Pod_Lubrication, T_Pod_Pull_tube, T_Pod_Detent_stop_lever, T_Pod_Foot_pad_legs_body_condition,
                T_Unit_Traversing_Lock, T_Unit_Elevation_lock_check, T_Unit_Elevation_lock_handle, T_Unit_Viscosity_of_Viscos_damper, T_Unit_Azimuth_lock_check, T_Unit_Lubrication, T_Unit_Protective_cover, T_Unit_Coil_Card,
                OS_Eye_Shield, OS_Focusing_knob, OS_Sillica_gel_condition, OS_Reticle_lamp, OS_Body_condition, OS_N2_purg_filling_connection, OS_Reticle_switch, OS_Cable_connector, OS_Locking_device, OS_Lens_cover, OS_Objective_lens,
                DMGS_Meter_indicator_AZ_Elev, DMGS_Sockets, DMGS_MGS_DMGS_case, DMGS_Protective_cover, DMGS_Cable, DMGS_Bty_connector, DMGS_Self_test,
                L_Tube_Body_Condition,
                TVPC_Body_Condition, TVPC_Fly_Net, TVPC_On_Off_Switch, TVPC_Indicator_It, TVPC_Connector, TVPC_Voltage,
                Bty_BB_287_Bty_connector, Bty_BB_287_Voltage_24V_sec, Bty_BB_287_Voltage_50V, Bty_BB_287_Voltage_50V_sec, Bty_BB_287_Bty_condition, Bty_BB_287_Bty_Tvpc, Bty_BB_287_Power_cable_condition,
                NVS_Coolant_unit, NVS_Eye_piece, NVS_Cable_connector, NVS_Lens_assy, NVS_Power_cable_condition, 
                BPC_Body, BPC_Cables, BPC_On_Off_Switch,
                VPC_Body, VPC_Switch, VPC_VPC_Power_Cable,
                L_Bty_Bty_Voltage,
                Doc_6_Monthly_verification_record, Doc_Last_ATI_pts_has_been_killed, Doc_Bty_charging_record, Doc_Storage_temp_Humidity_record, Doc_Firing_record_check, Doc_Svc_ability_Completeness_of_tools_accy, 
                Doc_Self_test_record_check, Doc_Is_eARMS_fully_func, Doc_Complete_eqpt_inventory_update_on_eARMS, Doc_DRWO_work_order_being_processed_on_eARMS, Doc_Are_Log_book_maintain_properly,
                Status, created_by
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
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
        
    
    def update_weapon(self, data, weapon_id):
        try:
            """ Updates vehicle data in SQLite Database """
            conn, cursor = self.db_connect()
            data = {k: (v if v != "" else None) for k, v in data.items()}
            sql = """
                UPDATE all_weapons SET
                Wpn_No = ?,
                T_Pod_Leg_lock_handle = ?, T_Pod_Anchor_claw = ?, T_Pod_Leveling_Bubbles = ?, T_Pod_Lubrication = ?, T_Pod_Pull_tube = ?, 
                T_Pod_Detent_stop_lever = ?, T_Pod_Foot_pad_legs_body_condition = ?,
                T_Unit_Traversing_Lock = ?, T_Unit_Elevation_lock_check = ?, T_Unit_Elevation_lock_handle = ?, T_Unit_Viscosity_of_Viscos_damper = ?, 
                T_Unit_Azimuth_lock_check = ?, T_Unit_Lubrication = ?, T_Unit_Protective_cover = ?, T_Unit_Coil_Card = ?,
                OS_Eye_Shield = ?, OS_Focusing_knob = ?, OS_Sillica_gel_condition = ?, OS_Reticle_lamp = ?, OS_Body_condition = ?, OS_N2_purg_filling_connection = ?,
                OS_Reticle_switch = ?, OS_Cable_connector = ?, OS_Locking_device = ?, OS_Lens_cover = ?, OS_Objective_lens = ?,
                DMGS_Meter_indicator_AZ_Elev = ?, DMGS_Sockets = ?, DMGS_MGS_DMGS_case = ?, DMGS_Protective_cover = ?, DMGS_Cable = ?, DMGS_Bty_connector = ?, DMGS_Self_test = ?,
                L_Tube_Body_Condition = ?,
                TVPC_Body_Condition = ?, TVPC_Fly_Net = ?, TVPC_On_Off_Switch = ?, TVPC_Indicator_It = ?, TVPC_Connector = ?, TVPC_Voltage = ?,
                Bty_BB_287_Bty_connector = ?, Bty_BB_287_Voltage_24V_sec = ?, Bty_BB_287_Voltage_50V = ?, Bty_BB_287_Voltage_50V_sec = ?, Bty_BB_287_Bty_condition = ?, Bty_BB_287_Power_cable_condition = ?,
                NVS_Coolant_unit = ?, NVS_Eye_piece = ?, NVS_Cable_connector = ?, NVS_Lens_assy = ?, NVS_Power_cable_condition = ?,
                BPC_Body = ?, BPC_Cables = ?, BPC_On_Off_Switch = ?,
                VPC_Body = ?, VPC_Switch = ?, VPC_VPC_Power_Cable = ?,
                L_Bty_Bty_Voltage = ?,
                Doc_6_Monthly_verification_record = ?, Doc_Last_ATI_pts_has_been_killed = ?, Doc_Bty_charging_record = ?, Doc_Storage_temp_Humidity_record = ?,
                Doc_Firing_record_check = ?, Doc_Svc_ability_Completeness_of_tools_accy = ?, Doc_Self_test_record_check = ?, Doc_Is_eARMS_fully_func = ?, Doc_Complete_eqpt_inventory_update_on_eARMS = ?,
                Doc_DRWO_work_order_being_processed_on_eARMS = ?, Doc_Are_Log_book_maintain_properly = ?,
                Status = ?,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = ?
            WHERE ID = ?;"""
            weapon_data_with_id = tuple(data.values()) + (weapon_id,)
            cursor.execute(sql, weapon_data_with_id)
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: update_weapon {e}")
            return False
        
    def get_weapon_count(self):
        try:
            conn, cursor = self.db_connect()
            sql = """
                SELECT 
                    COUNT(*) AS total_count,
                    SUM(CASE WHEN Status = 'Svc' THEN 1 ELSE 0 END) AS status_fit_count,
                    SUM(CASE WHEN Status = 'Unsvc' THEN 1 ELSE 0 END) AS status_unfit_count
                FROM all_weapons 
                WHERE is_deleted = 0;
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            counts = {
                "total": result[0],
                "fit_weapon": result[1],
                "unfit_weapon": result[2],
            }
            self.db_disconnect(conn, cursor)
            return counts
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: get_weapon_count {e}")
            return 0
        

    def delete_weapon(self, weapon_id):
        try:
            conn, cursor = self.db_connect()
            cursor.execute("""
                UPDATE all_weapons
                SET is_deleted = ?
                WHERE id = ?
            """, (1, weapon_id))
            conn.commit()
            self.db_disconnect(conn, cursor)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: delete_weapon {e}")
            return False