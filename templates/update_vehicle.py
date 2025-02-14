from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from database import VMS_DB
from datetime import datetime
from controllers.load_assets import *

class UpdateVehicle(QWidget):

    def __init__(self, user_session=None, data = None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        # print("self.user_id:",self.user_id)
        # print("self.username:",self.username)
        self.main_parent_welcome = parent
        self.data = data
        self.db_obj = VMS_DB() 
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("Vehicle Maintenance Form")
        calendar_icon_path = get_asset_path("assets/icons/calendar.png").replace("\\", "/")
        combo_dd_icon_path = get_asset_path("assets/icons/combo_dd.png").replace("\\", "/")

        self.setStyleSheet(f"""
            QWidget {{ background-color: #f4f4f4; font-size: 18px; }}
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
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path});}}
            QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
            QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
            QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
            QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
            QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white;}}

            QComboBox {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 14px; }}
            QComboBox::down-arrow {{ width: 20px; border: none; background: transparent; image: url({combo_dd_icon_path});}}
            QComboBox QAbstractItemView {{background-color: white;border: 1px solid #4a90e2;selection-background-color: #4a90e2; selection-color: white;}}
            QComboBox::item {{padding: 8px;}}
            QComboBox::item:selected {{background-color: #4a90e2;color: white;}}
        """)

        self.basic_details = {}
        self.maintenance_fields = {}
        self.battery_fields = {}
        self.flusing_fields = {}
        self.greasing_fields = {}
        self.gen_maint_fields = {}
        self.overhaul_fields = {}

        layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.setSpacing(6)

        def add_basic_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    
            
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            combo_layout = QVBoxLayout()
            combo_layout.addWidget(QLabel("Category:"))
            self.blocked_combo = QComboBox()
            self.blocked_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.blocked_combo.addItems(["A", "B"])
            combo_layout.addWidget(self.blocked_combo)

            ba_no_layout = QVBoxLayout()
            ba_no_layout.addWidget(QLabel("BA No:"))
            self.ba_no_input = QLineEdit()
            ba_no_layout.addWidget(self.ba_no_input)

            row1_layout.addLayout(combo_layout)
            row1_layout.addLayout(ba_no_layout)

            row2_layout = QHBoxLayout()

            make_type_layout = QVBoxLayout()
            make_type_layout.addWidget(QLabel("Make & Type:"))
            self.make_type_input = QLineEdit()
            make_type_layout.addWidget(self.make_type_input)

            engine_no_layout = QVBoxLayout()
            engine_no_layout.addWidget(QLabel("Engine No:"))
            self.engine_no_input = QLineEdit()
            engine_no_layout.addWidget(self.engine_no_input)

            row2_layout.addLayout(make_type_layout)
            row2_layout.addLayout(engine_no_layout)

            self.blocked_combo.setCurrentIndex(0 if self.data['Category'] =="A" else 1)
            self.ba_no_input.setText(self.data["BA No."])
            self.make_type_input.setText(self.data["Make Type"])
            self.engine_no_input.setText(self.data["Engine No."])

            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.basic_details[title] = {
                f"category": self.blocked_combo,
                f"ba_no_input": self.ba_no_input,
                f"make_type_input": self.make_type_input,
                f"engine_no_input": self.engine_no_input
            }
        

        def add_maintenance_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    
            
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDisplayFormat("dd-MM-yyyy")
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDisplayFormat("dd-MM-yyyy")
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            current_mileage_layout = QVBoxLayout()
            current_mileage_layout.addWidget(QLabel("Current Mileage:"))
            current_mileage = QLineEdit()
            current_mileage_layout.addWidget(current_mileage)

            due_mileage_layout = QVBoxLayout()
            due_mileage_layout.addWidget(QLabel("Due Mileage:"))
            due_mileage = QLineEdit()
            due_mileage_layout.addWidget(due_mileage)

            row2_layout.addLayout(current_mileage_layout)
            row2_layout.addLayout(due_mileage_layout)

            if title == "Oil Filter":
                issue_date_db = self.data["Issue Date (Oil Filter)"]
                due_date_db = self.data["Due Date (Oil Filter)"]
                issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
                due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
                current_mileage.setText(self.data["Current Mileage (Oil Filter)"])
                due_mileage.setText(self.data["Due Mileage (Oil Filter)"])
                
            if title == "Fuel Filter":
                issue_date_db = self.data["Issue Date (Fuel Filter)"]
                due_date_db = self.data["Due Date (Fuel Filter)"]
                issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
                due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
                current_mileage.setText(self.data["Current Mileage (Fuel Filter)"])
                due_mileage.setText(self.data["Due Mileage (Fuel Filter)"])
            
            if title == "Air Filter":
                issue_date_db = self.data["Issue Date (Air Filter)"]
                due_date_db = self.data["Due Date (Air Filter)"]
                issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
                due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
                current_mileage.setText(self.data["Current Mileage (Air Filter)"])
                due_mileage.setText(self.data["Due Mileage (Air Filter)"])
            
            if title == "Transmission Filter":
                issue_date_db = self.data["Issue Date (Transmission Filter)"]
                due_date_db = self.data["Due Date (Transmission Filter)"]
                issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
                due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
                current_mileage.setText(self.data["Current Mileage (Transmission Filter)"])
                due_mileage.setText(self.data["Due Mileage (Transmission Filter)"])

            if title == "Differential Oil":
                issue_date_db = self.data["Issue Date (Differential Oil)"]
                due_date_db = self.data["Due Date (Differential Oil)"]
                issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
                due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
                current_mileage.setText(self.data["Current Mileage (Differential Oil)"])
                due_mileage.setText(self.data["Due Mileage (Differential Oil)"])

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.maintenance_fields[title] = {
                f"issue_date_{title.lower().replace(' ', '_')}": issue_date,
                f"due_date_{title.lower().replace(' ', '_')}": due_date,
                f"current_mileage_{title.lower().replace(' ', '_')}": current_mileage,
                f"due_mileage_{title.lower().replace(' ', '_')}": due_mileage
            }

    
        def add_battery_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            
            # Create a horizontal layout for the row
            row_layout = QHBoxLayout()

            # Issue Date
            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            battery_issue_date = QDateEdit()
            battery_issue_date.setCalendarPopup(True)
            battery_issue_date.setDisplayFormat("dd-MM-yyyy")
            issue_layout.addWidget(battery_issue_date)

            # Due Date
            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            battery_due_date = QDateEdit()
            battery_due_date.setCalendarPopup(True)
            battery_due_date.setDisplayFormat("dd-MM-yyyy")
            due_layout.addWidget(battery_due_date)

            # Add both to the horizontal layout
            row_layout.addLayout(issue_layout)
            row_layout.addLayout(due_layout)

            issue_date_db = self.data["Battery Issue Date"]
            due_date_db = self.data["Battery Due Date"]
            battery_issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
            battery_due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))

            # Add the row to the group layout
            group_layout.addLayout(row_layout)
            group_box.setLayout(group_layout)
            # Add the group box to the form
            form_layout.addWidget(group_box, row, col, 1, 4)

            self.battery_fields[title] = {
                "battery_issue_date": battery_issue_date,
                "battery_due_date": battery_due_date
            }


        def add_flusing_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDate(QDate.currentDate())
            issue_date.setDisplayFormat("dd-MM-yyyy")
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.currentDate())
            due_date.setDisplayFormat("dd-MM-yyyy")
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            fuel_tank_flush_layout = QVBoxLayout()
            fuel_tank_flush_layout.addWidget(QLabel("Fuel Tank Flush:"))
            fuel_tank_flush = QLineEdit()
            fuel_tank_flush_layout.addWidget(fuel_tank_flush)

            radiator_flush_layout = QVBoxLayout()
            radiator_flush_layout.addWidget(QLabel("Radiator Flush:"))
            radiator_flush = QLineEdit()
            radiator_flush_layout.addWidget(radiator_flush)

            row2_layout.addLayout(fuel_tank_flush_layout)
            row2_layout.addLayout(radiator_flush_layout)

            issue_date_db = self.data["Flushing Issue Date"]
            due_date_db = self.data["Flushing Due Date"]
            issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
            due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
            fuel_tank_flush.setText(self.data["Fuel Tank Flush"])
            radiator_flush.setText(self.data["Radiator Flush"])

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.flusing_fields[title] = {
                "flusing_issue_date": issue_date,
                "flusing_due_date": due_date,
                "fuel_tank_flush": fuel_tank_flush,
                "radiator_flush": radiator_flush
            }
        

        def add_greasing_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDisplayFormat("dd-MM-yyyy")
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDisplayFormat("dd-MM-yyyy")
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            trs_and_suspension_layout = QVBoxLayout()
            trs_and_suspension_layout.addWidget(QLabel("Trs and suspension:"))
            trs_and_suspension = QLineEdit()
            trs_and_suspension_layout.addWidget(trs_and_suspension)

            engine_part_layout = QVBoxLayout()
            engine_part_layout.addWidget(QLabel("Engine parts:"))
            engine_part = QLineEdit()
            engine_part_layout.addWidget(engine_part)

            row2_layout.addLayout(trs_and_suspension_layout)
            row2_layout.addLayout(engine_part_layout)

            steering_lever_Pts_layout = QVBoxLayout()
            steering_lever_Pts_layout.addWidget(QLabel("Steering lever Pts:"))
            steering_lever_Pts = QLineEdit()
            steering_lever_Pts_layout.addWidget(steering_lever_Pts)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(steering_lever_Pts_layout)

            issue_date_db = self.data["Greasing Issue Date"]
            due_date_db = self.data["Greasing Due Date"]
            issue_date.setDate(QDate(issue_date_db.year, issue_date_db.month, issue_date_db.day))
            due_date.setDate(QDate(due_date_db.year, due_date_db.month, due_date_db.day))
            trs_and_suspension.setText(self.data["TRS and Suspension"])
            engine_part.setText(self.data["Engine Part"])
            steering_lever_Pts.setText(self.data["Steering Lever Pts"])

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.greasing_fields[title] = {
                "greasing_issue_date": issue_date,
                "greasing_due_date": due_date,
                "trs_and_suspension": trs_and_suspension,
                "engine_part": engine_part,
                "steering_lever_Pts": steering_lever_Pts
            }


        def add_gen_maint_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            wash_layout = QVBoxLayout()
            wash_layout.addWidget(QLabel("Wash:"))
            wash = QLineEdit()
            wash_layout.addWidget(wash)

            oil_level_check_layout = QVBoxLayout()
            oil_level_check_layout.addWidget(QLabel("Oil Level Check:"))
            oil_level_check = QLineEdit()
            oil_level_check_layout.addWidget(oil_level_check)

            row1_layout.addLayout(wash_layout)
            row1_layout.addLayout(oil_level_check_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            lubrication_of_parts_layout = QVBoxLayout()
            lubrication_of_parts_layout.addWidget(QLabel("Lubrication of parts:"))
            lubrication_of_parts = QLineEdit()
            lubrication_of_parts_layout.addWidget(lubrication_of_parts)

            air_cleaner_layout = QVBoxLayout()
            air_cleaner_layout.addWidget(QLabel("Air Cleaner Maint:"))
            air_cleaner = QLineEdit()
            air_cleaner_layout.addWidget(air_cleaner)

            row2_layout.addLayout(lubrication_of_parts_layout)
            row2_layout.addLayout(air_cleaner_layout)

            row3_layout = QHBoxLayout()

            fuel_filter_layout = QVBoxLayout()
            fuel_filter_layout.addWidget(QLabel("Fuel Filter Maint:"))
            fuel_filter = QLineEdit()
            fuel_filter_layout.addWidget(fuel_filter)

            french_chalk_layout = QVBoxLayout()
            french_chalk_layout.addWidget(QLabel("French chalk:"))
            french_chalk = QLineEdit()
            french_chalk_layout.addWidget(french_chalk)

            row3_layout.addLayout(fuel_filter_layout)
            row3_layout.addLayout(french_chalk_layout)

            row4_layout = QHBoxLayout()
            
            tr_adjustment_layout = QVBoxLayout()
            tr_adjustment_layout.addWidget(QLabel("Tr Adjustment:"))
            tr_adjustment = QLineEdit()
            tr_adjustment_layout.addWidget(tr_adjustment)

            row4_layout.addLayout(tr_adjustment_layout)

            wash.setText(self.data["Wash"])
            oil_level_check.setText(self.data["Oil Level Check"])
            lubrication_of_parts.setText(self.data["Lubrication of Parts"])
            air_cleaner.setText(self.data["Air Cleaner"])
            fuel_filter.setText(self.data["Fuel Filter"])
            french_chalk.setText(self.data["French Chalk"])
            tr_adjustment.setText(self.data["TR Adjustment"])

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.gen_maint_fields[title] = {
                "wash": wash,
                "oil_level_check": oil_level_check,
                "lubrication_of_parts": lubrication_of_parts,
                "air_cleaner": air_cleaner,
                "fuel_filter": fuel_filter,
                "french_chalk": french_chalk,
                "tr_adjustment": tr_adjustment
            }


        def add_overhaul_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    
        
            # Row 1: Current Mileage & Due Mileage
            row1_layout = QHBoxLayout()

            current_mileage_layout = QVBoxLayout()
            current_mileage_layout.addWidget(QLabel("Current Mileage:"))
            overhaul_current_milage = QLineEdit()
            current_mileage_layout.addWidget(overhaul_current_milage)

            due_mileage_layout = QVBoxLayout()
            due_mileage_layout.addWidget(QLabel("Due Mileage:"))
            overhaul_due_milage = QLineEdit()
            due_mileage_layout.addWidget(overhaul_due_milage)

            row1_layout.addLayout(current_mileage_layout)
            row1_layout.addLayout(due_mileage_layout)

            # Row 2: Remarks/Status
            row2_layout = QHBoxLayout()

            coverhaul_remarks_layout = QVBoxLayout()
            coverhaul_remarks_layout.addWidget(QLabel("Remarks/Status:"))
            overhaul_remarks_input = QTextEdit()
            coverhaul_remarks_layout.addWidget(overhaul_remarks_input)

            row2_layout.addLayout(coverhaul_remarks_layout)

            overhaul_current_milage.setText(self.data["Current Milage (Overhaul)"])
            overhaul_due_milage.setText(self.data["Due Milage (Overhaul)"])
            overhaul_remarks_input.setText(self.data["Status"])

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.overhaul_fields[title] = {
                "overhaul_current_milage": overhaul_current_milage,
                "overhaul_due_milage": overhaul_due_milage,
                "overhaul_remarks_input": overhaul_remarks_input if overhaul_remarks_input else "Nothing Mentioned"
            }
        
        # Maintenance Sections
        add_basic_section("Basic Details", 0, 0)
        add_maintenance_section("Oil Filter", 0, 1)
        add_maintenance_section("Fuel Filter", 2, 0)
        add_maintenance_section("Air Filter", 2, 1)
        add_maintenance_section("Transmission Filter", 4, 0)
        add_maintenance_section("Differential Oil", 4, 1)
        add_battery_section("Battery", 6, 0)
        add_greasing_section("Greasing", 8, 0)
        add_flusing_section("Flushing", 8, 1)
        add_gen_maint_section("Gen Maint (Monthly)", 10, 0)
        add_overhaul_section("Overhaul", 10, 1)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(" Update")
        save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        save_button.setIconSize(QSize(20, 20))
        save_button.clicked.connect(self.update_vehicle)

        cancel_button = QPushButton(" Cancel")
        cancel_button.setIcon(QIcon(get_asset_path("assets/icons/cancel.png")))
        cancel_button.setIconSize(QSize(20, 20))
        cancel_button.clicked.connect(self.cancel_button)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        form_container = QWidget()
        form_container.setLayout(form_layout)
        scroll_area.setWidget(form_container)

        # Add widgets to layout
        layout.addWidget(scroll_area)
        layout.addLayout(button_layout)
        self.setLayout(layout)


    def update_vehicle(self):
        """ Inserts user into the database """
        add_Vehicle_data = {}

        if not (self.basic_details['Basic Details']['ba_no_input'].text().strip() and self.basic_details['Basic Details']['make_type_input'].text().strip() and self.basic_details['Basic Details']['engine_no_input'].text().strip()):
            QMessageBox.warning(self, "Error", "BA NO, Make Type & Engine Number are required!")
            return

        for fields in self.basic_details.values():
            for key, widget in fields.items():
                if isinstance(widget, QComboBox):
                    add_Vehicle_data[key] = widget.currentText().strip()
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.maintenance_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()
        
        for fields in self.battery_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.flusing_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.greasing_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.gen_maint_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.overhaul_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()
                elif isinstance(widget, QTextEdit):
                    add_Vehicle_data[key] = widget.toPlainText().strip()

        add_Vehicle_data['updated_by'] = self.user_id
        add_Vehicle_data['updated_at'] = datetime.now()
        
        is_data_inserted = self.db_obj.update_vehicle(add_Vehicle_data, self.data['id'])
        if not is_data_inserted:
            QMessageBox.warning(self, "Failed", "Error while updating the data..! Please Try Again")
            return
        else:
            QMessageBox.information(self, "Success", "Vehicle Updated successfully!")
            self.cancel_button()

    def cancel_button(self):
        if hasattr(self.main_parent_welcome, "all_vehicle_obj"):
            self.main_parent_welcome.all_vehicle_obj.populate_table()

            # Switch back to ViewALLVehicles
        self.main_parent_welcome.content_area.setCurrentWidget(self.main_parent_welcome.all_vehicle_obj)

        # Delete current widget
        self.main_parent_welcome.content_area.removeWidget(self)
        self.deleteLater()

        # Reset the reference so it does not hold a deleted object
        self.main_parent_welcome.update_vehicle_obj = None