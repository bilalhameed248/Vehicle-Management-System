from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, 
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, QToolButton,
                             QGraphicsDropShadowEffect, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect
from controllers.load_assets import *

class Sidebar:
    
    def __init__(self):
        pass

    def menu_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #BDC3C7; height: 1px;")
        return separator
    

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
        self.home = self.create_menu_button("Home", "assets/icons/home.png")
        menu_layout.addWidget(self.home)

        # Vehicle Category
        vehicle_header = self.create_category_header("Vehicle", "assets/icons/vehicle.png")
        self.vehicle_container = self.create_category_container([
            ("Add New Vehicle", "assets/icons/vehicle_add.png", "add_vehicle_button"),
            ("View All Vehicles", "assets/icons/vehicle_view.png", "view_all_vehicle_button"),
            ("A VEH Fitness", "assets/icons/a_veh.png", "add_A_vehicle_fit_button"),
            ("A VEH Fitness Check", "assets/icons/a_veh_view.png", "view_A_vehicle_fit_button")
        ])
        vehicle_header.clicked.connect(lambda: self.toggle_category(vehicle_header, self.vehicle_container))
        menu_layout.addWidget(vehicle_header)
        menu_layout.addWidget(self.vehicle_container)

        # Weapon Category
        weapon_header = self.create_category_header("Weapon", "assets/icons/weapon.png")
        self.weapon_container = self.create_category_container([
            ("Add New Weapon", "assets/icons/add_weapon.png", "add_weapon_button"),
            ("View All Weapon", "assets/icons/view_all_weapons.png", "view_all_weapon_button")
        ])
        weapon_header.clicked.connect(lambda: self.toggle_category(weapon_header, self.weapon_container))
        menu_layout.addWidget(weapon_header)
        menu_layout.addWidget(self.weapon_container)

        # Settings Category
        settings_header = self.create_category_header("Settings", "assets/icons/settings.png")
        self.settings_container = self.create_category_container([
            ("Users", "assets/icons/users.png", "users_management_button")
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
        header.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        header.setArrowType(Qt.RightArrow)  # Default to right arrow (collapsed)
        # header.setArrowType(Qt.DownArrow)
        header.setCheckable(True)
        # header.setChecked(True)
        header.setChecked(False)  # Start collapsed
        header.setStyleSheet("""
            QToolButton { background-color: #2C3E50; color: white; border-radius: 5px; padding: 10px 20px;
                text-align: left; font-weight: bold; font-size: 13px; }
            QToolButton:hover { background-color: #3498DB; }
            QToolButton::menu-indicator { image: none; }
        """)
        return header

    def create_category_container(self, items):
        container = QWidget()
        container.setVisible(False)
        # container.setVisible(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 5, 5, 5)  # Indent subitems
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


    def create_menu1(self):
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

        self.add_A_vehicle_fit_button = self.create_menu_button("A VEH Fitness", "assets/icons/a_veh.png")
        self.view_A_vehicle_fit_button = self.create_menu_button("A VEH Fitness Check", "assets/icons/a_veh_view.png")

        self.add_weapon_button = self.create_menu_button("Add New Weapon", "assets/icons/add_weapon.png")
        self.view_all_weapon_button = self.create_menu_button("View All Weapon", "assets/icons/view_all_weapons.png")
        
        self.users_management_button = self.create_menu_button("Users", "assets/icons/users.png")

        for button in [self.home, self.add_vehicle_button, self.view_all_vehicle_button, self.add_A_vehicle_fit_button, self.view_A_vehicle_fit_button, self.add_weapon_button, self.view_all_weapon_button, self.users_management_button]:
            menu_layout.addWidget(button)
            if button in [self.view_all_vehicle_button, self.view_A_vehicle_fit_button, self.view_all_weapon_button]:
                menu_layout.addWidget(self.menu_separator())

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