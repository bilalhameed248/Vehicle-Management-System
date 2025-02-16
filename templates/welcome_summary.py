from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QSplitter, QPushButton,
                              QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QLineEdit)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from database import VMS_DB
from controllers.load_assets import *
import math

class WelcomeSummary(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_obj = VMS_DB()
        self.current_page = 0
        self.page_size = 10
        self.init_ui()

    def init_ui(self):
        """Initializes UI components."""

        self.summary_columns = ["Category", "BA No.", "Make & Type", "Status"]

        self.setStyleSheet("""
            QPushButton { background-color: #007BFF; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #0056b3; }
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
        self.welcome_message = QLabel("Welcome to ArmourTrack – Your Ultimate Vehicle & Weapon Management Portal", self)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setWordWrap(True)
        self.welcome_message.setFont(QFont("Arial", 20, QFont.Bold))
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
        self.total_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px;")
        search_layout.addWidget(self.total_vehicle_label)

        self.search_box_vhl = QLineEdit(self)
        self.search_box_vhl.setPlaceholderText("Search...")
        self.search_box_vhl.setFixedWidth(200)  # Adjust width as needed
        self.search_box_vhl.textChanged.connect(self.filter_wep_table)
        search_layout.addWidget(self.search_box_vhl)

        veh_summary_layout.addLayout(search_layout) 

        #************************************************************

        detail_summary = QHBoxLayout()

        self.total_a_vehicle_label = QLabel("", self)
        self.total_a_vehicle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_a_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px;")
        detail_summary.addWidget(self.total_a_vehicle_label)

        self.total_b_vehicle_label = QLabel("", self)
        self.total_b_vehicle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_b_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px;")
        detail_summary.addWidget(self.total_b_vehicle_label)

        self.total_fit_vehicle_label = QLabel("", self)
        self.total_fit_vehicle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_fit_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px;")
        detail_summary.addWidget(self.total_fit_vehicle_label)

        self.total_unfit_vehicle_label = QLabel("", self)
        self.total_unfit_vehicle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_unfit_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px;")
        detail_summary.addWidget(self.total_unfit_vehicle_label)

        self.total_a_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px; border: 2px solid white; padding: 5px;")
        self.total_b_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px; border: 2px solid white; padding: 5px;")
        self.total_fit_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px; border: 2px solid white; padding: 5px;")
        self.total_unfit_vehicle_label.setStyleSheet("color: white; padding-bottom: 10px; border: 2px solid white; padding: 5px;")

        veh_summary_layout.addLayout(detail_summary) 

        #************************************************************
        
        self.vehicle_table = self.create_table()
        veh_summary_layout.addWidget(self.vehicle_table)

        #************************************************************
        # --- Pagination Controls ---
        pagination_layout = QHBoxLayout()
        # Label to show "Showing x to y of z entries"
        self.entries_label = QLabel("Showing 0 to 0 of 0 entries")
        self.entries_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; padding: 12px; border-radius: 4px;")
        pagination_layout.addWidget(self.entries_label)
        
        pagination_layout.addStretch()
        
        # Container layout for page number buttons
        self.page_buttons_layout = QHBoxLayout()
        pagination_layout.addLayout(self.page_buttons_layout)
        
        pagination_layout.addStretch()
        
        # Previous and Next buttons
        self.btn_prev = QPushButton(" Prev")
        self.btn_prev.setIcon(QIcon(get_asset_path("assets/icons/btn_prev.png")))
        self.btn_prev.setIconSize(QSize(30, 30))
        self.btn_prev.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton(" Next")
        self.btn_next.setIcon(QIcon(get_asset_path("assets/icons/btn_next.png")))
        self.btn_next.setIconSize(QSize(30, 30))
        self.btn_next.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.btn_next)
        
        veh_summary_layout.addLayout(pagination_layout)
        #************************************************************

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
            "ArmourTrack ensures efficient and organized management of vehicle & weapon maintenance records for 44 AK Pak Army.", self)
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
        all_vehicle_data = self.db_obj.get_vehicle_summary(self.current_page, self.page_size)
        vehicles_summary_count = self.db_obj.get_vehicle_count()
        # Update Summary Label
        self.total_vehicle_label.setText(f"🚗 Total Vehicles: {vehicles_summary_count['total']}")
        self.total_a_vehicle_label.setText(f"A Vehicles: {vehicles_summary_count['category_A']}")
        self.total_b_vehicle_label.setText(f"B Vehicles: {vehicles_summary_count['category_B']}")
        self.total_fit_vehicle_label.setText(f"Fit: {vehicles_summary_count['fit_vehicle']}")
        self.total_unfit_vehicle_label.setText(f"Unfit: {vehicles_summary_count['unfit_vehicle']}")

        self.total_weapon_label.setText(f"🔫 Total Weapons: {vehicles_summary_count['total']}")
        
        # Update Table Data
        self.vehicle_table.setRowCount(len(all_vehicle_data))
        for row, vehicle in enumerate(all_vehicle_data):
            self.vehicle_table.setItem(row, 0, QTableWidgetItem(str(vehicle["category"])))
            self.vehicle_table.setItem(row, 1, QTableWidgetItem(str(vehicle["ba_no_input"])))
            self.vehicle_table.setItem(row, 2, QTableWidgetItem(str(vehicle["make_type_input"])))
            self.vehicle_table.setItem(row, 3, QTableWidgetItem(str(vehicle["overhaul_remarks_input"])))
        
        # Adjust table size
        self.vehicle_table.resizeRowsToContents()
        self.vehicle_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        self.update_pagination_buttons()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_data()


    def next_page(self):
        total_count = self.db_obj.get_vehicle_count()
        total_pages = math.ceil(total_count['total'] / self.page_size)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_data()


    def go_to_page(self, page):
        self.current_page = page
        self.load_data()


    def update_pagination_buttons(self):
        # Get the total count from the database.
        total_count = self.db_obj.get_vehicle_count()
        total_pages = math.ceil(total_count['total'] / self.page_size) if self.page_size else 1
        
        # Calculate the current entries range.
        start_entry = self.current_page * self.page_size + 1
        end_entry = min((self.current_page + 1) * self.page_size, total_count['total'])
        
        # Update the entries label.
        self.entries_label.setText(f"Showing {start_entry} to {end_entry} of {total_count['total']} entries")
        
        # Clear existing page number buttons.
        for i in reversed(range(self.page_buttons_layout.count())):
            widget = self.page_buttons_layout.itemAt(i).widget()
            if widget:
                self.page_buttons_layout.removeWidget(widget)
                widget.deleteLater()
        
        # Create page number buttons.
        for page in range(total_pages):
            btn = QPushButton(str(page + 1))
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #ccc; padding: 5px 10px; border-radius: 5px; }
                QPushButton:hover { background-color: #e0e0e0; }
                QPushButton:checked { background-color: #007bff; color: white;font-weight: bold; }
            """)
            # Mark the current page button as checked.
            if page == self.current_page:
                btn.setChecked(True)
            # When a button is clicked, jump to that page.
            btn.clicked.connect(lambda checked, p=page: self.go_to_page(p))
            self.page_buttons_layout.addWidget(btn)
        
        # Enable/disable previous/next buttons.
        self.btn_prev.setEnabled(self.current_page > 0)
        self.btn_next.setEnabled(self.current_page < total_pages - 1)



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
