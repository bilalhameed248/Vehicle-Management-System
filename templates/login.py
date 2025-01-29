from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys
import sqlite3
from database import get_user_by_username  # Import database functions

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Vehicle Maintenance System")
        self.setGeometry(100, 100, 400, 300)  # Window size
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return

        user = get_user_by_username(username)
        
        if user:
            user_id, db_username, db_password, is_blocked = user
            if is_blocked:
                QMessageBox.critical(self, "Blocked", "Your account is blocked. Contact admin.")
            elif password == db_password:  # You should hash passwords instead!
                QMessageBox.information(self, "Login Successful", f"Welcome {db_username}!")
                self.close()  # Close login window after successful login
            else:
                QMessageBox.warning(self, "Error", "Incorrect password!")
        else:
            QMessageBox.warning(self, "Error", "User not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginPage()
    login_window.show()
    sys.exit(app.exec_())