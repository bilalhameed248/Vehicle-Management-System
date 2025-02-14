from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QSplitter, 
                              QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QLineEdit)
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

        self.summary_columns = ["Category", "BA No.", "Make & Type", "Status"]

        self.setStyleSheet("""
            QTableWidget { padding: 20px; border: 1px solid #ddd; background-color: white; border-radius: 6px; font-size: 16px; }
            QHeaderView::section { background-color: #007BFF; color: white; font-weight: bold; padding: 8px; }
            QTableWidget::item { padding: 6px; }
            QSplitter { border: 2px dashed #3498DB; }
            QSplitter::handle { background: none; border: 2px dashed #3498DB; }  
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 18px; background-color: white; color: black; }
            QLineEdit#searchLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;  background-color: white; color: black;}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)

        #*********************************************************************************************************************
        
        # Welcome Message
        self.welcome_message = QLabel("Welcome to the Vehicle & Weapons Maintenance Record Portal", self)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setWordWrap(True)
        self.welcome_message.setFont(QFont("Arial", 24, QFont.Bold))
        self.welcome_message.setStyleSheet("color: #2C3E50; padding: 20px;")
        main_layout.addWidget(self.welcome_message, alignment=Qt.AlignTop)

        #*********************************************************************************************************************
        
        # Splitter for Summary Section
        splitter = QSplitter(Qt.Horizontal)
        
        # Left Side - Vehicle Summary
        veh_container = QWidget()
        veh_summary_layout = QVBoxLayout()
        
        self.vehicle_summary_label = QLabel("Vehicle Summary:", self)
        self.vehicle_summary_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.vehicle_summary_label.setStyleSheet("color: #27AE60; padding-bottom: 5px;")
        veh_summary_layout.addWidget(self.vehicle_summary_label)

        search_layout = QHBoxLayout()

        self.total_vehicle_label = QLabel("", self)
        self.total_vehicle_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_vehicle_label.setStyleSheet("color: #2C3E50; padding-bottom: 10px;")
        search_layout.addWidget(self.total_vehicle_label)

        self.search_box_vhl = QLineEdit(self)
        self.search_box_vhl.setPlaceholderText("Search...")
        self.search_box_vhl.setFixedWidth(200)  # Adjust width as needed
        self.search_box_vhl.textChanged.connect(self.filter_wep_table)
        search_layout.addWidget(self.search_box_vhl)

        veh_summary_layout.addLayout(search_layout)
        
        self.vehicle_table = self.create_table()
        veh_summary_layout.addWidget(self.vehicle_table)

        veh_container.setLayout(veh_summary_layout)
        splitter.addWidget(veh_container)

        #*********************************************************************************************************************
        
        # Right Side - Weapon Summary
        wep_container = QWidget()
        wep_summary_layout = QVBoxLayout()
        
        self.weapon_summary_label = QLabel("Weapon Summary:", self)
        self.weapon_summary_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.weapon_summary_label.setStyleSheet("color: #27AE60; padding-bottom: 5px;")
        wep_summary_layout.addWidget(self.weapon_summary_label)
        
        search_layout_wpn = QHBoxLayout()

        self.total_weapon_label = QLabel("", self)
        self.total_weapon_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_weapon_label.setStyleSheet("color: #2C3E50; padding-bottom: 10px;")
        search_layout_wpn.addWidget(self.total_weapon_label)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setFixedWidth(200)  # Adjust width as needed
        search_layout_wpn.addWidget(self.search_box)

        wep_summary_layout.addLayout(search_layout_wpn)
        
        self.weapon_table = self.create_table(dummy_data=True)
        wep_summary_layout.addWidget(self.weapon_table, Qt.AlignRight)
        
        wep_container.setLayout(wep_summary_layout)
        splitter.addWidget(wep_container)

        #*********************************************************************************************************************
        
        main_layout.addWidget(splitter)
        
        # Additional Information Label
        self.additional_message = QLabel(
            "This portal is designed to streamline and enhance the management of vehicle & weapons "
            "maintenance records of 44 AK Pak ARMY", self)
        self.additional_message.setAlignment(Qt.AlignCenter)
        self.additional_message.setWordWrap(True)
        self.additional_message.setFont(QFont("Arial", 14))
        self.additional_message.setStyleSheet("color: #7F8C8D; padding: 10px;")
        main_layout.addWidget(self.additional_message, alignment=Qt.AlignBottom)
        
        self.setLayout(main_layout)
        
        # Load initial data
        self.load_data()
    
    def create_table(self, dummy_data=False):
        """Creates a styled table widget."""
        table = QTableWidget(self)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(self.summary_columns)
        table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        table.setAlternatingRowColors(True)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table.setFixedWidth(int(self.width() * 1))
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
        self.total_weapon_label.setText(f"🔫 Total Weapons: {total_vehicles}")
        
        # Update Table Data
        # display_rows = min(5, total_vehicles)
        display_rows = total_vehicles
        self.vehicle_table.setRowCount(display_rows)
        for row, vehicle in enumerate(all_vehicle_data[:display_rows]):
            self.vehicle_table.setItem(row, 0, QTableWidgetItem(str(vehicle["category"])))
            self.vehicle_table.setItem(row, 1, QTableWidgetItem(str(vehicle["ba_no_input"])))
            self.vehicle_table.setItem(row, 2, QTableWidgetItem(str(vehicle["make_type_input"])))
            self.vehicle_table.setItem(row, 3, QTableWidgetItem(str(vehicle["overhaul_remarks_input"])))
        
        # Adjust table size
        self.vehicle_table.resizeRowsToContents()
        self.vehicle_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

    def filter_wep_table(self):
        """Filter table rows based on the search box input."""
        filter_text = self.search_box_vhl.text().lower()
        for row in range(self.vehicle_table.rowCount()):
            row_visible = False
            for col in range(len(self.summary_columns)):
                item = self.vehicle_table.item(row, col)
                if item and filter_text in item.text().lower():
                    row_visible = True
                    break
            self.vehicle_table.setRowHidden(row, not row_visible)
