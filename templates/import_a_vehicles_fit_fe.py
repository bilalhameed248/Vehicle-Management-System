from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QGridLayout, QDialog)
from PyQt5.QtGui import  QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from controllers.load_assets import *
from controllers.import_a_vehicles_fit import ImportAVehiclesFit

class ImportAVehiclesFitFE(QDialog):

    def __init__(self, user_session=None, parent=None, db_to_display = None):
        super().__init__(parent)       
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username') 
        self.db_to_display = db_to_display
        self.import_dialogbox()
    
    def import_dialogbox(self):
        self.setWindowTitle("Import Vehicles")
        self.setFixedSize(450, 300)  # Adjusted size for better spacing
        self.setStyleSheet("background-color: #f4f4f4; border-radius: 10px;")
        self.setWindowIcon(QIcon(get_asset_path("assets/icons/vehicle_add.png")))
        
        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Label
        title_label = QLabel("Import Vehicles")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333;")
        layout.addWidget(title_label)

        # Form Layout
        form_layout = QGridLayout()

        # File Input Field
        self.file_input = QPushButton("Select File")
        self.file_input.setStyleSheet("background-color: #3498db; color: white; padding: 4px; border-radius: 5px;")
        self.file_input.clicked.connect(self.select_file)
        form_layout.addWidget(QLabel("Choose File:"), 2, 0)
        file_label = QLabel("No file selected")
        file_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        form_layout.addWidget(self.file_input, 2, 1)
        form_layout.addWidget(file_label, 3, 1)

        layout.addLayout(form_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(" Import")
        self.save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        self.save_button.setIconSize(QSize(20, 20))
        self.cancel_button = QPushButton(" Cancel")
        self.cancel_button.setIcon(QIcon(get_asset_path("assets/icons/cancel.png")))
        self.cancel_button.setIconSize(QSize(20, 20))

        self.style_button(self.save_button, "#28a745")
        self.style_button(self.cancel_button, "#dc3545")

        self.save_button.clicked.connect(self.import_vehicles_fun)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load user data from the database
        # self.load_vehicles_data()

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            self.selected_file = file_path
            self.file_input.setText(file_path)

    def style_button(self, button, color):
        button.setStyleSheet(f"""background-color: {color}; color: white; border-radius: 5px; padding: 8px;font-weight: bold;""")


    def import_vehicles_fun(self):
        if hasattr(self, 'selected_file') and self.selected_file:
            excel_path = self.selected_file  # Get the selected file path
            try:
                self.imp_veh_obj = ImportAVehiclesFit(user_session=self.user_session, db_to_display=self.db_to_display)
                is_successfully_import = self.imp_veh_obj.read_and_insert_excel(excel_path)
                if is_successfully_import:
                    QMessageBox.information(self, "Success", "Vehicles imported successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", f"Failed to import Vehicles")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import file: {str(e)}")
        else:
            QMessageBox.warning(self, "No File", "Please select a file before importing.")