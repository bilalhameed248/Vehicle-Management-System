from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QFileDialog, 
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox, QGridLayout, QDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from database import VMS_DB
from templates.vehicle_report import VehicleReport
from templates.update_vehicle import UpdateVehicle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from controllers.load_assets import *
from controllers.import_vehicles import ImportVehicles
import math

class ImportVehiclesFE(QDialog):

    def __init__(self):
        self.imp_veh_obj = ImportVehicles()

    def import_button(self):
        import_button = QPushButton("Export")
        import_button.setFixedSize(100, 45)  # Set button size
        import_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #218838; }
        """)
        import_button.setIcon(QIcon(get_asset_path("assets/icons/xlsx.png")))
        import_button.setIconSize(QSize(20, 20))
        import_button.clicked.connect(self.import_vehicle)
        return import_button
    
    def import_dialogbox(self):
        self.setWindowTitle("Import Vehicles")
        self.setFixedSize(500, 400)  # Adjusted size for better spacing
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
        self.file_input.clicked.connect(self.select_file)
        form_layout.addWidget(QLabel("Select File:"), 2, 0)
        form_layout.addWidget(self.file_input, 2, 1)

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

        self.save_button.clicked.connect(self.import_vehicles)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load user data from the database
        self.load_vehicles_data()

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.file_input.setText(file_path)

    def style_button(self, button, color):
        button.setStyleSheet(f"""background-color: {color}; color: white; border-radius: 5px; padding: 8px;font-weight: bold;""")


    def import_vehicles(self):
        excel_path = ""
        self.imp_veh_obj.read_and_insert_excel(excel_path)