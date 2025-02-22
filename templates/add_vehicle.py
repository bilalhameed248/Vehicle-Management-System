from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from database import VMS_DB  
from templates.view_all_vehicles import ViewALLVehicles
from controllers.load_assets import *

class AddVehicle(QWidget):

    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        # print("self.user_id:",self.user_id)
        # print("self.username:",self.username)
        self.main_parent_welcome = parent
        self.initUI()
        self.db_obj = VMS_DB() 


    def initUI(self):
        self.setWindowTitle("Vehicle Maintenance Form")
        calendar_icon_path = get_asset_path("assets/icons/calendar.png").replace("\\", "/")
        combo_dd_icon_path = get_asset_path("assets/icons/combo_dd.png").replace("\\", "/")

        self.setStyleSheet(f"""QWidget {{ background-color: #f4f4f4; font-size: 18px; }}
            QLabel {{ font-weight: bold; }}
            QLineEdit, QTextEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px;}}
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
            
            QDateEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px; }}
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path}); }}
            QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
            QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
            QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
            QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
            QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white; }}

            QComboBox {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px; }}
            QComboBox::down-arrow {{ width: 20px; border: none; background: transparent; image: url({combo_dd_icon_path}); }}
            QComboBox QAbstractItemView {{ background-color: white; border: 1px solid #4a90e2; selection-background-color: #4a90e2; selection-color: white;}}
            QComboBox::item {{ padding: 8px; }}
            QComboBox::item:selected {{ background-color: #4a90e2; color: white; }}
        """)

        self.basic_details = {}
        self.maintenance_fields = {}
        self.battery_fields = {}
        self.flusing_fields = {}
        self.greasing_fields = {}
        self.gen_maint_fields = {}
        self.overhaul_fields = {}
        self.status_fields = {}

        layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.setSpacing(6)

        def combo_input(title, items):
            combo_layout = QVBoxLayout()
            combo_layout.addWidget(QLabel(title))
            self.blocked_combo = QComboBox()
            self.blocked_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.blocked_combo.addItem("--Select--")
            self.blocked_combo.setItemData(0, 0, Qt.UserRole - 1)  # Disable the first item
            self.blocked_combo.addItems(items)
            self.blocked_combo.setCurrentIndex(0)
            combo_layout.addWidget(self.blocked_combo)
            return combo_layout, self.blocked_combo
        
        def text_input_fun(title):
            text_input_layout = QVBoxLayout()
            text_input_layout.addWidget(QLabel(title))
            self.text_input = QLineEdit()
            text_input_layout.addWidget(self.text_input)
            return text_input_layout, self.text_input
        
        def date_input(title):
            date_input_layout = QVBoxLayout()
            date_input_layout.addWidget(QLabel(title))
            self.date_input = QDateEdit()
            self.date_input.setCalendarPopup(True)
            self.date_input.setDate(QDate.currentDate())
            self.date_input.setDisplayFormat("dd-MM-yyyy")
            date_input_layout.addWidget(self.date_input)
            return date_input_layout, self.date_input

        def add_basic_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["A", "B"]
            self.category_layout, self.category_input = combo_input("Status:", combo_items)
            self.ba_no_input_layout, self.ba_no_input = text_input_fun("BA No:")
            self.make_type_layout, self.make_type_input = text_input_fun("Make & Type:")
            self.engine_no_layout, self.engine_no_input = text_input_fun("Engine No:")

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.category_layout)
            row1_layout.addLayout(self.ba_no_input_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.make_type_layout)
            row2_layout.addLayout(self.engine_no_layout)

            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.basic_details[title] = {
                f"category": self.category_input,
                f"ba_no_input": self.ba_no_input,
                f"make_type_input": self.make_type_input,
                f"engine_no_input": self.engine_no_input
            }


        def add_maintenance_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            issue_date_layout, issue_date = date_input("Issue Date:")
            due_date_layout, due_date = date_input("Due Date:")
            current_mileage_layout, current_mileage = text_input_fun("Current Mileage:")
            due_mileage_layout, due_mileage = text_input_fun("Due Mileage:")

            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(issue_date_layout)
            row1_layout.addLayout(due_date_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()
            row2_layout.addLayout(current_mileage_layout)
            row2_layout.addLayout(due_mileage_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # form_layout.addWidget(group_box, row, col)

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
            
            self.issue_date_layout, self.battery_issue_date = date_input("Issue Date:")
            self.due_date_layout, self.battery_due_date = date_input("Due Date:")

            row_layout = QHBoxLayout()
            row_layout.addLayout(self.issue_date_layout)
            row_layout.addLayout(self.due_date_layout)

            # Add the row to the group layout
            group_layout.addLayout(row_layout)
            group_box.setLayout(group_layout)
            # Add the group box to the form
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.battery_fields[title] = {
                "battery_issue_date": self.battery_issue_date,
                "battery_due_date": self.battery_due_date
            }

        
        def add_greasing_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            self.issue_date_layout, self.greasing_issue_date = date_input("Issue Date:")
            self.due_date_layout, self.greasing_due_date = date_input("Due Date:")
            self.trs_and_suspension_layout, self.trs_and_suspension = text_input_fun("Trs and suspension:")
            self.engine_part_layout, self.engine_part = text_input_fun("Engine parts:")
            self.steering_lever_Pts_layout, self.steering_lever_Pts = text_input_fun("Steering lever Pts:")

            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.issue_date_layout)
            row1_layout.addLayout(self.due_date_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.trs_and_suspension_layout)
            row2_layout.addLayout(self.engine_part_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.steering_lever_Pts_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.greasing_fields[title] = {
                "greasing_issue_date": self.greasing_issue_date,
                "greasing_due_date": self.greasing_due_date,
                "trs_and_suspension": self.trs_and_suspension,
                "engine_part": self.engine_part,
                "steering_lever_Pts": self.steering_lever_Pts
            }


        def add_flusing_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            self.issue_date_layout, self.flushing_issue_date = date_input("Issue Date:")
            self.due_date_layout, self.flushing_due_date = date_input("Due Date:")
            self.fuel_tank_flush_layout, self.fuel_tank_flush = text_input_fun("Fuel Tank Flush:")
            self.radiator_flush_layout, self.radiator_flush = text_input_fun("Radiator Flush:")

            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.issue_date_layout)
            row1_layout.addLayout(self.due_date_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.fuel_tank_flush_layout)
            row2_layout.addLayout(self.radiator_flush_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.flusing_fields[title] = {
                "flusing_issue_date": self.flushing_issue_date,
                "flusing_due_date": self.flushing_due_date,
                "fuel_tank_flush": self.fuel_tank_flush,
                "radiator_flush": self.radiator_flush
            }


        def add_gen_maint_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            self.wash_layout, self.wash = text_input_fun("Wash:")
            self.oil_level_check_layout, self.oil_level_check = text_input_fun("Oil Level Check:")
            self.lubrication_of_parts_layout, self.lubrication_of_parts = text_input_fun("Lubrication of parts:")
            self.air_cleaner_layout, self.air_cleaner = text_input_fun("Air Cleaner Maint:")
            self.fuel_filter_layout, self.fuel_filter = text_input_fun("Fuel Filter Maint:")
            self.french_chalk_layout, self.french_chalk = text_input_fun("French chalk:")
            self.tr_adjustment_layout, self.tr_adjustment = text_input_fun("Tr Adjustment:")

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.wash_layout)
            row1_layout.addLayout(self.oil_level_check_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.lubrication_of_parts_layout)
            row2_layout.addLayout(self.air_cleaner_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.fuel_filter_layout)
            row3_layout.addLayout(self.french_chalk_layout)

            row4_layout = QHBoxLayout()
            row4_layout.addLayout(self.tr_adjustment_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            self.gen_maint_fields[title] = {
                "wash": self.wash,
                "oil_level_check": self.oil_level_check,
                "lubrication_of_parts": self.lubrication_of_parts,
                "air_cleaner": self.air_cleaner,
                "fuel_filter": self.fuel_filter,
                "french_chalk": self.french_chalk,
                "tr_adjustment": self.tr_adjustment
            }


        def add_overhaul_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            self.current_mileage_layout, self.overhaul_current_milage = text_input_fun("Current Mileage:")
            self.due_mileage_layout, self.overhaul_due_milage = text_input_fun("Due Mileage:")
        
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.current_mileage_layout)
            row1_layout.addLayout(self.due_mileage_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.overhaul_fields[title] = {
                "overhaul_current_milage": self.overhaul_current_milage,
                "overhaul_due_milage": self.overhaul_due_milage
            }


        def add_status_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    
    
            combo_items = ["Fit", "Unfit"]
            self.status_layout, self.status_input = combo_input("Status:", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.status_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.status_fields[title] = {
                "overhaul_remarks_input": self.status_input
            }


        # Maintenance Sections
        add_basic_section("Basic Details", 0, 0)
        add_maintenance_section("Oil Filter", 0, 1)
        add_maintenance_section("Fuel Filter", 0, 2)
        add_maintenance_section("Air Filter", 2, 0)
        add_maintenance_section("Transmission Filter", 2, 1)
        add_maintenance_section("Differential Oil", 2, 2)
        add_greasing_section("Greasing", 4, 0)
        add_flusing_section("Flushing", 4, 1)
        add_gen_maint_section("Gen Maint (Monthly)", 4, 2)
        add_battery_section("Battery", 6, 0)
        add_overhaul_section("Overhaul", 6, 1)
        add_status_section("Remarks/Status", 6, 2)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(" Save")
        save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        save_button.setIconSize(QSize(20, 20))
        save_button.clicked.connect(self.save_vehicle)

        clear_button = QPushButton(" Clear/Reset")
        clear_button.setIcon(QIcon(get_asset_path("assets/icons/clear.png")))
        clear_button.setIconSize(QSize(20, 20))
        clear_button.clicked.connect(self.clear_fields)

        cancel_button = QPushButton(" Cancel")
        cancel_button.setIcon(QIcon(get_asset_path("assets/icons/cancel.png")))
        cancel_button.setIconSize(QSize(20, 20))
        # cancel_button.clicked.connect(self.cancel_add_vehicle)

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
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


    def save_vehicle(self):
        """ Inserts user into the database """
        add_vehicle_data = {}

        required_fields = ['ba_no_input', 'make_type_input', 'engine_no_input']
        if not all(self.basic_details['Basic Details'][field].text().strip() for field in required_fields):
            QMessageBox.warning(self, "Error", "BA NO, Make Type & Engine Number are required!")
            return
        
        field_categories = [
            self.basic_details, self.maintenance_fields, self.battery_fields, self.flusing_fields, self.greasing_fields, 
            self.gen_maint_fields, self.overhaul_fields, self.status_fields
        ]

        for category in field_categories:
            for fields in category.values():
                for key, widget in fields.items():
                    if isinstance(widget, QComboBox):
                        add_vehicle_data[key] = None if widget.currentText().strip() == "--Select--" else  widget.currentText().strip()
                    elif isinstance(widget, QLineEdit):
                        add_vehicle_data[key] = widget.text().strip()
                    elif isinstance(widget, QDateEdit):
                        add_vehicle_data[key] = widget.date().toString("yyyy-MM-dd")
        add_vehicle_data['created_by'] = self.user_id

        is_data_inserted = self.db_obj.insert_vehicle(add_vehicle_data)
        if not is_data_inserted:
            QMessageBox.warning(self, "Failed", "Error while saving the data..! Please Try Again")
            return
        else:
            QMessageBox.information(self, "Success", "Vehicle added successfully!")
            return
    

    def clear_fields(self):
        self.blocked_combo.setCurrentIndex(0)
        self.ba_no_input.setText("")
        self.make_type_input.setText("")
        self.engine_no_input.setText("")

        self.battery_issue_date.setDate(QDate.currentDate())
        self.battery_due_date.setDate(QDate.currentDate())

        self.greasing_issue_date.setDate(QDate.currentDate())
        self.greasing_due_date.setDate(QDate.currentDate())
        self.trs_and_suspension.setText("")
        self.engine_part.setText("")
        self.steering_lever_Pts.setText("")

        self.flushing_issue_date.setDate(QDate.currentDate())
        self.flushing_due_date.setDate(QDate.currentDate())
        self.fuel_tank_flush.setText("")
        self.radiator_flush.setText("")

        self.wash.setText("")
        self.oil_level_check.setText("")
        self.lubrication_of_parts.setText("")
        self.air_cleaner.setText("")
        self.fuel_filter.setText("")
        self.french_chalk.setText("")
        self.tr_adjustment.setText("")

        self.overhaul_current_milage.setText("")
        self.overhaul_due_milage.setText("")

    # def cancel_add_vehicle(self):
    #     self.main_parent_welcome.welcome_summary_obj.load_data()  # Reload fresh data
    #     self.main_parent_welcome.content_area.setCurrentWidget(self.welcome_summary_obj)  # Switch view