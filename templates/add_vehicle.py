from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from database import VMS_DB  
from templates.view_all_vehicles import ViewALLVehicles

class AddVehicle(QWidget):
    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        print("self.user_id:",self.user_id)
        print("self.username:",self.username)
        self.initUI()
        self.db_obj = VMS_DB() 

    def initUI(self):
        self.setWindowTitle("Vehicle Maintenance Form")
        self.setStyleSheet("""
            QWidget { background-color: #f4f4f4; font-size: 18px; }
            QLabel { font-weight: bold; }
            QLineEdit, QDateEdit, QTextEdit { padding: 5px; border: 1px solid #ccc; border-radius: 4px;}
            QPushButton { background-color: #007BFF; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
            QGroupBox {font-weight: bold; border: 2px solid #007BFF; padding: 10px; margin-top: 20px;margin-bottom: 20px; border-radius: 8px; }
            QGroupBox title { color: #007BFF; font-size: 16px; }
            QScrollBar:vertical {border: none; background: #f0f0f0; width: 20px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: blue; min-height: 20px; border-radius: 5px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none;}
            QScrollBar:horizontal {border: none; background: #f0f0f0; height: 10px; margin: 0px 0px 0px 0px; }
            QScrollBar::handle:horizontal { background: blue; min-width: 20px; border-radius: 5px; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {background: none;}
        """)

        self.maintenance_fields = {}
        self.battery_fields = {}
        self.flusing_fields = {}
        self.greasing_fields = {}
        self.gen_maint_fields = {}
        self.overhaul_fields = {}

        layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.setSpacing(12)

        # Create input fields
        self.blocked_combo = QComboBox()
        self.blocked_combo.addItem("A")
        self.blocked_combo.addItem("B")
        self.blocked_combo.setStyleSheet("""
            QComboBox {background-color: #f0f0f0;border: 2px solid #4a90e2; border-radius: 5px; padding: 5px; font-size: 14px; color: #333;}
            QComboBox::drop-down {border-left: 2px solid #4a90e2; background-color: #e6e6e6;}
            QComboBox::down-arrow {image: url('path_to_your_arrow_icon.png');  /* Optional: custom arrow icon */}
            QComboBox QAbstractItemView {background-color: white;border: 1px solid #4a90e2;selection-background-color: #4a90e2; selection-color: white;}
            QComboBox::item {padding: 8px;}
            QComboBox::item:selected {background-color: #4a90e2;color: white;}""")
        self.ba_no_input = QLineEdit()
        self.make_type_input = QLineEdit()
        self.engine_no_input = QLineEdit()
        
        form_layout.addWidget(QLabel("Category:"), 0, 0)
        form_layout.addWidget(self.blocked_combo, 0, 1)
        form_layout.addWidget(QLabel("BA No:"), 0, 2)
        form_layout.addWidget(self.ba_no_input, 0, 3)
        form_layout.addWidget(QLabel("Make & Type:"), 1, 0)
        form_layout.addWidget(self.make_type_input, 1, 1)
        form_layout.addWidget(QLabel("Engine No:"), 1, 2)
        form_layout.addWidget(self.engine_no_input, 1, 3)
        

        def add_maintenance_section(title, row):
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

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

            # Store references to input fields
            self.maintenance_fields[title] = {
                f"issue_date_{title.lower().replace(' ', '_')}": issue_date,
                f"due_date_{title.lower().replace(' ', '_')}": due_date,
                f"current_mileage_{title.lower().replace(' ', '_')}": current_mileage,
                f"due_mileage_{title.lower().replace(' ', '_')}": due_mileage
            }

    
        def add_battery_section(title, row):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            
            # Create a horizontal layout for the row
            row_layout = QHBoxLayout()

            # Issue Date
            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            battery_issue_date = QDateEdit()
            battery_issue_date.setCalendarPopup(True)
            battery_issue_date.setDate(QDate.currentDate())
            battery_issue_date.setDisplayFormat("dd-MM-yyyy")
            issue_layout.addWidget(battery_issue_date)

            # Due Date
            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            battery_due_date = QDateEdit()
            battery_due_date.setCalendarPopup(True)
            battery_due_date.setDate(QDate.currentDate())
            battery_due_date.setDisplayFormat("dd-MM-yyyy")
            due_layout.addWidget(battery_due_date)

            # Add both to the horizontal layout
            row_layout.addLayout(issue_layout)
            row_layout.addLayout(due_layout)

            # Add the row to the group layout
            group_layout.addLayout(row_layout)
            group_box.setLayout(group_layout)
            # Add the group box to the form
            form_layout.addWidget(group_box, row, 0, 1, 4)

            self.battery_fields[title] = {
                "battery_issue_date": battery_issue_date,
                "battery_due_date": battery_due_date
            }


        def add_flusing_section(title, row):
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

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

            self.flusing_fields[title] = {
                "flusing_issue_date": issue_date,
                "flusing_due_date": due_date,
                "fuel_tank_flush": fuel_tank_flush,
                "radiator_flush": radiator_flush
            }
        

        def add_greasing_section(title, row):
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
            issue_date.setDisplayFormat("dd-MM-yyyy")
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

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

            self.greasing_fields[title] = {
                "greasing_issue_date": issue_date,
                "greasing_due_date": due_date,
                "trs_and_suspension": trs_and_suspension,
                "engine_part": engine_part,
                "steering_lever_Pts": steering_lever_Pts
            }


        def add_gen_maint_section(title, row):
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

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

            self.gen_maint_fields[title] = {
                "wash": wash,
                "oil_level_check": oil_level_check,
                "lubrication_of_parts": lubrication_of_parts,
                "air_cleaner": air_cleaner,
                "fuel_filter": fuel_filter,
                "french_chalk": french_chalk,
                "tr_adjustment": tr_adjustment
            }

        # Maintenance Sections
        add_maintenance_section("Oil Filter", 2)
        add_maintenance_section("Fuel Filter", 4)
        add_maintenance_section("Air Filter", 6)
        add_maintenance_section("Transmission Filter", 8)
        add_maintenance_section("Differential Oil", 10)
        add_battery_section("Battery", 12)
        add_greasing_section("Greasing", 14)
        add_flusing_section("Flushing", 16)
        add_gen_maint_section("Gen Maint (Monthly)", 18)
        
        # Overhaul Section
        form_layout.addWidget(QLabel("Overhaul - Current Mileage:"), 20, 0)
        overhaul_current_milage = QLineEdit()
        form_layout.addWidget(overhaul_current_milage, 20, 1)
        
        form_layout.addWidget(QLabel("Due Mileage:"), 20, 2)
        overhaul_due_milage = QLineEdit()
        form_layout.addWidget(overhaul_due_milage, 20, 3)

        # Remarks Section
        form_layout.addWidget(QLabel("Remarks:"), 21, 0)
        overhaul_remarks_input = QTextEdit()
        form_layout.addWidget(overhaul_remarks_input, 21, 1, 1, 3)

        self.overhaul_fields['Overhaul'] = {
            "overhaul_current_milage": overhaul_current_milage,
            "overhaul_due_milage": overhaul_due_milage,
            "overhaul_remarks_input": overhaul_remarks_input if overhaul_remarks_input else "Nothing Mentioned"
        }

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(" Save")
        save_button.setIcon(QIcon("assets/icons/save.png"))
        save_button.setIconSize(QSize(20, 20))
        save_button.clicked.connect(self.save_vehicle)

        clear_button = QPushButton("Clear")
        clear_button.setIcon(QIcon("assets/icons/clear.png"))
        clear_button.setIconSize(QSize(20, 20))

        cancel_button = QPushButton(" Cancel")
        cancel_button.setIcon(QIcon("assets/icons/cancel.png"))
        cancel_button.setIconSize(QSize(20, 20))

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
        add_Vehicle_data = {}

        category = "A" if self.blocked_combo.currentIndex() == 1 else "B"
        ba_no_input = self.ba_no_input.text().strip()
        make_type_input = self.make_type_input.text().strip()
        engine_no_input = self.engine_no_input.text().strip()

        if not (ba_no_input or make_type_input or engine_no_input):
            QMessageBox.warning(self, "Error", "BA NO, Make Type & Engine Number are required!")
            return

        add_Vehicle_data['category'] = category
        add_Vehicle_data['ba_no_input'] = ba_no_input
        add_Vehicle_data['make_type_input'] = make_type_input
        add_Vehicle_data['engine_no_input'] = engine_no_input

        for fields in self.maintenance_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()
        
        for fields in self.battery_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.flusing_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.greasing_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.gen_maint_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()

        for fields in self.overhaul_fields.values():
            for key, widget in fields.items():
                if isinstance(widget, QDateEdit):
                    add_Vehicle_data[key] = widget.date().toString("dd-MM-yyyy")
                elif isinstance(widget, QLineEdit):
                    add_Vehicle_data[key] = widget.text().strip()
                elif isinstance(widget, QTextEdit):
                    add_Vehicle_data[key] = widget.toPlainText().strip()

        add_Vehicle_data['created_by'] = self.user_id
        add_Vehicle_data['updated_by'] = ''
        add_Vehicle_data['updated_at'] = ''
        add_Vehicle_data['deleted_at'] = ''
        add_Vehicle_data['is_deleted'] = 0

        # Now you can use maintenance_data to save to the database
        # print("add_Vehicle_data:",add_Vehicle_data)
        # print("\n\n",add_Vehicle_data.keys()) 
        is_data_inserted = self.db_obj.insert_vehicle(add_Vehicle_data)
        if not is_data_inserted:
            QMessageBox.warning(self, "Failed", "Error while saving the data..! Please Try Again")
            return
        else:
            QMessageBox.information(self, "Success", "User added successfully!")
            self.accept()

    # def open_view_all_vehicles_page(self):
    #     """Close login page and show welcome page"""
    #     self.welcome_window = ViewALLVehicles(user_session=self.user_session, parent=self)
    