from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
from database import VMS_DB
from templates.welcome import WelcomePage
from controllers.load_assets import *

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Vehicle Maintenance Module")
        self.setStyleSheet("background-color: #1E1E1E;")
        self.setWindowIcon(QIcon(get_asset_path("assets/images/tank.png")))
        self.initUI()
        self.setWindowState(Qt.WindowMaximized)
        self.show()
        self.db_obj = VMS_DB()

    def initUI(self):
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(get_asset_path("assets/images/login_bg.jpg")))
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        # Main Layout
        self.container = QWidget(self)
        self.container.setFixedSize(600, 500)
        self.container.setStyleSheet("background: rgba(0, 0, 0, 0.7); border-radius: 20px;")

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(40,40,40,40)
        
        # Title
        self.title = QLabel("Vehicle Maintenance Module")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setStyleSheet("color: #FFFFFF;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Username Field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setText("zahid44")  # Hardcoded username
        self.username_input.setStyleSheet(self.inputStyle())
        self.username_input.returnPressed.connect(self.check_credentials)  # Added line
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setText("Z44ahid")  # Hardcoded password
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.inputStyle())
        self.password_input.returnPressed.connect(self.check_credentials)  # Added line
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(self.buttonStyle())
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet(self.closeButtonStyle())
        self.close_button.clicked.connect(self.closeApp)
        layout.addWidget(self.close_button)

        # Grid Layout for Centering
        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.bg_label, 0, 0)  # Background image
        grid_layout.addWidget(self.container, 0, 0, Qt.AlignCenter)  # Center Login Form
        #grid_layout.addWidget(self.container, 0, 0, Qt.AlignBottom | Qt.AlignRight)  # Login Form Bottom-Right
        

    def resizeEvent(self, event):
        """Resize background image dynamically when the window resizes."""
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

    def inputStyle(self):
        return """
            QLineEdit { background: rgba(255, 255, 255, 0.2); border: none; padding: 10px; border-radius: 10px; color: white; font-size: 14px; }
            QLineEdit::placeholder {color: #CCCCCC;}
        """
    
    def buttonStyle(self):
        return """
            QPushButton { background: #ff9800; border: none; padding: 12px; border-radius: 10px; font-size: 16px; color: white;}
            QPushButton:hover {background: #e68900;}
        """
    
    def closeButtonStyle(self):
        return """
            QPushButton { background: #ff3b30; border: none; padding: 12px; border-radius: 10px; font-size: 16px; color: white;}
            QPushButton:hover { background: #d32f2f; }
        """
    
    def closeApp(self):
        self.close()

    def open_welcome_page(self):
        """Close login page and show welcome page"""
        self.close() 
        self.welcome_window = WelcomePage(self.user_session)
        self.welcome_window.show()

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return
        user = self.db_obj.get_user_by_username(username)
        if user:
            user_id, db_username, db_password, is_blocked = user
            if is_blocked:
                QMessageBox.critical(self, "Blocked", "Your account is blocked. Contact admin.")
            elif password == db_password:  # You should hash passwords instead!
                # QMessageBox.information(self, "Login Successful", f"Welcome {db_username}!")
                self.user_session = {
                    'user_id': user_id,
                    'username': db_username
                }
                self.open_welcome_page()
            else:
                QMessageBox.warning(self, "Error", "Incorrect password!")
        else:
            QMessageBox.warning(self, "Error", "User not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginPage()
    login_window.show()
    sys.exit(app.exec_())