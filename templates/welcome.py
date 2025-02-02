from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon

import sqlite3
from database import VMS_DB
from templates.add_vehicle import AddVehicle
from templates.users import Users
# from templates.login import LoginPage 

class WelcomePage(QWidget):

    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Home - Vehicle Maintenance Module")
        self.setStyleSheet("background-color: #1E1E1E;")
        self.setWindowIcon(QIcon("assets/images/tank.png"))
        self.initUI()
        self.setWindowState(Qt.WindowMaximized)
        self.show()
        self.user_session = session
        self.db_obj = VMS_DB()
        self.add_vehicle_obj = AddVehicle()

    def update_menu_button_style(self, clicked_button):
        # Reset the style of all buttons
        buttons = [self.home, self.add_vehicle_button, self.view_all_button, self.create_report_button, self.users_management_button]
        for button in buttons:
            button.setStyleSheet("""
                QPushButton {background-color: #34495E; color: white; border-radius: 5px; padding: 10px 20px; text-align: left; }
                QPushButton:hover { background-color: #2980B9; }
            """)
        clicked_button.setStyleSheet("""
            QPushButton { background-color: #2980B9; color: white; border-radius: 5px; padding: 10px 20px; text-align: left;}
        """)

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Top Navigation Bar
        navbar = self.create_navbar()
        main_layout.addWidget(navbar)
        
        # Main Content Area (Horizontal Split: Left Menu & Right Content)
        content_layout = QHBoxLayout()
        
        # Left Menu
        menu_frame = self.create_menu()
        content_layout.addWidget(menu_frame)
        
        # Right Content Area
        self.content_area = QStackedWidget()
        self.content_area.addWidget(self.create_welcome_message())  # Initial Page
        content_layout.addWidget(self.content_area)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Connect button click to function
        self.add_vehicle_button.clicked.connect(lambda: self.show_add_vehicle_page(self.add_vehicle_button))
        self.home.clicked.connect(lambda: self.show_home_page(self.home))
        self.users_management_button.clicked.connect(lambda: self.show_users_management_button_page(self.users_management_button))
        self.logout_button.clicked.connect(self.logout_function)
    
    def create_navbar(self):
        navbar = QFrame(self)
        navbar.setStyleSheet(""" background-color: #2C3E50; color: white; padding: 2px; """)
        navbar_layout = QHBoxLayout()
        
        # Title on the left
        title_label = QLabel("Vehicle Management System")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        
        # Profile & Logout Buttons on the right
        self.profile_button = QPushButton("Profile")
        self.logout_button = QPushButton("Logout")
        
        for button in [self.profile_button, self.logout_button]:
            button.setStyleSheet("""
                QPushButton { background-color: #2980B9; color: white; border-radius: 5px; padding: 8px 15px; font-size: 14px; }
                QPushButton:hover { background-color: #3498DB; }
            """)
        
        self.profile_button.setIcon(QIcon("assets/icons/profile.png"))
        self.profile_button.setIconSize(QSize(20, 20))
        self.logout_button.setIcon(QIcon("assets/icons/logout.png"))
        self.logout_button.setIconSize(QSize(20, 20))
        
        navbar_layout.addWidget(title_label)
        navbar_layout.addStretch()
        navbar_layout.addWidget(self.profile_button)
        navbar_layout.addWidget(self.logout_button)
        
        navbar.setLayout(navbar_layout)
        return navbar
    
    def create_menu(self):
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignTop)

        self.home = self.create_menu_button("Home", "assets/icons/home.png")
        self.add_vehicle_button = self.create_menu_button("Add New Vehicle", "assets/icons/vehicle_add.png")
        self.view_all_button = self.create_menu_button("View All Vehicles", "assets/icons/vehicle_view.png")
        self.create_report_button = self.create_menu_button("Create Report", "assets/icons/report_create.png")
        self.users_management_button = self.create_menu_button("Users", "assets/icons/users.png")

        for button in [self.home, self.add_vehicle_button, self.view_all_button, self.create_report_button, self.users_management_button]:
            menu_layout.addWidget(button)

        menu_frame = QFrame(self)
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet("background-color: #34495E; color: white; padding: 10px;")
        menu_frame.setFixedWidth(310)

        # self.add_vehicle_button.clicked.connect(self.add_new_vehicle)

        return menu_frame

    def create_menu_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(30, 30))
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setStyleSheet(""" 
            QPushButton { background-color: #34495E; color: white; border-radius: 5px; padding: 10px 20px; text-align: left; }
            QPushButton:hover { background-color: #2980B9; }
        """)
        return button

    def create_welcome_message(self):
        welcome_message = QLabel("Welcome to the Vehicle Maintenance Record Portal", self)
        welcome_message.setAlignment(Qt.AlignCenter)
        welcome_message.setWordWrap(True)
        welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_message.setStyleSheet("color: #2C3E50; padding: 20px;")

        additional_message = QLabel(
            "This portal is designed to streamline and enhance the management of vehicle "
            "maintenance records of 44 AK Pak ARMY", self)
        additional_message.setAlignment(Qt.AlignCenter)
        additional_message.setWordWrap(True)
        additional_message.setFont(QFont("Arial", 14))
        additional_message.setStyleSheet("color: #7F8C8D; padding: 10px;")
        
        empty_page = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(welcome_message)
        layout.addWidget(additional_message)
        empty_page.setLayout(layout)
        return empty_page

    def show_add_vehicle_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.add_vehicle_obj = AddVehicle(self)  # Create AddVehicle widget
        self.content_area.addWidget(self.add_vehicle_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.add_vehicle_obj)  # Switch view

    def show_users_management_button_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.users_obj = Users(self)  # Create AddVehicle widget
        self.content_area.addWidget(self.users_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.users_obj)  # Switch view
    
    def show_home_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.content_area.setCurrentIndex(0)

    def logout_function(self):
        """Log out the user and redirect to the login page."""
        # Close the current window (logging out)
        self.close()  # Closes the current window
        
        # Delay import to avoid circular import issues
        from templates.login import LoginPage  # Importing inside the function
        
        # Open the LoginPage
        self.login_page = LoginPage()  # Create the login page
        self.login_page.show()  # Show the login page