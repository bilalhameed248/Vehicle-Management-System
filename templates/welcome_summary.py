from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                              QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy)
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
        self.layout.setContentsMargins(20, 10, 20, 10)
        
        # Welcome Message
        self.welcome_message = QLabel("Welcome to the Vehicle & Weapons Maintenance Record Portal", self)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setWordWrap(True)
        self.welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        self.welcome_message.setStyleSheet("color: #2C3E50; padding-bottom: 10px;")
        self.layout.addWidget(self.welcome_message, alignment=Qt.AlignTop)

        #*********************************************************************************************************************
        
        # Vehicle Summary
        veh_summary_layout = QVBoxLayout()
        self.vehicle_summary_label = QLabel("Vehicle Summary:", self)
        self.vehicle_summary_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.vehicle_summary_label.setStyleSheet("color: #27AE60; padding-bottom: 5px;")
        veh_summary_layout.addWidget(self.vehicle_summary_label)
        
        # Total Vehicle Summary Label
        self.total_vehicle_label = QLabel("", self)
        self.total_vehicle_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_vehicle_label.setStyleSheet("color: #2C3E50; padding-bottom: 10px;")
        veh_summary_layout.addWidget(self.total_vehicle_label)

        self.layout.addLayout(veh_summary_layout)

        # Table Setup
        self.vehicle_table = self.create_table()
        self.layout.addWidget(self.vehicle_table, alignment=Qt.AlignLeft) 

        #*********************************************************************************************************************

        # Weapon Summary Section
        wep_summary_layout = QVBoxLayout()
        self.weapon_summary_label = QLabel("Weapon Summary:", self)
        self.weapon_summary_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.weapon_summary_label.setStyleSheet("color: #27AE60; padding-bottom: 5px;")
        wep_summary_layout.addWidget(self.weapon_summary_label)

        # Total Weapon Summary Label
        self.total_weapon_label = QLabel("", self)
        self.total_weapon_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_weapon_label.setStyleSheet("color: #2C3E50; padding-bottom: 10px;")
        wep_summary_layout.addWidget(self.total_weapon_label)

        self.layout.addLayout(wep_summary_layout)
        
        self.weapon_table = self.create_table(dummy_data=True)
        self.layout.addWidget(self.weapon_table, alignment=Qt.AlignLeft)

        #*********************************************************************************************************************

        # Additional Information Label
        self.additional_message = QLabel(
            "This portal is designed to streamline and enhance the management of vehicle & weapons "
            "maintenance records of 44 AK Pak ARMY", self)
        self.additional_message.setAlignment(Qt.AlignCenter)
        self.additional_message.setWordWrap(True)
        self.additional_message.setFont(QFont("Arial", 14))
        self.additional_message.setStyleSheet("color: #7F8C8D; padding-top: 20px;")
        self.layout.addWidget(self.additional_message, alignment=Qt.AlignBottom)
        
        self.setLayout(self.layout)
        
        # Load initial data
        self.load_data()
    
    def create_table(self, dummy_data=False):
        """Creates a styled table widget."""
        table = QTableWidget(self)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Category", "BA No.", "Make & Type", "Status"])
        table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        table.setStyleSheet("""
            QTableWidget { border: 1px solid #ddd; background-color: white; border-radius: 6px; font-size: 16px; }
            QHeaderView::section { background-color: #007BFF; color: white; font-weight: bold; padding: 8px; }
            QTableWidget::item { padding: 6px; }
        """)
        table.setAlternatingRowColors(True)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setFixedWidth(int(self.width() * 1))
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        if dummy_data:
            table.setRowCount(5)
            for row in range(5):
                for col in range(4):
                    table.setItem(row, col, QTableWidgetItem(f"Dummy {row}-{col}"))
        
        return table
    
    def load_data(self):
        """Loads fresh data from the database and updates the UI."""
        all_vehicle_data = self.db_obj.get_all_vehicle()
        total_vehicles = len(all_vehicle_data)
        
        # Update Summary Label
        self.total_vehicle_label.setText(f"🚗 Total Vehicles: {total_vehicles}")
        self.total_weapon_label.setText(f"Total Weapons: {total_vehicles}")
        
        # Update Table Data
        # display_rows = min(5, total_vehicles)
        display_rows = total_vehicles
        self.vehicle_table.setRowCount(display_rows)
        for row, vehicle in enumerate(all_vehicle_data[:display_rows]):
            self.vehicle_table.setItem(row, 0, QTableWidgetItem(str(vehicle["category"])))
            self.vehicle_table.setItem(row, 1, QTableWidgetItem(str(vehicle["ba_no_input"])))
            self.vehicle_table.setItem(row, 2, QTableWidgetItem(str(vehicle["make_type_input"])))
            self.vehicle_table.setItem(row, 3, QTableWidgetItem(str(vehicle["overhaul_remarks_input"])))

        # if total_vehicles > 5:
        #     self.vehicle_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # else:
        #     self.vehicle_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Adjust table size
        self.vehicle_table.resizeRowsToContents()
        self.vehicle_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
