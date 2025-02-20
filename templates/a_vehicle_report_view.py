from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QDate, QTimer, QSize 
from templates.view_all_vehicles import ViewALLVehicles
from controllers.load_assets import *
import sys


class AVehicleReportView(QWidget):

    def __init__(self, user_session=None, parent=None, data = None, db_to_display = None, main_heading = None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        # print("self.user_id:",self.user_id)
        # print("self.username:",self.username)
        self.data = data if data else {}
        print(self.data, len(self.data))
        self.db_to_display = db_to_display
        self.main_header = main_heading if main_heading else {}
        self.main_parent_welcome = parent

        self.initUI()

    def initUI(self):
        self.apply_styles()  # Call it here
        # Main layout is a scroll area so large content can scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # 1) Title / Header
        self.create_title_header()

        # 2) VEH BASIC INFO Section
        self.create_basic_info_section()

        # 3) VEH FITNESS CHECK Section
        self.create_fitness_check_section()

        # 4) FITNESS REPORT Section
        self.create_fitness_report_section()

        # Add a stretch at the end
        self.main_layout.addStretch()

        scroll.setWidget(container)

        # Set main layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #E8EFF9; font-family: Arial; }
            QLabel { font-size: 14px; color: #000; }
            QGroupBox { background-color: white; border: 2px solid #B0C4DE; border-radius: 5px; padding: 10px; font-size: 14px; font-weight: bold; }
            QScrollArea { border: none; background: #E8EFF9;}
            QPushButton { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px; padding: 5px; }
            QPushButton:hover { background-color: #45a049; }
        """)

    def calculate_score(self):
        print("\n\n,self.data", len(self.data))
        keys_to_remove = {'BA NO', 'Make', 'Type', 'CI', 'In Svc', 'Created By', 'Created At', 'id'}
        filtered_data = {key: value for key, value in self.data.items() if key not in keys_to_remove}


        
        print("\n\nfiltered_data,",filtered_data)
        print("\n\nlen(filtered_data)",len(filtered_data))
        print("\n\nlen(keys)",len(filtered_data.keys()))

        total_score = 75
        complete_score = 0
        incomplete_score = 0

        complete_values = {"Svc", "Ok", "Up", "Complete"}
        incomplete_values = {"Unsvc", "Unsatisfactory", "Down", "Incomplete"}

        for value in filtered_data.values():
            if value in complete_values:
                complete_score += 1
            elif value in incomplete_values:
                incomplete_score += 1
        complete_score_percentage = (complete_score / total_score) * 100

        return {
            "complete_score": complete_score,
            "incomplete_score": incomplete_score,
            "complete_score_percentage": round(complete_score_percentage, 2)
        }

    def create_title_header(self):
        title_label = QLabel("A VEH FITNESS CHECK MODULE")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""background-color: #2E86C1; color: white; font-size: 24px; font-weight: bold; padding: 12px; border-radius: 4px;""")
        self.main_layout.addWidget(title_label)

    def create_basic_info_section(self):
        basic_info_group = QGroupBox("VEH BASIC INFO")
        basic_info_group.setStyleSheet("""
            QGroupBox {background-color: #AED6F1; font-weight: bold; border: 2px solid #2E86C1; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #154360;}
        """)
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # For each item in Basic Details, create a mini-box with label + value
        basic_details = self.main_header.get("Basic Details", [])
        for field in basic_details:
            value = self.data.get(field, "")
            field_widget = self.create_field_widget(field, value)
            layout.addWidget(field_widget)

        basic_info_group.setLayout(layout)
        self.main_layout.addWidget(basic_info_group)

    def create_fitness_check_section(self):
        """
        Creates the big "VEH FITNESS CHECK" area with sub-sections
        (Cooling Sys, Hyd Ramp, Lub Sys, etc.)
        """
        fitness_group = QGroupBox("VEH FITNESS CHECK")
        fitness_group.setStyleSheet("""
            QGroupBox { background-color: #FAD7A0; font-weight: bold; border: 2px solid #DC7633; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #6E2C00; }
        """)
        # We can use a grid layout or flow-like layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)

        # We want to skip "Basic Details" and "Creation Details" 
        # because they go in other sections
        exclude_sections = ["Basic Details", "Creation Details"]
        categories = [cat for cat in self.main_header.keys() if cat not in exclude_sections]

        # We'll place them in rows & columns. Adjust to your preference:
        # for example, 3 columns of sub-group boxes
        row = 0
        col = 0
        max_columns = 4

        for cat in categories:
            sub_group = self.create_sub_section(cat, self.main_header[cat])
            grid.addWidget(sub_group, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        fitness_group.setLayout(grid)
        self.main_layout.addWidget(fitness_group)

    def create_sub_section(self, title, fields):
        """
        Creates a sub group box for each category (e.g. "Cooling Sys")
        containing a vertical list or small grid of the items + status
        """
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox { background-color: #FCF3CF; font-weight: normal; border: 1px solid #B7950B; border-radius: 3px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #7D6608; }
        """)

        # Use a simple grid or vertical layout for the fields
        layout = QGridLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 10, 5, 10)

        row = 0
        for field in fields:
            value = self.data.get(field, "")
            # Field label
            lbl_field = QLabel(field)
            lbl_field.setStyleSheet("font-weight: bold;")

            # Value label with color-coded background for Svc/Unsvc
            lbl_value = self.create_status_label(value)

            layout.addWidget(lbl_field, row, 0)
            layout.addWidget(lbl_value, row, 1)
            row += 1

        group_box.setLayout(layout)
        return group_box

    def create_status_label(self, value):
        """
        Returns a QLabel for the item value, color-coded for Svc/Unsvc/None
        """
        lbl = QLabel(str(value))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedWidth(80)

        # Color-code based on value
        if value in ["Svc", "Ok", "Up", "Complete"]:
            lbl.setStyleSheet("background-color: #ABEBC6; color: black; border: 1px solid #58D68D;")
        elif value in ["Unsvc", "Unsatisfactory", "Down", "Incomplete"]:
            lbl.setStyleSheet("background-color: #F5B7B1; color: black; border: 1px solid #EC7063;")
        else:
            # For None or empty, just gray out
            lbl.setStyleSheet("background-color: #D5D8DC; color: black; border: 1px solid #BDC3C7;")

        return lbl

    def create_fitness_report_section(self):
        """
        Creates the "FITNESS REPORT" section at the bottom with dummy values
        (Overall Score, Total Tests, Fitness %, Download, etc.)
        """
        report_group = QGroupBox("FITNESS REPORT")
        report_group.setStyleSheet("""
            QGroupBox { background-color: #D6EAF8; font-weight: bold; border: 2px solid #5DADE2; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #1B4F72; }
        """)
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        score_result = self.calculate_score()

        # Dummy data: "Overall Score: 120 / 166", "Total Tests: 13", etc.
        # You can style these similarly as needed
        dummy_labels = [
            f"Overall Score: {score_result['complete_score']} / 75",
            f"Total Faults: {score_result['incomplete_score']}",
            f"Fitness: {score_result['complete_score_percentage']}%",
            "Download: PDF | Excel",
            "Edit/Update: Veh Summary"
        ]

        for text in dummy_labels:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size: 14px; font-weight: normal;")
            layout.addWidget(lbl)

        report_group.setLayout(layout)
        self.main_layout.addWidget(report_group)

    def create_field_widget(self, label_text, value_text):
        """
        A helper to create a small VBox with label on top and the value below
        to mimic the "BA NO" -> "5465" style from the Basic Info section
        """
        w = QWidget()
        vbox = QVBoxLayout(w)
        vbox.setSpacing(5)
        vbox.setContentsMargins(0, 0, 0, 0)

        lbl_field = QLabel(label_text)
        lbl_field.setAlignment(Qt.AlignCenter)
        lbl_field.setStyleSheet(""" background-color: #F4D03F; color: #1B2631; font-weight: bold; border: 1px solid #B7950B; border-radius: 3px; padding: 5px; """)

        lbl_value = QLabel(str(value_text))
        lbl_value.setAlignment(Qt.AlignCenter)
        lbl_value.setStyleSheet(""" background-color: #FDEBD0; color: #1B2631; font-weight: normal; border: 1px solid #B7950B; border-radius: 3px; padding: 5px; """)

        vbox.addWidget(lbl_field)
        vbox.addWidget(lbl_value)
        return w





