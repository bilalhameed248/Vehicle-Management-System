from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QHBoxLayout, QMessageBox,QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import VMS_DB  # Assuming VMS_DB handles database interactions

class Users(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()  # Database object
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Management")
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

        # Title
        title_label = QLabel("User Management")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        header_layout = QHBoxLayout()

        # Left side (Search)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setFixedWidth(300)
        search_button = QPushButton("Search")
        search_button.setMaximumWidth(100)
        search_button.clicked.connect(self.search_users)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        header_layout.addLayout(search_layout)

        # Right side (Add User)
        add_user_button = QPushButton("Add User")
        add_user_button.setStyleSheet("background-color: #28a745; color: white; padding: 10px 20px; border-radius: 6px; font-weight: bold;")
        # add_user_button.clicked.connect(self.add_user)
        add_user_button.setMaximumWidth(100)
        header_layout.addWidget(add_user_button)

        # Add the header layout to the main layout
        layout.addLayout(header_layout)

        # User Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Blocked", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.setStyleSheet("QTableWidget { border: none; }")

        layout.addWidget(self.user_table)

        self.load_users()

        self.setLayout(layout)

    def search_users(self):
        """ Placeholder for search function """
        print("Searching for:", self.search_input.text())

    def load_users(self):
        """Fetches users from the database and populates the table."""
        users = self.db_obj.fetch_users()  # Fetch users from the database
        self.user_table.setRowCount(len(users))

        for row, user in enumerate(users):
            id, username, email, is_blocked = user

            self.user_table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(username))
            self.user_table.setItem(row, 2, QTableWidgetItem(email))
            self.user_table.setItem(row, 3, QTableWidgetItem("Yes" if is_blocked else "No"))

            # Action Buttons (Edit, Delete)
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #28a745; color: black; border-radius: 3px; padding: 4px;")
            edit_button.clicked.connect(lambda checked, id=id: self.edit_user(id))

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #dc3545; color: black; border-radius: 3px; padding: 4px;")
            delete_button.clicked.connect(lambda checked, id=id: self.delete_user(id))

            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.setAlignment(Qt.AlignCenter)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.user_table.setCellWidget(row, 4, button_widget)

    def edit_user(self, user_id):
        """Edit user logic here"""
        QMessageBox.information(self, "Edit User", f"Editing User ID: {user_id}")

    def delete_user(self, user_id):
        """Deletes user from the database."""
        confirm = QMessageBox.question(self, "Delete User", f"Are you sure you want to delete user ID {user_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db_obj.delete_user(user_id)
            self.load_users()  # Refresh table

