from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, 
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, QToolButton,
                             QGraphicsDropShadowEffect, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect

import sqlite3
from controllers.load_assets import *
from database import VMS_DB
from templates.welcome_summary import WelcomeSummary
from templates.add_vehicle import AddVehicle
from templates.view_all_vehicles import ViewALLVehicles
from templates.add_weapon import AddWeapon
from templates.view_all_weapons import ViewALLWeapons
from templates.view_all_a_vehicles_fit import ViewALLAVehiclesFit
from templates.add_a_vehicle_fit import AddAVehicleFit
from templates.users import Users
from templates.navbar import ATNavbar

class WelcomePage(QWidget):

    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Home - ArmourTrack-44AK")
        self.setStyleSheet("background-color: #1E1E1E;")
        self.setWindowIcon(QIcon(get_asset_path("assets/images/tank.png")))
        self.setWindowState(Qt.WindowMaximized)
        self.show()
        self.user_session = session
        self.db_obj = VMS_DB()
        self.welcome_summary_obj = WelcomeSummary()
        self.add_vehicle_obj = AddVehicle(self.user_session)
        self.nav_obj = ATNavbar(parent=self)
        self.initUI()


    def initUI(self):
        self.main_layout = QVBoxLayout()
        
        # Top Navigation Bar
        navbar = self.nav_obj.create_navbar()
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

    
    def create_menu(self):
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(10)
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

        # Home Button (Top-level item)
        self.home = self.create_menu_button(" Home", "assets/icons/home.png")
        menu_layout.addWidget(self.home)

        # Vehicle Category
        vehicle_header = self.create_category_header("Vehicle", "assets/icons/vehicle.png")
        self.vehicle_container = self.create_category_container([
            (" Add New Vehicle", "assets/icons/vehicle_add.png", "add_vehicle_button"),
            (" View All Vehicles", "assets/icons/vehicle_view.png", "view_all_vehicle_button"),
            (" Add A Vehicle", "assets/icons/a_veh.png", "add_A_vehicle_fit_button"),
            (" View All A Vehicles", "assets/icons/a_veh_view.png", "view_A_vehicle_fit_button")
        ])
        vehicle_header.clicked.connect(lambda: self.toggle_category(vehicle_header, self.vehicle_container))
        menu_layout.addWidget(vehicle_header)
        menu_layout.addWidget(self.vehicle_container)

        # Weapon Category 
        weapon_header = self.create_category_header("Weapon", "assets/icons/weapon.png")
        self.weapon_container = self.create_category_container([
            (" Add New Weapon", "assets/icons/add_weapon.png", "add_weapon_button"),
            (" View All Weapons", "assets/icons/view_all_weapons.png", "view_all_weapon_button")
        ])
        weapon_header.clicked.connect(lambda: self.toggle_category(weapon_header, self.weapon_container))
        menu_layout.addWidget(weapon_header)
        menu_layout.addWidget(self.weapon_container)

        # Settings Category
        settings_header = self.create_category_header("Settings", "assets/icons/setting.png")
        self.settings_container = self.create_category_container([
            (" Users", "assets/icons/users.png", "users_management_button")
        ])
        settings_header.clicked.connect(lambda: self.toggle_category(settings_header, self.settings_container))
        menu_layout.addWidget(settings_header)
        menu_layout.addWidget(self.settings_container)

        # Connect button click to function
        self.home.clicked.connect(lambda: self.show_home_page(self.home))
        self.add_vehicle_button.clicked.connect(lambda: self.show_add_vehicle_page(self.add_vehicle_button))
        self.view_all_vehicle_button.clicked.connect(lambda: self.show_all_vehicle_page(self.view_all_vehicle_button))

        self.add_A_vehicle_fit_button.clicked.connect(lambda: self.show_add_A_vehicle_Fit_page(self.add_A_vehicle_fit_button))
        self.view_A_vehicle_fit_button.clicked.connect(lambda: self.show_all_A_vehicle_Fit_page(self.view_A_vehicle_fit_button))

        self.add_weapon_button.clicked.connect(lambda: self.show_add_weapon_page(self.add_weapon_button))
        self.view_all_weapon_button.clicked.connect(lambda: self.show_all_weapon_page(self.view_all_weapon_button))

        self.users_management_button.clicked.connect(lambda: self.show_users_management_button_page(self.users_management_button))

        # Initially collapse all categories
        self.toggle_category(vehicle_header, self.vehicle_container)
        self.toggle_category(weapon_header, self.weapon_container)
        self.toggle_category(settings_header, self.settings_container)

        menu_frame = QFrame(self)
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet("background-color: #34495E; color: white; padding: 10px;")
        menu_frame.setFixedWidth(310)
        return menu_frame
        

    def create_category_header(self, title, icon_path):
        header = QToolButton()
        header.setText(title)
        header.setIcon(QIcon(get_asset_path(icon_path)))
        header.setIconSize(QSize(24, 24))  # Critical addition
        header.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        header.setArrowType(Qt.RightArrow)  # Default to right arrow (collapsed)
        # header.setArrowType(Qt.DownArrow)
        header.setCheckable(True)
        # header.setChecked(True)
        header.setChecked(False)  # Start collapsed
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header.setStyleSheet("""
            QToolButton { background-color: #2C3E50; color: white; border-radius: 5px; padding: 10px 20px;
                text-align: left; font-weight: bold; font-size: 18px; }
            QToolButton:hover { background-color: #3498DB; }
            QToolButton::menu-indicator { image: none; }
        """)
        return header


    def create_category_container(self, items):
        container = QWidget()
        container.setVisible(False)
        # container.setVisible(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Indent subitems
        layout.setSpacing(8)

        for text, icon, attr_name in items:
            btn = self.create_menu_button(text, icon)
            setattr(self, attr_name, btn)
            layout.addWidget(btn)

        container.setLayout(layout)
        return container

    def toggle_category(self, header, container):
        if header.isChecked():
            container.show()
            header.setArrowType(Qt.DownArrow)
        else:
            container.hide()
            header.setArrowType(Qt.RightArrow)


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
        button.setIconSize(QSize(26, 26))
        button.setFont(QFont("Arial", 12, QFont.Bold))
        button.setStyleSheet(""" 
            QPushButton { background-color: #34495E; color: white; border-radius: 5px; padding: 10px 20px; text-align: left; }
            QPushButton:hover { background-color: #2980B9; }
        """)
        return button


    def update_menu_button_style(self, clicked_button):
        # Reset the style of all buttons
        buttons = [self.home, self.add_vehicle_button, self.view_all_vehicle_button, self.add_A_vehicle_fit_button, self.view_A_vehicle_fit_button,  self.add_weapon_button, self.view_all_weapon_button, self.users_management_button]
        for button in buttons:
            button.setStyleSheet("""
                QPushButton {background-color: #34495E; color: white; border-radius: 5px; padding: 10px 20px; text-align: left; }
                QPushButton:hover { background-color: #2980B9; }
            """)
        clicked_button.setStyleSheet("""
            QPushButton { background-color: #2980B9; color: white; border-radius: 5px; padding: 10px 20px; text-align: left;}
        """)

    def show_home_page(self, clicked_button):
        
        self.update_menu_button_style(clicked_button)
        # self.content_area.addWidget(self.welcome_summary_obj)  # Add to stacked widget
        self.welcome_summary_obj.load_data_veh()  # Reload fresh data
        self.welcome_summary_obj.load_data_wep()  # Reload fresh data
        self.content_area.setCurrentWidget(self.welcome_summary_obj)  # Switch view

        """Switch to the 'Add New Vehicle' page."""
        # self.update_menu_button_style(clicked_button)
        # self.content_area.setCurrentIndex(0)

    def show_add_vehicle_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.add_vehicle_obj = AddVehicle(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.add_vehicle_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.add_vehicle_obj)  # Switch view


    def show_all_vehicle_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        if hasattr(self, "all_vehicle_obj"):
            self.content_area.removeWidget(self.all_vehicle_obj)
            self.all_vehicle_obj.deleteLater()
            
        self.update_menu_button_style(clicked_button)
        self.all_vehicle_obj = ViewALLVehicles(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.all_vehicle_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.all_vehicle_obj)  # Switch view

    #***********************************************************************************************************************

    def show_add_A_vehicle_Fit_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.add_a_vehicle_fit_obj = AddAVehicleFit(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.add_a_vehicle_fit_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.add_a_vehicle_fit_obj)  # Switch view
    
    def show_all_A_vehicle_Fit_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        if hasattr(self, "all_a_vehicle_fit_obj"):
            self.content_area.removeWidget(self.all_a_vehicle_fit_obj)
            self.all_a_vehicle_fit_obj.deleteLater()
            
        self.update_menu_button_style(clicked_button)
        self.all_a_vehicle_fit_obj = ViewALLAVehiclesFit(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.all_a_vehicle_fit_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.all_a_vehicle_fit_obj)  # Switch view

    #***********************************************************************************************************************

    def show_add_weapon_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.add_weapon_obj = AddWeapon(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.add_weapon_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.add_weapon_obj)  # Switch view


    def show_all_weapon_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        if hasattr(self, "all_weapon_obj"):
            self.content_area.removeWidget(self.all_weapon_obj)
            self.all_weapon_obj.deleteLater()
            
        self.update_menu_button_style(clicked_button)
        self.all_weapon_obj = ViewALLWeapons(user_session=self.user_session, parent=self)
        self.content_area.addWidget(self.all_weapon_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.all_weapon_obj)  # Switch view

    
    def show_users_management_button_page(self, clicked_button):
        """Switch to the 'Add New Vehicle' page."""
        self.update_menu_button_style(clicked_button)
        self.users_obj = Users(self)
        self.content_area.addWidget(self.users_obj)  # Add to stacked widget
        self.content_area.setCurrentWidget(self.users_obj)  # Switch view