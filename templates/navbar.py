from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QScrollArea, 
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget, QSizePolicy, QToolButton,
                             QGraphicsDropShadowEffect, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect
from controllers.load_assets import *


class ATNavbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_parent = parent
        pass

    def create_navbar(self):
        navbar = QFrame(self)
        navbar.setStyleSheet(""" background-color: #2C3E50; color: white; padding: 2px; """)
        navbar_layout = QHBoxLayout()
        
        # Title on the left
        title_label = QLabel("ArmourTrack")
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

        self.logout_button.clicked.connect(self.logout_function)
        
        navbar_layout.addWidget(title_label)
        navbar_layout.addStretch()
        navbar_layout.addWidget(self.profile_button)
        navbar_layout.addWidget(self.logout_button)
        
        navbar.setLayout(navbar_layout)
        return navbar
    
    def logout_function(self):
        """Log out the user and redirect to the login page."""
        self.user_session = None
        # self.close()
        self.main_parent.close()
        from templates.login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()