from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QHBoxLayout, QMessageBox,QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import VMS_DB  # Assuming VMS_DB handles database interactions
from controllers.load_assets import *

class Profile(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()  # Database object
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Profile")
        self.setStyleSheet("""
            QWidget { background-color: #f0f2f5; font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel { font-size: 22px; font-weight: bold; padding: 10px; color: #333; }
            QPushButton { background-color: #007BFF; color: white; padding: 8px 12px; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
            QTableWidget { border: 1px solid #ddd; background-color: white; border-radius: 8px; }
            QTableWidget::item { padding: 8px; }
            QTableWidget::item:selected { background-color: #d0e2ff; }
        """)

        layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        # User Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Blocked", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.setStyleSheet("QTableWidget { border: none; }")

        layout.addWidget(self.user_table)

        self.load_users()

        self.setLayout(layout)