from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, 
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, 
                             QGraphicsDropShadowEffect, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect

import sqlite3
from database import VMS_DB
from templates.add_vehicle import AddVehicle
from templates.users import Users
from templates.view_all_vehicles import ViewALLVehicles
# from templates.login import LoginPage 
from controllers.load_assets import *

class WelcomePage(QWidget):

    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Home - Vehicle Maintenance Module")
        self.setStyleSheet("background-color: #1E1E1E;")
        self.setWindowIcon(QIcon(get_asset_path("assets/images/tank.png")))
        self.setWindowState(Qt.WindowMaximized)
        self.show()
        self.user_session = session
        self.db_obj = VMS_DB()
        self.add_vehicle_obj = AddVehicle(self.user_session)
        self.initUI()

    def update_menu_button_style(self, clicked_button):
        # Reset the style of all buttons
        buttons = [self.home, self.add_vehicle_button, self.view_all_vehicle_button, self.users_management_button]
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

        # Set stretch factors: Menu (index 0) should not stretch, Content area (index 1) should expand
        content_layout.setStretch(0, 0)  # Left menu should not expand
        content_layout.setStretch(1, 1)  # Right content should take up remaining space
        
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Connect button click to function
        self.home.clicked.connect(lambda: self.show_home_page(self.home))
        self.add_vehicle_button.clicked.connect(lambda: self.show_add_vehicle_page(self.add_vehicle_button))
        self.view_all_vehicle_button.clicked.connect(lambda: self.show_all_vehicle_page(self.view_all_vehicle_button))
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
        
        self.profile_button.setIcon(QIcon(get_asset_path("assets/icons/profile.png")))
        self.profile_button.setIconSize(QSize(20, 20))
        self.logout_button.setIcon(QIcon(get_asset_path("assets/icons/logout.png")))
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
        self.view_all_vehicle_button = self.create_menu_button("View All Vehicles", "assets/icons/vehicle_view.png")
        self.users_management_button = self.create_menu_button("Users", "assets/icons/users.png")

        for button in [self.home, self.add_vehicle_button, self.view_all_vehicle_button, self.users_management_button]:
            menu_layout.addWidget(button)

        # Add toggle button at the bottom of the menu
        self.toggle_button = QPushButton("Toggle Menu")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("""
            QPushButton { background-color: #2C3E50; color: white; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #3498DB; }
        """)
        self.toggle_button.clicked.connect(self.toggle_menu)
        menu_layout.addWidget(self.toggle_button)

        menu_frame = QFrame(self)
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet("background-color: #34495E; color: white; padding: 10px;")
        # menu_frame.setFixedWidth(310)
        menu_frame.setMinimumWidth(310)
        menu_frame.setMaximumWidth(310)
        self.menu_frame = menu_frame
        return menu_frame

    def create_menu_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(get_asset_path(icon_path)))
        button.setIconSize(QSize(30, 30))
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setStyleSheet(""" 
            QPushButton { background-color: #34495E; color: white; border-radius: 5px; padding: 10px 20px; text-align: left; }
            QPushButton:hover { background-color: #2980B9; }
        """)
        return button
    
    def toggle_menu(self):
        # Determine the target width based on current width.
        current_width = self.menu_frame.width()
        print("current_width:",current_width)
        if current_width > 50:
            new_width = 50
            self.toggle_button.setText("Expand Menu")
        else:
            new_width = 310
            self.toggle_button.setText("Collapse Menu")

        # Animate the transition for a smoother user experience
        self.animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation.setDuration(250)  # duration in milliseconds
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(new_width)
        self.animation.start()

        self.animation = QPropertyAnimation(self.menu_frame, b"geometry")
        # self.animation.setDuration(250)
        # self.animation.setStartValue(self.menu_frame.geometry())
        # self.animation.setEndValue(QRect(self.menu_frame.x(), self.menu_frame.y(), new_width, self.menu_frame.height()))
        # self.animation.start()

    def create_welcome_message(self):
        all_vehicle_data = self.db_obj.get_all_vehicle()
        welcome_message = QLabel("Welcome to the Vehicle Maintenance Record Portal", self)
        welcome_message.setAlignment(Qt.AlignCenter)
        welcome_message.setWordWrap(True)
        welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_message.setStyleSheet("color: #2C3E50; padding: 20px;")

        # --- Summary Section ---
        total_vehicles = len(all_vehicle_data)  # Count total vehicles
        print(f"total_vehicles: {total_vehicles}")
        summary_label = QLabel(f"🚗 **Total Vehicles: {total_vehicles}**", self)
        summary_label.setAlignment(Qt.AlignCenter)
        summary_label.setFont(QFont("Arial", 16, QFont.Bold))
        summary_label.setStyleSheet("color: #27AE60; padding: 10px;")

        # --- Vehicle Data Table ---
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["BA No.", "Make & Type", "Status"])
        table.setRowCount(len(all_vehicle_data))

        table.setStyleSheet("""
            QTableView { border: 1px solid #ddd; background-color: white; border-radius: 8px; font-size: 18px; }
            QTableWidget {border: 1px solid #ddd; background-color: white; border-radius: 6px; }
            QHeaderView::section { background-color: #007BFF; color: white; font-weight: bold; padding: 8px; }
            QTableWidgetItem { padding: 8px; }
        """)

        # Populate table with data
        for row, vehicle in enumerate(all_vehicle_data):
            table.setItem(row, 0, QTableWidgetItem(str(vehicle["ba_no_input"])))
            table.setItem(row, 1, QTableWidgetItem(str(vehicle["make_type_input"])))
            table.setItem(row, 2, QTableWidgetItem(str(vehicle["overhaul_remarks_input"])))

        # Properly resize table to remove empty space
        table.resizeRowsToContents()
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Hide empty vertical header (removes extra index column)
        table.verticalHeader().setVisible(False)
        
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # --- Additional Info ---

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
        layout.addWidget(summary_label)
        layout.addWidget(table)
        layout.addWidget(additional_message)
        layout.setSpacing(15)  # Spacing between elements
        empty_page.setLayout(layout)
        return empty_page

    def show_add_vehicle_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.add_vehicle_obj = AddVehicle(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.add_vehicle_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.add_vehicle_obj)  # Switch view

    def show_users_management_button_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.users_obj = Users(self)
        self.content_area.addWidget(self.users_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.users_obj)  # Switch view
    
    def show_home_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.content_area.setCurrentIndex(0)

    def show_all_vehicle_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        if hasattr(self, "all_vehicle_obj"):
            self.content_area.removeWidget(self.all_vehicle_obj)
            self.all_vehicle_obj.deleteLater()
            
        self.update_menu_button_style(clicked_button)
        self.all_vehicle_obj = ViewALLVehicles(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.all_vehicle_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.all_vehicle_obj)  # Switch view

    def logout_function(self):
        """Log out the user and redirect to the login page."""
        self.user_session = None
        self.close()
        from templates.login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()