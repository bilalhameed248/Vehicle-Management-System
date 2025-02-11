# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDateEdit
# from PyQt5.QtCore import QDate
# from PyQt5.QtGui import QIcon
# from controllers.load_assets import *

# class CalendarWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         issue_layout = QVBoxLayout()
#         issue_layout.addWidget(QLabel("Issue Date:"))

#         issue_date = QDateEdit()
#         issue_date.setCalendarPopup(True)
#         issue_date.setDate(QDate.currentDate())
#         issue_date.setMinimumDate(QDate.currentDate().addYears(-5))
#         issue_date.setMaximumDate(QDate.currentDate().addYears(5))
#         issue_date.setDisplayFormat("dd-MM-yyyy")

#         calendar_icon_path = get_asset_path("assets/icons/calendar.png")

#         # Apply Stylesheet with Calendar Icon
#         issue_date.setStyleSheet(f"""
#             QDateEdit {{ border: 2px solid #0078D7; border-radius: 5px; padding: 5px; background-color: white; font-size: 14px; }}
#             QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; }}
#             QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path});}}
#             QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
#             QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
#             QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
#             QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
#             QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white;}}
#         """)

#         issue_layout.addWidget(issue_date)
#         self.setLayout(issue_layout)

# app = QApplication([])
# window = CalendarWidget()
# window.show()
# app.exec_()

# CREATE TABLE "all_vehicles" (
#   "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "category" TEXT DEFAULT NULL,
#   "ba_no_input" TEXT DEFAULT NULL,
#   "make_type_input" TEXT DEFAULT NULL,
#   "engine_no_input" TEXT DEFAULT NULL,
#   "issue_date_oil_filter" DATE DEFAULT NULL,
#   "due_date_oil_filter" DATE DEFAULT NULL,
#   "current_mileage_oil_filter" TEXT DEFAULT NULL,
#   "due_mileage_oil_filter" TEXT DEFAULT NULL,
#   "issue_date_fuel_filter" DATE DEFAULT NULL,
#   "due_date_fuel_filter" DATE DEFAULT NULL,
#   "current_mileage_fuel_filter" TEXT DEFAULT NULL,
#   "due_mileage_fuel_filter" TEXT DEFAULT NULL,
#   "issue_date_air_filter" DATE DEFAULT NULL,
#   "due_date_air_filter" DATE DEFAULT NULL,
#   "current_mileage_air_filter" TEXT DEFAULT NULL,
#   "due_mileage_air_filter" TEXT DEFAULT NULL,
#   "issue_date_transmission_filter" DATE DEFAULT NULL,
#   "due_date_transmission_filter" DATE DEFAULT NULL,
#   "current_mileage_transmission_filter" TEXT DEFAULT NULL,
#   "due_mileage_transmission_filter" TEXT DEFAULT NULL,
#   "issue_date_differential_oil" DATE DEFAULT NULL,
#   "due_date_differential_oil" DATE DEFAULT NULL,
#   "current_mileage_differential_oil" TEXT DEFAULT NULL,
#   "due_mileage_differential_oil" TEXT DEFAULT NULL,
#   "battery_issue_date" DATE DEFAULT NULL,
#   "battery_due_date" DATE DEFAULT NULL,
#   "flusing_issue_date" DATE DEFAULT NULL,
#   "flusing_due_date" DATE DEFAULT NULL,
#   "fuel_tank_flush" TEXT DEFAULT NULL,
#   "radiator_flush" TEXT DEFAULT NULL,
#   "greasing_issue_date" DATE DEFAULT NULL,
#   "greasing_due_date" DATE DEFAULT NULL,
#   "trs_and_suspension" TEXT DEFAULT NULL,
#   "engine_part" TEXT DEFAULT NULL,
#   "steering_lever_Pts" TEXT DEFAULT NULL,
#   "wash" TEXT DEFAULT NULL,
#   "oil_level_check" TEXT DEFAULT NULL,
#   "lubrication_of_parts" TEXT DEFAULT NULL,
#   "air_cleaner" TEXT DEFAULT NULL,
#   "fuel_filter" TEXT DEFAULT NULL,
#   "french_chalk" TEXT DEFAULT NULL,
#   "tr_adjustment" TEXT DEFAULT NULL,
#   "overhaul_current_milage" TEXT DEFAULT NULL,
#   "overhaul_due_milage" TEXT DEFAULT NULL,
#   "overhaul_remarks_input" TEXT DEFAULT NULL,
#   "created_by" TEXT DEFAULT NULL,
#   "updated_by" TEXT DEFAULT NULL,
#   "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   "deleted_at" TIMESTAMP DEFAULT NULL,
#   "is_deleted" INTEGER DEFAULT 0
# );