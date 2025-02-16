import sqlite3

# # Connect to the database (or create it if it doesn't exist)
# conn = sqlite3.connect("vms44AKDB.db")

# # Create a cursor object to execute SQL commands
# cursor = conn.cursor()

# # Create users table
# cursor.execute("""
# Select count (*) from all_vehicles where is_deleted = 0;
# """)

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# print("Users table created successfully!")


# def insert_user(name, email, username, password, is_blocked=0):
#     conn = sqlite3.connect("vms44AKDB.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
#                    (name, email, username, password, is_blocked))
#     conn.commit()
#     conn.close()

# # insert_user("Zia Shahid", "zia@outlook.com", "ziashahid", "Zia", 1)
# # print("User inserted successfully!")


# def insert_vehicle():
#     conn = sqlite3.connect("vms44AKDB.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO all_vehicles (
#             category, ba_no_input, make_type_input, engine_no_input,
#             issue_date_oil_filter, due_date_oil_filter, current_mileage_oil_filter, due_mileage_oil_filter,
#             issue_date_fuel_filter, due_date_fuel_filter, current_mileage_fuel_filter, due_mileage_fuel_filter,
#             issue_date_air_filter, due_date_air_filter, current_mileage_air_filter, due_mileage_air_filter,
#             issue_date_transmission_filter, due_date_transmission_filter, current_mileage_transmission_filter, due_mileage_transmission_filter,
#             issue_date_differential_oil, due_date_differential_oil, current_mileage_differential_oil, due_mileage_differential_oil,
#             battery_issue_date, battery_due_date, flusing_issue_date, flusing_due_date,
#             fuel_tank_flush, radiator_flush, greasing_issue_date, greasing_due_date,
#             trs_and_suspension, engine_part, steering_lever_Pts, wash,
#             oil_level_check, lubrication_of_parts, air_cleaner, fuel_filter,
#             french_chalk, tr_adjustment, overhaul_current_milage, overhaul_due_milage,
#             overhaul_remarks_input, created_by, updated_by, created_at, updated_at, deleted_at, is_deleted
#         ) VALUES (
#             'SUV', 'BA123', 'Toyota', 'ENG456',
#             '2024-02-01', '2025-02-01', '15000', '30000',
#             '2024-03-01', '2025-03-01', '16000', '32000',
#             '2024-04-01', '2025-04-01', '17000', '34000',
#             '2024-05-01', '2025-05-01', '18000', '36000',
#             '2024-06-01', '2025-06-01', '19000', '38000',
#             '2024-07-01', '2025-07-01', '20000', '40000',
#             '2024-08-01', '2025-08-01', '2024-09-01', '2025-09-01',
#             'Yes', 'No', '2024-10-01', '2025-10-01',
#             'Good', 'Operational', 'Stable', 'Yes',
#             'Checked', 'Lubricated', 'Clean', 'Changed',
#             'Applied', 'Adjusted', '25000', '50000',
#             'No remarks', '1', 'Admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, 0
#         )
#     """)
#     conn.commit()
#     conn.close()
#     print("User inserted successfully!")

# insert_vehicle()

# pyinstaller --onefile --windowed --icon=app_icon.ico --add-data "assets;assets" --add-data "vms44AKDB.db;." main.py

from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont

app = QApplication([])

table = QTableWidget(3, 3)  # Create a table with 3 rows and 3 columns
font = QFont("Arial", 16)  # Set font size to 14

# Apply font to all cells
for row in range(table.rowCount()): 
    for col in range(table.columnCount()):
        item = QTableWidgetItem(f"Cell {row},{col}")
        item.setFont(font)  # Set font size
        table.setItem(row, col, item)

table.show()
app.exec_()
