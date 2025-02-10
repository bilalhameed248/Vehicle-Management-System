from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QVBoxLayout, QPushButton, QTableView, QHBoxLayout, QComboBox,
    QLineEdit, QHeaderView, QStyledItemDelegate, QHBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import QTimer, QSize
from database import VMS_DB
from controllers.load_assets import *


class UpdateUserDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()  # Database connection
        self.user_id = user_id  # Store the user ID for updating
        self.setWindowTitle("Update User")
        self.setFixedSize(500, 400)  # Adjusted size for better spacing
        self.setStyleSheet("background-color: #f4f4f4; border-radius: 10px;")
        self.setWindowIcon(QIcon(get_asset_path("assets/icons/edit_user.png")))
        
        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Label
        title_label = QLabel("Update User")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333;")
        layout.addWidget(title_label)

        # Form Layout
        form_layout = QGridLayout()

        # Styled Input Fields
        self.name_input = self.create_input_field("Enter full name")
        self.username_input = self.create_input_field("Enter username")
        self.email_input = self.create_input_field("Enter email")
        self.password_input = self.create_input_field("Enter password", password=True)

        # Blocked Status Select Box (Yes/No)
        self.blocked_combo = QComboBox()
        self.blocked_combo.addItem("Yes")
        self.blocked_combo.addItem("No")
        self.blocked_combo.setStyleSheet("""
            QComboBox {background-color: #f0f0f0;border: 2px solid #4a90e2; border-radius: 5px; padding: 5px; font-size: 14px; color: #333;}
            QComboBox::drop-down {border-left: 2px solid #4a90e2; background-color: #e6e6e6;}
            QComboBox::down-arrow {image: url('path_to_your_arrow_icon.png');  /* Optional: custom arrow icon */}
            QComboBox QAbstractItemView {background-color: white;border: 1px solid #4a90e2;selection-background-color: #4a90e2; selection-color: white;}
            QComboBox::item {padding: 8px;}
            QComboBox::item:selected {background-color: #4a90e2;color: white;}""")
        
        form_layout.addWidget(QLabel("Name:"), 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(QLabel("Username:"), 1, 0)
        form_layout.addWidget(self.username_input, 1, 1)
        form_layout.addWidget(QLabel("Email:"), 2, 0)
        form_layout.addWidget(self.email_input, 2, 1)
        form_layout.addWidget(QLabel("Password:"), 3, 0)
        form_layout.addWidget(self.password_input, 3, 1)
        form_layout.addWidget(QLabel("Blocked:"), 4, 0)
        form_layout.addWidget(self.blocked_combo, 4, 1)

        layout.addLayout(form_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(" Update")
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

        # Load user data from the database
        self.load_user_data()

    def create_input_field(self, placeholder, password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(
            "background: white; border: 1px solid #ccc; border-radius: 5px; padding: 5px;"
        )
        if password:
            field.setEchoMode(QLineEdit.Password)
        return field

    def style_button(self, button, color):
        button.setStyleSheet(f"""background-color: {color}; color: white; border-radius: 5px; padding: 8px;font-weight: bold;""")

    def load_user_data(self):
        """ Loads the user data from the database and populates the fields """
        # Fetch user data by user_id
        user_data = self.db_obj.fetch_user_by_id(self.user_id)
        
        if user_data:
            name, username, email, password, is_blocked = user_data

            # Set fields with the fetched data
            self.name_input.setText(name)
            self.username_input.setText(username)
            self.email_input.setText(email)
            self.password_input.setText(password)  # You might want to keep the password hidden
            self.blocked_combo.setCurrentIndex(0 if is_blocked else 1)  # Set Blocked status (Yes or No)
        else:
            QMessageBox.warning(self, "Error", "User not found!")

    def save_user(self):
        """ Inserts user into the database """
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        is_blocked = 0 if self.blocked_combo.currentIndex() == 1 else 1

        if not name or not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            self.db_obj.update_user_in_db(name, email, username, password, is_blocked, self.user_id)
            QMessageBox.information(self, "Success", "User updated successfully!")
            self.accept()  # Close dialog
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error adding user: {str(e)}")


