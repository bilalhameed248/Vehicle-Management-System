from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, QVBoxLayout, QHBoxLayout, QSpacerItem,QStackedWidget, QSizePolicy, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QColor, QFont, QIcon

import sqlite3
from database import VMS_DB
from templates.add_vehicle import AddVehicle

class WelcomePage(QWidget):

    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Login - Vehicle Maintenance/Management System")
        self.setStyleSheet("background-color: #1E1E1E;")
        self.initUI()
        self.setWindowState(Qt.WindowMaximized)
        self.show() 
        self.user_session = session
        self.db_obj = VMS_DB()
        # self.add_vObj = AddVehicle()

    def initUI(self):
        # Main Layout with Left Menu and Right Content Area
        main_layout = QHBoxLayout()

        # Left Menu Layout
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignTop)

        # Menu Buttons
        self.home = self.create_menu_button("Home", "assets/icons/home.png")
        self.add_vehicle_button = self.create_menu_button("Add New Vehicle", "assets/icons/vehicle_add.png")
        self.view_all_button = self.create_menu_button("View All Vehicles", "assets/icons/vehicle_view.png")
        self.create_report_button = self.create_menu_button("Create Report", "assets/icons/report_create.png")
        self.logout_button = self.create_menu_button("Logout", "assets/icons/logout.png")
        self.profile_button = self.create_menu_button("Profile", "assets/icons/profile.png")

        # Add buttons to menu layout
        menu_layout.addWidget(self.home)
        menu_layout.addWidget(self.add_vehicle_button)
        menu_layout.addWidget(self.view_all_button)
        menu_layout.addWidget(self.create_report_button)
        menu_layout.addWidget(self.logout_button)
        menu_layout.addWidget(self.profile_button)

        # Set up the left menu as a vertical panel
        menu_frame = QFrame(self)
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet("background-color: #2C3E50; color: white; padding: 10px;")
        menu_frame.setFixedWidth(300)  # Fixed width for the left menu
        main_layout.addWidget(menu_frame)

        # Right Content Area
        self.content_area = QStackedWidget()
        self.content_area.addWidget(self.create_welcome_message())  # Initial page: Welcome message
        main_layout.addWidget(self.content_area)

        self.add_vehicle_button.clicked.connect(self.add_new_vehicle)


        self.setLayout(main_layout)

    def add_new_vehicle(self):
        """Create the add new vehicle form."""
        # Create a QWidget to hold the form inside a scroll area
        form_container = QWidget()

        # Layout for the form
        form_layout = QFormLayout()

        # Vehicle Information Inputs
        self.vehicle_name_input = QLineEdit(self)
        self.vehicle_name_input.setPlaceholderText("Enter Vehicle Name")
        form_layout.addRow("Vehicle Name:", self.vehicle_name_input)

        self.vehicle_model_input = QLineEdit(self)
        self.vehicle_model_input.setPlaceholderText("Enter Vehicle Model")
        form_layout.addRow("Vehicle Model:", self.vehicle_model_input)

        self.registration_number_input = QLineEdit(self)
        self.registration_number_input.setPlaceholderText("Enter Registration Number")
        form_layout.addRow("Registration Number:", self.registration_number_input)

        self.manufacture_year_input = QLineEdit(self)
        self.manufacture_year_input.setPlaceholderText("Enter Manufacture Year")
        form_layout.addRow("Manufacture Year:", self.manufacture_year_input)

        self.vehicle_type_input = QLineEdit(self)
        self.vehicle_type_input.setPlaceholderText("Enter Vehicle Type")
        form_layout.addRow("Vehicle Type:", self.vehicle_type_input)

        # Add Save Record Button
        self.save_record_button = QPushButton("Save Record")
        # self.save_record_button.clicked.connect(self.save_vehicle_record)
        form_layout.addRow(self.save_record_button)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Set the form container as the widget inside the scroll area
        form_container.setLayout(form_layout)
        scroll_area.setWidget(form_container)

        self.content_area.addWidget(scroll_area)  # Add scroll area to content area
        self.content_area.setCurrentWidget(scroll_area)  # Show the form (instead of the welcome message)

    def create_menu_button(self, text, icon_path):
        """Create a styled menu button with an icon and text."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))  # Set the button icon
        button.setIconSize(QSize(30, 30))  # Adjust icon size
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setStyleSheet(""" 
            QPushButton {
                background-color: #34495E;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                border: none;
                font-size: 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        return button

    def create_welcome_message(self):
        """Create the welcome message page."""
        welcome_message = QLabel(f"Welcome to the Vehicle Maintenance Record Portal", self)
        welcome_message.setAlignment(Qt.AlignCenter)
        welcome_message.setWordWrap(True)
        welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_message.setStyleSheet("color: #2C3E50; padding: 20px;")

        # Additional message (below the welcome message)
        additional_message = QLabel(
            "This portal is designed to streamline and enhance the management of vehicle "
            "maintenance records of 44 AK Pak ARMY", self)
        additional_message.setAlignment(Qt.AlignCenter)
        additional_message.setWordWrap(True)
        additional_message.setFont(QFont("Arial", 14))  # Smaller font size
        additional_message.setStyleSheet("color: #7F8C8D; padding: 10px;")
        
        # A simple placeholder page (empty space)
        empty_page = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(welcome_message)
        layout.addWidget(additional_message)  # Add the new message below
        empty_page.setLayout(layout)
        return empty_page

    # def add_new_vehicle(self):
    #     # Placeholder for adding new vehicle logic
    #     print("Add New Vehicle clicked")
    #     # Logic here, for example: self.show_add_vehicle_page()
    
    def view_all_vehicles(self):
        # Placeholder for viewing all vehicles logic
        print("View All Vehicles clicked")
        # Logic here, for example: self.show_view_all_vehicles()

    def create_report(self):
        # Placeholder for creating a report logic
        print("Create Report clicked")
        # Logic here, for example: self.show_create_report()

    def logout(self):
        # Placeholder for logout logic
        print("Logout clicked")
        # Logic here, for example: self.logout_user()

    def profile(self):
        # Placeholder for profile logic
        print("Profile clicked")
        # Logic here, for example: self.show_user_profile()