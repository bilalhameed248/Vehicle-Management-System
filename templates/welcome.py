from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, 
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, 
                             QGraphicsDropShadowEffect, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect

import sqlite3
from database import VMS_DB
from templates.add_vehicle import AddVehicle
from templates.welcome_summary import WelcomeSummary
from templates.users import Users
from templates.view_all_vehicles import ViewALLVehicles
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
        self.welcome_summary_obj = WelcomeSummary()
        self.add_vehicle_obj = AddVehicle(self.user_session)
        self.initUI()


    def initUI(self):
        self.main_layout = QVBoxLayout()
        
        # Top Navigation Bar
        navbar = self.create_navbar()
        self.main_layout.addWidget(navbar)
        
        # Main Content Area (Horizontal Split: Left Menu & Right Content)
        self.content_layout = QHBoxLayout()
        
        # Left Menu
        self.menu_frame = self.create_menu()
        self.content_layout.addWidget(self.menu_frame)
        
        # Right Content Area
        self.content_area = QStackedWidget()
        self.content_area.addWidget(self.welcome_summary_obj)  # Initial Page
        self.content_layout.addWidget(self.content_area)

        # Set stretch factors: Menu (index 0) should not stretch, Content area (index 1) should expand
        self.content_layout.setStretch(0, 0)  # Left menu should not expand
        self.content_layout.setStretch(1, 5)  # Right content should take up remaining space
        
        
        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

        self.sidebar_expanded = True

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

        # Add toggle button at the bottom of the menu
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setIcon(QIcon(get_asset_path("assets/icons/sidebar.png")))
        self.toggle_button.setIconSize(QSize(24, 24))  # Adjust size if needed
        self.toggle_button.setStyleSheet("""
            QPushButton { background-color: #2C3E50; color: white; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #3498DB; }
        """)
        self.toggle_button.clicked.connect(self.toggle_menu)
        menu_layout.addWidget(self.toggle_button)

        self.home = self.create_menu_button("Home", "assets/icons/home.png")
        self.add_vehicle_button = self.create_menu_button("Add New Vehicle", "assets/icons/vehicle_add.png")
        self.view_all_vehicle_button = self.create_menu_button("View All Vehicles", "assets/icons/vehicle_view.png")
        self.users_management_button = self.create_menu_button("Users", "assets/icons/users.png")

        for button in [self.home, self.add_vehicle_button, self.view_all_vehicle_button, self.users_management_button]:
            menu_layout.addWidget(button)

        menu_frame = QFrame(self)
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet("background-color: #34495E; color: white; padding: 10px;")
        menu_frame.setFixedWidth(310)
        return menu_frame


    def toggle_menu(self):
        """Animates and toggles the sidebar width."""
        new_width = 100 if self.sidebar_expanded else 310
        self.sidebar_expanded = not self.sidebar_expanded
        # self.toggle_button.setText("▶ Expand" if new_width == 50 else "◀ Collapse")

        # Animation for smooth transition
        self.animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.menu_frame.width())
        self.animation.setEndValue(new_width)
        self.animation.start()

        self.animation2 = QPropertyAnimation(self.menu_frame, b"maximumWidth")
        self.animation2.setDuration(300)
        self.animation2.setStartValue(self.menu_frame.width())
        self.animation2.setEndValue(new_width)
        self.animation2.start()

        # Ensuring the width actually changes after animation
        self.animation2.finished.connect(lambda: self.menu_frame.setFixedWidth(new_width))

        # Adjust stretch factor to expand content when menu collapses
        self.content_layout.setStretch(0, 0 if new_width == 50 else 1)
        self.content_layout.setStretch(1, 6 if new_width == 50 else 5)
    

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
        
        self.update_menu_button_style(clicked_button)
        # self.content_area.addWidget(self.welcome_summary_obj)  # Add to stacked widget
        self.welcome_summary_obj.load_data()  # Reload fresh data
        self.content_area.setCurrentWidget(self.welcome_summary_obj)  # Switch view

        """Switch to the 'Add New Vehicle' page."""
        # self.update_menu_button_style(clicked_button)
        # self.content_area.setCurrentIndex(0)


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