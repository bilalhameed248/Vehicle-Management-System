from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from database import VMS_DB
from templates.vehicle_report import VehicleReport
from templates.update_vehicle import UpdateVehicle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from controllers.load_assets import *

class MultiLevelHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super(MultiLevelHeaderView, self).__init__(orientation, parent)
        self.group_headers = []  # List of tuples: (start_index, span, label)
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setSectionsClickable(False)
        # Define colors for group (main) header and sub header.
        self.groupBgColor = QColor("#007BFF")   # Group header background color.

        self.groupColors = {
            "Basic Details": QColor("#FF5733"),  # Red-Orange
            "Oil Filter": QColor("#33A1FF"),     # Blue
            "Fuel Filter": QColor("#28B463"),    # Green
            "Air Filter": QColor("#F1C40F"),     # Yellow
            "Transmission Filter": QColor("#8E44AD"),  # Purple
            "Differential Oil": QColor("#E67E22"),  # Orange
            "Battery Info": QColor("#2C3E50"),  # Dark Blue
            "Flushing Info": QColor("#D35400"),  # Dark Orange
            "Greasing Info": QColor("#C0392B"),  # Dark Red
            "General Maint": QColor("#16A085"),  # Teal
            "Overall": QColor("#7F8C8D")         # Gray
        }

        self.groupTextColor = QColor("white")    # Group header text color.
        self.subBgColor = QColor("#007BFF")        # Sub header background color.
        self.subTextColor = QColor("white")        # Sub header text color.

        # Font for main headers (larger & bold)
        self.mainHeaderFont = QFont("Segoe UI", 14, QFont.Bold)

    def setGroupHeaders(self, group_headers):
        """Set group headers as list of tuples: (start_index, span, label)."""
        self.group_headers = group_headers
        self.update()

    def sizeHint(self):
        original = super(MultiLevelHeaderView, self).sizeHint()
        # Double the height to allow for two rows (group header + sub header).
        return QSize(original.width(), original.height() * 2)

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        total_height = self.height()
        half = total_height // 2
        sub_margin = 0  # Top margin for sub header text.

        # --- Draw Group (Main) Headers in the Upper Half ---
        painter.setFont(self.mainHeaderFont)
        for start, span, label in self.group_headers:
            # Calculate the starting x position and total width (taking scrolling into account).
            group_x = self.sectionViewportPosition(start)
            group_width = sum(self.sectionSize(i) for i in range(start, start + span))
            group_rect = QRect(group_x, 0, group_width, half)
            visible_group_rect = group_rect.intersected(self.viewport().rect())
            bg_color = self.groupColors.get(label, QColor("#007BFF"))
            painter.fillRect(visible_group_rect, bg_color)
            painter.setPen(self.groupTextColor)
            painter.drawRect(visible_group_rect)
            painter.drawText(visible_group_rect, Qt.AlignCenter, label)

        # --- Draw Sub Headers in the Lower Half ---
        painter.setFont(QFont("Segoe UI", 10))
        for i in range(self.count()):
            x = self.sectionViewportPosition(i)
            width = self.sectionSize(i)
            # Sub header rectangle starts at half + sub_margin and spans the rest of the header height.
            sub_rect = QRect(x, half + sub_margin, width, total_height - half - sub_margin)
            painter.fillRect(sub_rect, self.subBgColor)
            painter.setPen(self.subTextColor)
            painter.drawRect(sub_rect)
            # Get the text from the header model.
            text = self.model().headerData(i, self.orientation(), Qt.DisplayRole)
            painter.drawText(sub_rect, Qt.AlignCenter, str(text))

