import sys
from PyQt5.QtWidgets import QApplication
from templates.login import LoginPage

def main():
    app = QApplication(sys.argv)
    
    # Create and show the login window
    login_window = LoginPage()
    login_window.show()
    
    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
