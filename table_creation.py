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



from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QVBoxLayout,
QWidget, QLabel, QLineEdit, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy)
from controllers.load_assets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        calendar_icon_path = get_asset_path("assets/icons/calendar.png").replace("\\", "/")
        combo_dd_icon_path = get_asset_path("assets/icons/combo_dd.png").replace("\\", "/")

        self.setStyleSheet(f"""QWidget {{ background-color: #f4f4f4; font-size: 18px; }}
            QLabel {{ font-weight: bold; }}
            QLineEdit, QTextEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 14px;}}
            QPushButton {{ background-color: #007BFF; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #0056b3; }}
            QPushButton:pressed {{ background-color: #004085; }}
            QGroupBox {{font-weight: bold; border: 2px solid #007BFF; padding: 10px; margin-top: 20px;margin-bottom: 20px; border-radius: 8px; }}
            QGroupBox title {{ color: #007BFF; font-size: 16px; }}
            QScrollBar:vertical {{border: none; background: #f0f0f0; width: 20px; margin: 0px 0px 0px 0px;}}
            QScrollBar::handle:vertical {{background: blue; min-height: 20px; border-radius: 5px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{background: none;}}
            QScrollBar:horizontal {{border: none; background: #f0f0f0; height: 10px; margin: 0px 0px 0px 0px; }}
            QScrollBar::handle:horizontal {{ background: blue; min-width: 20px; border-radius: 5px; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{background: none;}}
            
            QDateEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 14px; }}
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path}); }}
            QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
            QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
            QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
            QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
            QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white; }}

            QComboBox {{ width: 50px; padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 14px; }}
            QComboBox::down-arrow {{ width: 20px; border: none; background: transparent; image: url({combo_dd_icon_path}); }}
            QComboBox QAbstractItemView {{ background-color: white; border: 1px solid #4a90e2; selection-background-color: #4a90e2; selection-color: white;}}
            QComboBox::item {{ padding: 8px; }}
            QComboBox::item:selected {{ background-color: #4a90e2; color: white; }}
        """)

        # Create main layout
        main_layout = QVBoxLayout()

        # Create layout
        basic_dtl_layout = QHBoxLayout()
        
        group_box = QGroupBox("Basic Details")
        group_layout = QVBoxLayout()

        # Create input fields
        self.blocked_combo = QComboBox()
        self.blocked_combo.addItems(["A", "B"])
        self.ba_no_input = QLineEdit()
        self.make_type_input = QLineEdit()
        self.engine_no_input = QLineEdit()

        # Add widgets with spacing
        basic_dtl_layout.addWidget(QLabel("Category:"))
        basic_dtl_layout.addWidget(self.blocked_combo)
        basic_dtl_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        basic_dtl_layout.addWidget(QLabel("BA No:"))
        basic_dtl_layout.addWidget(self.ba_no_input)
        basic_dtl_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        basic_dtl_layout.addWidget(QLabel("Make & Type:"))
        basic_dtl_layout.addWidget(self.make_type_input)
        basic_dtl_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        basic_dtl_layout.addWidget(QLabel("Engine No:"))
        basic_dtl_layout.addWidget(self.engine_no_input)

        group_layout.addLayout(basic_dtl_layout)
        group_box.setLayout(group_layout)

        main_layout.addWidget(group_box)

        # Set layout
        self.setLayout(main_layout)

app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