class ViewALLVehicles(QWidget):
    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        # print("self.user_id:", self.user_id)
        # print("self.username:", self.username)
        self.main_parent = parent
        # print("VIew All Vehicle: self.main_parent:",self.main_parent, "\n")
        
        self.vr_obj = VehicleReport()
        self.db_obj = VMS_DB() 
        self.columns = []
        self.initUI()

    def initUI(self):
        """Initialize UI and load the data table."""
        self.setup_ui()   # Setup UI elements
        self.populate_table()  # Load data into the table


    def refresh_data(self):
        """Refresh the vehicle table data."""
        self.populate_table()  # Reload data from the database


    def setup_ui(self):
        """Creates the UI layout and table structure."""
        self.setWindowTitle("Maintenance Management")
        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa; font-family: 'Segoe UI', Arial, sans-serif; font-size: 16px; }
            QLabel { font-size: 26px; font-weight: bold; padding: 12px; color: #333; }
            QPushButton { background-color: #007BFF; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #0056b3; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 18px; }
            QTableView { border: 1px solid #ddd; background-color: white; border-radius: 8px; font-size: 18px; }
            QTableWidget {border: 1px solid #ddd; background-color: white; border-radius: 6px; }
            QHeaderView::section { background-color: #007BFF; color: white; font-weight: bold; padding: 8px; }
            QTableWidgetItem { padding: 8px; }
            QLineEdit#searchLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;}
            QScrollBar:horizontal {border: none; background: #f0f0f0; height: 12px; margin: 0px 0px 0px 0px; border-radius: 4px;}
            QScrollBar::handle:horizontal {background: #007BFF; min-width: 20px; border-radius: 4px;}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {background: none; border: none; width: 0px; }
            QScrollBar:vertical {border: none; background: #f0f0f0; width: 8px; margin: 0px 0px 0px 0px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #007BFF; min-height: 20px; border-radius: 4px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; border: none; height: 0px;}
        """)

        # Layout
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_label = QLabel("All Vehicles")
        header_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 12px; border-radius: 4px;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()

        # Search Box
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setObjectName("searchLineEdit")
        self.search_line_edit.setPlaceholderText("Search...")
        self.search_line_edit.setFixedWidth(200)
        self.search_line_edit.textChanged.connect(self.filter_table)
        header_layout.addWidget(self.search_line_edit)
        
        layout.addLayout(header_layout)

        # Table Widget
        self.table_widget = QTableWidget(self)
        self.table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_widget.verticalHeader().setVisible(False)

        # Replace the default horizontal header with our custom header
        header = MultiLevelHeaderView(Qt.Horizontal, self.table_widget)
        self.table_widget.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignCenter)

        # header = self.table_widget.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setStretchLastSection(True)
        # header.setDefaultAlignment(Qt.AlignCenter)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def populate_table(self):
        """Fetches and populates the table with vehicle data."""
        # Mapping from DB keys to header names – not used for ordering now.
        db_to_display = {
            "category": "Category", "ba_no_input": "BA No.", "make_type_input": "Make Type", "engine_no_input": "Engine No.",
            "issue_date_oil_filter": "Issue Date (Oil Filter)", "due_date_oil_filter": "Due Date (Oil Filter)", "current_mileage_oil_filter": "Current Mileage (Oil Filter)", "due_mileage_oil_filter": "Due Mileage (Oil Filter)",
            "issue_date_fuel_filter": "Issue Date (Fuel Filter)", "due_date_fuel_filter": "Due Date (Fuel Filter)", "current_mileage_fuel_filter": "Current Mileage (Fuel Filter)", "due_mileage_fuel_filter": "Due Mileage (Fuel Filter)",
            "issue_date_air_filter": "Issue Date (Air Filter)", "due_date_air_filter": "Due Date (Air Filter)", "current_mileage_air_filter": "Current Mileage (Air Filter)", "due_mileage_air_filter": "Due Mileage (Air Filter)",
            "issue_date_transmission_filter": "Issue Date (Transmission Filter)", "due_date_transmission_filter": "Due Date (Transmission Filter)", "current_mileage_transmission_filter": "Current Mileage (Transmission Filter)", "due_mileage_transmission_filter": "Due Mileage (Transmission Filter)",
            "issue_date_differential_oil": "Issue Date (Differential Oil)", "due_date_differential_oil": "Due Date (Differential Oil)", "current_mileage_differential_oil": "Current Mileage (Differential Oil)", "due_mileage_differential_oil": "Due Mileage (Differential Oil)",
            "battery_issue_date": "Battery Issue Date", "battery_due_date": "Battery Due Date",
            "flusing_issue_date": "Flushing Issue Date", "flusing_due_date": "Flushing Due Date", "fuel_tank_flush": "Fuel Tank Flush", "radiator_flush": "Radiator Flush",
            "greasing_issue_date": "Greasing Issue Date", "greasing_due_date": "Greasing Due Date", "trs_and_suspension": "TRS and Suspension","engine_part": "Engine Part", "steering_lever_Pts": "Steering Lever Pts", 
            "wash": "Wash", "oil_level_check": "Oil Level Check", "lubrication_of_parts": "Lubrication of Parts",
            "air_cleaner": "Air Cleaner", "fuel_filter": "Fuel Filter", "french_chalk": "French Chalk", "tr_adjustment": "TR Adjustment",
            "overhaul_current_milage": "Current Milage (Overhaul)", "overhaul_due_milage": "Due Milage (Overhaul)", "overhaul_remarks_input": "Remarks",
            "created_by": "Created By", "created_at": "Created At"
        }

        # Define your main header grouping in the order you want:
        main_header = {
            'Basic Details': ['Category', 'BA No.', 'Make Type', 'Engine No.'], 
            'Oil Filter' : ["Issue Date (Oil Filter)", "Due Date (Oil Filter)",  "Current Mileage (Oil Filter)", "Due Mileage (Oil Filter)"],
            'Fuel Filter': ["Issue Date (Fuel Filter)", "Due Date (Fuel Filter)", "Current Mileage (Fuel Filter)", "Due Mileage (Fuel Filter)"],
            'Air Filter': ["Issue Date (Air Filter)", "Due Date (Air Filter)", "Current Mileage (Air Filter)", "Due Mileage (Air Filter)"],
            'Transmission Filter': ["Issue Date (Transmission Filter)", "Due Date (Transmission Filter)", "Current Mileage (Transmission Filter)", "Due Mileage (Transmission Filter)"],
            'Differential Oil': ["Issue Date (Differential Oil)", "Due Date (Differential Oil)", "Current Mileage (Differential Oil)", "Due Mileage (Differential Oil)"],
            'Battery Info': ["Battery Issue Date", "Battery Due Date"],
            'Flusing Info': ["Flushing Issue Date", "Flushing Due Date", "Fuel Tank Flush", "Radiator Flush"],
            'Greasing Info': ["Greasing Issue Date", "Greasing Due Date", "TRS and Suspension", "Engine Part", "Steering Lever Pts"],
            'General Maint': ["Wash", "Oil Level Check", "Lubrication of Parts", "Air Cleaner", "Fuel Filter", "French Chalk", "TR Adjustment"],
            'Overall': ["Current Milage (Overhaul)", "Due Milage (Overhaul)", "Remarks", "Created By", "Created At"]
        }

        # Build the flat list of columns based on the main_header order.
        columns = []
        for group, cols in main_header.items():
            columns.extend(cols)
        self.columns = columns.copy()
        # Append the Actions column (not part of any group)
        flat_headers = columns + ["Actions"]

        # Set up the table dimensions.
        self.table_widget.setColumnCount(len(flat_headers))
        self.table_widget.setHorizontalHeaderLabels(flat_headers)

        # Compute group header positions.
        group_headers = []
        current_index = 0
        for group, cols in main_header.items():
            span = len(cols)
            group_headers.append((current_index, span, group))
            current_index += span
        # Set the group headers in the custom header.
        header = self.table_widget.horizontalHeader()
        if isinstance(header, MultiLevelHeaderView):
            header.setGroupHeaders(group_headers)

        # Fetch the data from the database.
        all_vehicle_data = self.db_obj.get_all_vehicle()
        self.data = []
        for row in all_vehicle_data:
            # Build the record in the same order as columns.
            record = {col: row.get(key) for key, col in db_to_display.items() if col in columns}
            record["id"] = row["id"]  # Keep ID for actions
            self.data.append(record)

        self.table_widget.setRowCount(len(self.data))
        # Fill table cells.

        for row_index, row_data in enumerate(self.data):
            for col_index, col_name in enumerate(self.columns):
                cell_value = row_data.get(col_name, "")
                # Format dates
                if cell_value and ("Date" in col_name or "Created At" in col_name):
                    try:
                        # print(f"Before Conversion: {type(cell_value)} {cell_value}")

                        if isinstance(cell_value, datetime):
                            cell_value = cell_value.strftime('%d-%m-%Y')
                        else:
                            # print("Ok here")
                            dt = datetime.strptime(cell_value, '%Y-%m-%d')
                            # cell_value = dt.strftime('%d-%m-%Y') #(in My SQL only)
                            cell_value = dt.date() #(in SQLITE only)

                        row_data[col_name] = cell_value #(in SQLITE only)
                        # print(f"After Conversion: {type(cell_value)} {cell_value}")
                    except Exception:
                        pass
                    
                if col_name == 'Issue Date (Oil Filter)':
                    self.date_rules(cell_value, row_index, col_index, 6 , 20)

                elif col_name == 'Issue Date (Fuel Filter)':
                    self.date_rules(cell_value, row_index, col_index, 12 , 20)

                elif col_name in ['Issue Date (Air Filter)', 'Issue Date (Transmission Filter)', 'Issue Date (Differential Oil)']:
                    self.date_rules(cell_value, row_index, col_index, 18 , 20)

                elif col_name == 'Battery Issue Date':
                    self.date_rules(cell_value, row_index, col_index, 42 , 20)
                
                elif col_name == 'Flushing Issue Date':
                    self.date_rules(cell_value, row_index, col_index, 4 , 20)

                elif col_name == 'Greasing Issue Date':
                    self.date_rules(cell_value, row_index, col_index, 3 , 20)

                else:
                    item = QTableWidgetItem(str(cell_value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_widget.setItem(row_index, col_index, item)

            # Create Action Buttons (edit, delete, report) – unchanged code.
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(4)

            btn_edit = QPushButton("Edit")
            btn_edit.setIcon(QIcon(get_asset_path("assets/icons/edit_2.png")))
            btn_edit.setIconSize(QSize(20, 20))

            btn_delete = QPushButton("Delete")
            btn_delete.setIcon(QIcon(get_asset_path("assets/icons/delete.png")))
            btn_delete.setIconSize(QSize(20, 20))

            btn_report = QPushButton("Report")
            btn_report.setIcon(QIcon(get_asset_path("assets/icons/pdf_view.png")))
            btn_report.setIconSize(QSize(20, 20))

            btn_edit.clicked.connect(lambda checked, row=row_data: self.edit_row(row))
            btn_delete.clicked.connect(lambda checked, row=row_data: self.delete_row(row))
            btn_report.clicked.connect(lambda checked, row=row_data: self.report_row(row))

            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addWidget(btn_report)
            action_layout.addStretch()

            self.table_widget.setCellWidget(row_index, len(flat_headers) - 1, action_widget)

        # Adjust Column Width for the Actions column.
        action_col_index = self.table_widget.columnCount() - 1
        self.table_widget.setColumnWidth(action_col_index, 280)



    def date_rules(self, cell_value, row_index, col_index, no_of_month, no_of_days):
        # print(f"IN Rule: {type(cell_value)}, {cell_value},  {date.today()}")
        difference = relativedelta(date.today(), cell_value)
        months_diff = difference.years * 12 + difference.months
        days_diff = difference.days
        # print(f"{months_diff} : {days_diff}")
        item = QTableWidgetItem(str(cell_value))
        item.setTextAlignment(Qt.AlignCenter)

        if months_diff >= no_of_month:
            item.setBackground(QColor(255, 0, 0)) 
            item.setForeground(QColor(255, 255, 255))
        elif months_diff >= (no_of_month-1) and days_diff >= no_of_days and days_diff <= (no_of_days+10):
            item.setBackground(QColor(255, 255, 0))
            item.setForeground(QColor(0, 0, 0))
        self.table_widget.setItem(row_index, col_index, item)


    def filter_table(self):
        """Filter table rows based on the search box input."""
        filter_text = self.search_line_edit.text().lower()
        for row in range(self.table_widget.rowCount()):
            row_visible = False
            # Check each column (except the Actions column) for a match
            for col in range(len(self.columns)):
                item = self.table_widget.item(row, col)
                if item and filter_text in item.text().lower():
                    row_visible = True
                    break
            self.table_widget.setRowHidden(row, not row_visible)


    def edit_row(self, row):
        # print("edit_row parent:",self.main_parent, "\n\n")
        if hasattr(self.main_parent, "update_vehicle_obj") and self.main_parent.update_vehicle_obj is not None:
            self.main_parent.content_area.removeWidget(self.main_parent.update_vehicle_obj)
            self.main_parent.update_vehicle_obj.deleteLater()
            self.main_parent.update_vehicle_obj = None  # Reset the reference

        # Create new instance and switch view
        self.main_parent.update_vehicle_obj = UpdateVehicle(user_session = self.user_session, data = row, parent = self.main_parent)
        self.main_parent.content_area.addWidget(self.main_parent.update_vehicle_obj)
        self.main_parent.content_area.setCurrentWidget(self.main_parent.update_vehicle_obj)


    def delete_row(self, row):
        vehicle_id = row['id']
        vehicle_ba_no = row['BA No.']
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Delete Vehicle")
        confirm.setWindowIcon(QIcon(get_asset_path("assets/icons/delete.png")))  # Replace with your actual icon path
        confirm.setText(f"Are you sure you want to delete vehicle {vehicle_ba_no}?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = confirm.exec_()
        if result == QMessageBox.Yes:
            is_deleted_result  = self.db_obj.delete_vehicle(vehicle_id)
            if is_deleted_result:
                self.populate_table()  # Refresh table after deletion
            else:
                QMessageBox.warning(self, "Error", "Failed to delete vehicle.")


    def report_row(self, row):
        self.vr_obj.generate_vehicle_pdf_report_updated(row)