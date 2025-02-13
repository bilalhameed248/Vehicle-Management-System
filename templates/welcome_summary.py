from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                              QTableWidgetItem, QHeaderView, QAbstractItemView)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import VMS_DB

class WelcomeSummary(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()
        self.init_ui()
    
    def init_ui(self):
        """Initializes UI components."""
        self.layout = QVBoxLayout()
        
        # Welcome Message
        self.welcome_message = QLabel("Welcome to the Vehicle Maintenance Record Portal", self)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setWordWrap(True)
        self.welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        self.welcome_message.setStyleSheet("color: #2C3E50; padding: 20px;")
        self.layout.addWidget(self.welcome_message)
        
        # Total Vehicle Summary Label
        self.total_vehicle_label = QLabel("", self)
        self.total_vehicle_label.setAlignment(Qt.AlignCenter)
        self.total_vehicle_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_vehicle_label.setStyleSheet("color: #27AE60; padding: 10px;")
        self.layout.addWidget(self.total_vehicle_label)

        # Vehicle Summary
        summary_layout = QHBoxLayout()
        self.vehicle_summary_label = QLabel("Vehicle Summary", self)
        self.vehicle_summary_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.vehicle_summary_label.setStyleSheet("color: #27AE60; padding: 10px;")
        summary_layout.addWidget(self.vehicle_summary_label)
        self.layout.addLayout(summary_layout)

        # Table Setup
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Category", "BA No.", "Make & Type", "Status"])
        self.table.setStyleSheet("""
            QTableView { border: 1px solid #ddd; background-color: white; border-radius: 8px; font-size: 18px; }
            QTableWidget {border: 1px solid #ddd; background-color: white; border-radius: 6px; }
            QHeaderView::section { background-color: #007BFF; color: white; font-weight: bold; padding: 8px; }
            QTableWidgetItem { padding: 8px; }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table, alignment=Qt.AlignCenter)
        
        # Additional Information Label
        self.additional_message = QLabel(
            "This portal is designed to streamline and enhance the management of vehicle "
            "maintenance records of 44 AK Pak ARMY", self)
        self.additional_message.setAlignment(Qt.AlignCenter)
        self.additional_message.setWordWrap(True)
        self.additional_message.setFont(QFont("Arial", 14))
        self.additional_message.setStyleSheet("color: #7F8C8D; padding: 10px;")
        self.layout.addWidget(self.additional_message)
        
        self.setLayout(self.layout)
        
        # Load initial data
        self.load_data()
    
    
    def load_data(self):
        """Loads fresh data from the database and updates the UI."""
        all_vehicle_data = self.db_obj.get_all_vehicle()
        total_vehicles = len(all_vehicle_data)
        
        # Update Summary Label
        self.total_vehicle_label.setText(f"🚗 **Total Vehicles: {total_vehicles}**")
        
        # Update Table Data
        self.table.setRowCount(len(all_vehicle_data))
        for row, vehicle in enumerate(all_vehicle_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(vehicle["category"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(vehicle["ba_no_input"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(vehicle["make_type_input"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(vehicle["overhaul_remarks_input"])))
        
        # Adjust table size
        self.table.resizeRowsToContents()
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
