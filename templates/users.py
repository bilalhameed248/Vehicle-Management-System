from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QVBoxLayout, QPushButton, QTableView, QHBoxLayout, QComboBox,
    QLineEdit, QHeaderView, QStyledItemDelegate, QHBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import QTimer, QSize
from database import VMS_DB  
from templates.add_user import AddUserDialog
from templates.update_user import UpdateUserDialog
from controllers.users import UserFilterProxy, ButtonDelegate
from controllers.load_assets import *

class Users(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Management")
        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa; font-family: 'Segoe UI', Arial, sans-serif; font-size: 18px;  }
            QLabel { font-size: 24px; font-weight: bold; padding: 10px; color: #333; }
            QPushButton { background-color: #007BFF; color: white; padding: 8px 12px; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #0056b3; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 18px; }
            QTableView { border: 1px solid #ddd; background-color: white; border-radius: 8px; font-size: 18px; }
        """)

        layout = QVBoxLayout()

        title_label = QLabel("User Management")
        title_label.setStyleSheet("border-radius: 5px; padding: 4px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Search Box (Right)
        search_layout = QHBoxLayout()

        # Add User Button (Left)
        self.add_user_button = QPushButton(" Add User")
        self.add_user_button.setIcon(QIcon(get_asset_path("assets/icons/add_user.png")))
        self.add_user_button.setIconSize(QSize(20, 20))
        self.add_user_button.setFixedSize(130, 40)  # Set size
        self.add_user_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px; font-weight: bold;")
        self.add_user_button.clicked.connect(self.add_user)

        # Search Box (Right)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filter_users)  

        # Add widgets in the correct order
        search_layout.addWidget(self.add_user_button)
        search_layout.addStretch()
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)

        self.model = QStandardItemModel(0, 5)  # 5 Columns (Including Action Buttons)
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Username", "Blocked", "Actions"])

        # Proxy Model for filtering
        self.proxy_model = UserFilterProxy(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.user_table = QTableView()
        self.user_table.setModel(self.proxy_model)
        self.user_table.setSortingEnabled(True)  
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Set Delegate for Action Buttons
        self.user_table.setItemDelegateForColumn(4, ButtonDelegate(self.user_table))
        layout.addWidget(self.user_table)
        self.load_users()
        self.user_table.hideColumn(0)
        self.setLayout(layout)

    def filter_users(self):
        """ Search users dynamically and refresh buttons after filtering """
        search_text = self.search_input.text()
        self.proxy_model.setFilterFixedString(search_text)
        QTimer.singleShot(100, self.refresh_action_buttons)

    def refresh_action_buttons(self):
        """ Reapply action buttons to all visible rows after filtering """
        for row in range(self.proxy_model.rowCount()):
            proxy_index = self.proxy_model.index(row, 4)  # Column 5 (Actions)
            source_index = self.proxy_model.mapToSource(proxy_index)
            source_row = source_index.row()
            button_delegate = ButtonDelegate(self.user_table)
            button_widget = button_delegate.create_buttons(self.user_table, source_row)
            self.user_table.setIndexWidget(proxy_index, button_widget)

    def load_users(self):
        users = self.db_obj.fetch_users()
        self.model.setRowCount(0)  

        for row, user in enumerate(users):
            id, name, username, is_blocked = user
            items = [
                QStandardItem(str(id)),
                QStandardItem(name),
                QStandardItem(username),
                QStandardItem("Yes" if is_blocked else "No"),
                QStandardItem("")  # Empty item for action buttons
            ]
            self.model.appendRow(items)
            # If user is blocked, change text color to red
            if is_blocked:
                for item in items:
                    # item.setBackground(Qt.red)
                    item.setForeground(Qt.red)  # White text for contrast

            # Get the correct model index
            model_index = self.model.index(row, 4)
            proxy_index = self.proxy_model.mapFromSource(model_index)
            button_delegate = ButtonDelegate(self.user_table)
            button_widget = button_delegate.create_buttons(self.user_table, row)
            self.user_table.setIndexWidget(proxy_index, button_widget)
        self.proxy_model.sort(0, Qt.AscendingOrder)

    def edit_user(self, row):
        """ Edit user logic """
        user_id = self.model.item(row, 0).text()
        dialog = UpdateUserDialog(user_id, self)
        if dialog.exec_():  # If user clicks Save
            self.load_users()  # Refresh user list after update

    def delete_user(self, row):
        """ Deletes user from the database """
        user_id = self.model.item(row, 0).text()
        user_name = self.model.item(row, 1).text()
        confirm = QMessageBox(self)

        confirm.setWindowTitle("Delete User")
        confirm.setWindowIcon(QIcon(get_asset_path("assets/icons/delete.png")))  # Replace with your actual icon path
        confirm.setText(f"Are you sure you want to delete user {user_name}?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = confirm.exec_()
        # confirm = QMessageBox.question(self, "Delete User", f"Are you sure you want to delete user {user_name}?",QMessageBox.Yes | QMessageBox.No)

        if result == QMessageBox.Yes:
            self.db_obj.delete_user(user_id)
            self.load_users()  # Refresh table

    def add_user(self):
        """ Opens a form or dialog to add a new user """
        # QMessageBox.information(self, "Add User", "Add User button clicked!")
        dialog = AddUserDialog(self)
        if dialog.exec_():  # If user clicks Save
            self.load_users()  # Refresh user table