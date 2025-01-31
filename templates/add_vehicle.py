from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QGridLayout, QVBoxLayout,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QDate

class AddVehicle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Vehicle Maintenance Form")
        self.setStyleSheet("""
            QWidget { background-color: #f4f4f4; font-size: 18px; }
            QLabel { font-weight: bold; }
            QLineEdit, QDateEdit { padding: 5px; border: 1px solid #ccc; border-radius: 4px;}
            QPushButton { background-color: #007BFF; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
            QGroupBox {font-weight: bold; border: 2px solid #007BFF; padding: 10px; margin-top: 20px;margin-bottom: 20px; border-radius: 8px; }
            QGroupBox title { color: #007BFF; font-size: 16px; }
            QScrollBar:vertical {border: none; background: #f0f0f0; width: 10px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: blue; min-height: 20px; border-radius: 5px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none;}
            QScrollBar:horizontal {border: none; background: #f0f0f0; height: 10px; margin: 0px 0px 0px 0px; }
            QScrollBar::handle:horizontal { background: blue; min-width: 20px; border-radius: 5px; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {background: none;}
        """)

        layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.setSpacing(12)

        # Create input fields
        self.id_input = QLineEdit()
        self.ba_no_input = QLineEdit()
        self.make_type_input = QLineEdit()
        self.engine_no_input = QLineEdit()
        
        form_layout.addWidget(QLabel("ID:"), 0, 0)
        form_layout.addWidget(self.id_input, 0, 1)
        form_layout.addWidget(QLabel("BA No:"), 0, 2)
        form_layout.addWidget(self.ba_no_input, 0, 3)
        form_layout.addWidget(QLabel("Make & Type:"), 1, 0)
        form_layout.addWidget(self.make_type_input, 1, 1)
        form_layout.addWidget(QLabel("Engine No:"), 1, 2)
        form_layout.addWidget(self.engine_no_input, 1, 3)
        
        # Function to create maintenance rows
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
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.currentDate())
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            current_mileage_layout = QVBoxLayout()
            current_mileage_layout.addWidget(QLabel("Current Mileage:"))
            current_mileage = QLineEdit()
            current_mileage.setValidator(QIntValidator())
            current_mileage_layout.addWidget(current_mileage)

            due_mileage_layout = QVBoxLayout()
            due_mileage_layout.addWidget(QLabel("Due Mileage:"))
            due_mileage = QLineEdit()
            due_mileage.setValidator(QIntValidator())
            due_mileage_layout.addWidget(due_mileage)

            row2_layout.addLayout(current_mileage_layout)
            row2_layout.addLayout(due_mileage_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

        def add_battery_section(title, row):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            
            # Create a horizontal layout for the row
            row_layout = QHBoxLayout()

            # Issue Date
            issue_layout = QVBoxLayout()
            issue_layout.addWidget(QLabel("Issue Date:"))
            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDate(QDate.currentDate())
            issue_layout.addWidget(issue_date)

            # Due Date
            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.currentDate())
            due_layout.addWidget(due_date)

            # Add both to the horizontal layout
            row_layout.addLayout(issue_layout)
            row_layout.addLayout(due_layout)

            # Add the row to the group layout
            group_layout.addLayout(row_layout)
            group_box.setLayout(group_layout)

            # Add the group box to the form
            form_layout.addWidget(group_box, row, 0, 1, 4)

        # Function to create maintenance rows
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
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.currentDate())
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            fuel_tank_flush_layout = QVBoxLayout()
            fuel_tank_flush_layout.addWidget(QLabel("Fuel Tank Flush:"))
            fuel_tank_flush = QLineEdit()
            fuel_tank_flush.setValidator(QIntValidator())
            fuel_tank_flush_layout.addWidget(fuel_tank_flush)

            radiator_flush_layout = QVBoxLayout()
            radiator_flush_layout.addWidget(QLabel("Radiator Flush:"))
            radiator_flush = QLineEdit()
            radiator_flush.setValidator(QIntValidator())
            radiator_flush_layout.addWidget(radiator_flush)

            row2_layout.addLayout(fuel_tank_flush_layout)
            row2_layout.addLayout(radiator_flush_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)
        
        # Function to create maintenance rows
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
            issue_layout.addWidget(issue_date)

            due_layout = QVBoxLayout()
            due_layout.addWidget(QLabel("Due Date:"))
            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.currentDate())
            due_layout.addWidget(due_date)

            row1_layout.addLayout(issue_layout)
            row1_layout.addLayout(due_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            trs_and_suspension_layout = QVBoxLayout()
            trs_and_suspension_layout.addWidget(QLabel("Trs and suspension:"))
            trs_and_suspension = QLineEdit()
            trs_and_suspension.setValidator(QIntValidator())
            trs_and_suspension_layout.addWidget(trs_and_suspension)

            engine_part_layout = QVBoxLayout()
            engine_part_layout.addWidget(QLabel("Engine parts:"))
            engine_part = QLineEdit()
            engine_part.setValidator(QIntValidator())
            engine_part_layout.addWidget(engine_part)

            row2_layout.addLayout(trs_and_suspension_layout)
            row2_layout.addLayout(engine_part_layout)

            steering_lever_Pts_layout = QVBoxLayout()
            steering_lever_Pts_layout.addWidget(QLabel("Steering lever Pts:"))
            steering_lever_Pts = QLineEdit()
            steering_lever_Pts.setValidator(QIntValidator())
            steering_lever_Pts_layout.addWidget(steering_lever_Pts)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(steering_lever_Pts_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

        # Function to create maintenance rows
        def add_gen_maint_section(title, row):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            # Row 1: Issue Date & Due Date
            row1_layout = QHBoxLayout()

            wash_layout = QVBoxLayout()
            wash_layout.addWidget(QLabel("Wash:"))
            wash = QLineEdit()
            wash.setValidator(QIntValidator())
            wash_layout.addWidget(wash)

            oil_level_check_layout = QVBoxLayout()
            oil_level_check_layout.addWidget(QLabel("Oil Level Check:"))
            engine_part = QLineEdit()
            engine_part.setValidator(QIntValidator())
            oil_level_check_layout.addWidget(engine_part)

            row1_layout.addLayout(wash_layout)
            row1_layout.addLayout(oil_level_check_layout)

            # Row 2: Current Mileage & Due Mileage
            row2_layout = QHBoxLayout()

            lubrication_of_parts_layout = QVBoxLayout()
            lubrication_of_parts_layout.addWidget(QLabel("Lubrication of parts:"))
            lubrication_of_parts = QLineEdit()
            lubrication_of_parts.setValidator(QIntValidator())
            lubrication_of_parts_layout.addWidget(lubrication_of_parts)

            air_cleaner_layout = QVBoxLayout()
            air_cleaner_layout.addWidget(QLabel("Air Cleaner Maint:"))
            air_cleaner = QLineEdit()
            air_cleaner.setValidator(QIntValidator())
            air_cleaner_layout.addWidget(air_cleaner)

            row2_layout.addLayout(lubrication_of_parts_layout)
            row2_layout.addLayout(air_cleaner_layout)

            row3_layout = QHBoxLayout()

            fuel_filter_layout = QVBoxLayout()
            fuel_filter_layout.addWidget(QLabel("Fuel Filter Maint:"))
            fuel_filter = QLineEdit()
            fuel_filter.setValidator(QIntValidator())
            fuel_filter_layout.addWidget(fuel_filter)

            french_chalk_layout = QVBoxLayout()
            french_chalk_layout.addWidget(QLabel("French chalk:"))
            french_chalk = QLineEdit()
            french_chalk.setValidator(QIntValidator())
            french_chalk_layout.addWidget(french_chalk)

            row3_layout.addLayout(fuel_filter_layout)
            row3_layout.addLayout(french_chalk_layout)

            row4_layout = QHBoxLayout()
            
            tr_adjustment_layout = QVBoxLayout()
            tr_adjustment_layout.addWidget(QLabel("Tr Adjustment:"))
            tr_adjustment = QLineEdit()
            tr_adjustment.setValidator(QIntValidator())
            tr_adjustment_layout.addWidget(tr_adjustment)

            row4_layout.addLayout(tr_adjustment_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, 0, 1, 4)

        # Maintenance Sections
        add_maintenance_section("Oil Filter", 2)
        add_maintenance_section("Fuel Filter", 4)
        add_maintenance_section("Air Filter", 6)
        add_maintenance_section("Transmission Filter", 8)
        add_maintenance_section("Differential Oil", 10)
        
        # Battery
        add_battery_section("Battery", 12)
        # Greasing
        add_greasing_section("Greasing", 14)
        # Flushing
        add_flusing_section("Flushing", 16)

        add_gen_maint_section("Gen Maint (Monthly)", 18)
        
        # Overhaul Section
        form_layout.addWidget(QLabel("Overhaul - Current Mileage:"), 20, 0)
        overhaul_current = QLineEdit()
        overhaul_current.setValidator(QIntValidator())
        form_layout.addWidget(overhaul_current, 20, 1)
        
        form_layout.addWidget(QLabel("Due Mileage:"), 20, 2)
        overhaul_due = QLineEdit()
        overhaul_due.setValidator(QIntValidator())
        form_layout.addWidget(overhaul_due, 20, 3)

        # Remarks Section
        form_layout.addWidget(QLabel("Remarks:"), 21, 0)
        self.remarks_input = QLineEdit()
        form_layout.addWidget(self.remarks_input, 21, 1, 1, 3)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")
        cancel_button = QPushButton("Cancel")
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