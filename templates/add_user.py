from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QVBoxLayout, QPushButton, QTableView, QHBoxLayout, QComboBox,
    QLineEdit, QHeaderView, QStyledItemDelegate, QHBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import QTimer, QSize
from database import VMS_DB
from controllers.load_assets import *

class AddUserDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()
        self.setWindowTitle("Add New User")
        self.setFixedSize(500, 400)  # Adjusted size for better spacing
        self.setStyleSheet("background-color: #f4f4f4; border-radius: 10px;")
        self.setWindowIcon(QIcon(get_asset_path("assets/icons/add_user.png")))
        
        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Label
        title_label = QLabel("Add New User")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333;")
        layout.addWidget(title_label)

        # Form Layout
        form_layout = QGridLayout()

        # Styled Input Fields
        self.name_input = self.create_input_field("Enter full name")
        self.username_input = self.create_input_field("Enter username")
        self.password_input = self.create_input_field("Enter password", password=True)

        form_layout.addWidget(QLabel("Name:"), 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(QLabel("Username:"), 1, 0)
        form_layout.addWidget(self.username_input, 1, 1)
        form_layout.addWidget(QLabel("Password:"), 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)
        
        layout.addLayout(form_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(" Save")
        self.save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        self.save_button.setIconSize(QSize(20, 20))
        self.cancel_button = QPushButton(" Cancel")
        self.cancel_button.setIcon(QIcon(get_asset_path("assets/icons/cancel.png")))
        self.cancel_button.setIconSize(QSize(20, 20))

        self.style_button(self.save_button, "#28a745")
        self.style_button(self.cancel_button, "#dc3545")

        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    def create_input_field(self, placeholder, password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet( "background: white; border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        if password:
            field.setEchoMode(QLineEdit.Password)
        return field


    def style_button(self, button, color):
        button.setStyleSheet(f"""background-color: {color}; color: white; border-radius: 5px; padding: 8px; font-weight: bold;""")


    def save_user(self):
        """ Inserts user into the database """
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not name or not username or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return
        try:
            self.db_obj.insert_user(name, username, password)
            QMessageBox.information(self, "Success", "User added successfully!")
            self.accept()  # Close dialog
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error adding user: {str(e)}")