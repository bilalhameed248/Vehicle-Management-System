from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox, QComboBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from database import VMS_DB
from templates.vehicle_report import VehicleReport
from templates.update_vehicle import UpdateVehicle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from controllers.load_assets import *
from controllers.report_all_vehicles import Report
from templates.import_vehicles_fe import ImportVehiclesFE
import math

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
            "Overhaul": QColor("#7F8C8D"),         # Gray
            "Status & Creation Details": QColor("#008B8B") # Deep Cyan
        }

        self.groupTextColor = QColor("white")    # Group header text color.
        self.subBgColor = QColor("#007BFF")        # Sub header background color.
        self.subTextColor = QColor("white")        # Sub header text color.

        # Font for main headers (larger & bold)
        self.mainHeaderFont = QFont("Segoe UI", 16, QFont.Bold)
        self.subHeaderFont = QFont("Segoe UI", 14, QFont.Bold)

        self.setFont(self.subHeaderFont)

    def sectionSizeFromContents(self, logicalIndex):
        size = super(MultiLevelHeaderView, self).sectionSizeFromContents(logicalIndex)
        padding = 60
        size.setWidth(size.width() + padding)
        return size

    def setGroupHeaders(self, group_headers):
        """Set group headers as list of tuples: (start_index, span, label)."""
        self.group_headers = group_headers
        self.update()


    def sizeHint(self):
        original = super(MultiLevelHeaderView, self).sizeHint()
        return QSize(original.width(), int(original.height() * 2.5))


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
        painter.setFont(self.subHeaderFont)
        for i in range(self.count()):
            x = self.sectionViewportPosition(i)
            width = self.sectionSize(i)
            # Sub header rectangle starts at half + sub_margin and spans the rest of the header height.
            sub_rect = QRect(x, half + sub_margin, width, total_height - half - sub_margin)
            painter.fillRect(sub_rect, self.subBgColor)
            painter.setPen(self.subTextColor)
            painter.drawRect(sub_rect)
            # Get the text from the header model.
            text_rect = sub_rect.adjusted(8, 0, -8, 0)
            text = self.model().headerData(i, self.orientation(), Qt.DisplayRole)
            painter.drawText(text_rect, Qt.AlignCenter, str(text).split('(')[0].strip())

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

        self.current_page = 0
        self.page_size = 20
        
        self.vr_obj = VehicleReport()
        self.db_obj = VMS_DB() 
        self.columns = []

        # Mapping from DB keys to header names – not used for ordering now.
        self.db_to_display = {
            "category": "Category", "ba_no_input": "BA No.", "make_type_input": "Make Type", "engine_no_input": "Engine No.",
            "issue_date_oil_filter": "Issue Date (Oil Filter)", "due_date_oil_filter": "Due Date (Oil Filter)", "current_mileage_oil_filter": "Current Mileage (Oil Filter)", "due_mileage_oil_filter": "Due Mileage (Oil Filter)",
            "issue_date_fuel_filter": "Issue Date (Fuel Filter)", "due_date_fuel_filter": "Due Date (Fuel Filter)", "current_mileage_fuel_filter": "Current Mileage (Fuel Filter)", "due_mileage_fuel_filter": "Due Mileage (Fuel Filter)",
            "issue_date_air_filter": "Issue Date (Air Filter)", "due_date_air_filter": "Due Date (Air Filter)", "current_mileage_air_filter": "Current Mileage (Air Filter)", "due_mileage_air_filter": "Due Mileage (Air Filter)",
            "issue_date_transmission_filter": "Issue Date (Transmission Filter)", "due_date_transmission_filter": "Due Date (Transmission Filter)", "current_mileage_transmission_filter": "Current Mileage (Transmission Filter)", "due_mileage_transmission_filter": "Due Mileage (Transmission Filter)",
            "issue_date_differential_oil": "Issue Date (Differential Oil)", "due_date_differential_oil": "Due Date (Differential Oil)", "current_mileage_differential_oil": "Current Mileage (Differential Oil)", "due_mileage_differential_oil": "Due Mileage (Differential Oil)",
            "battery_issue_date": "Issue Date (Battery)", "battery_due_date": "Due Date (Battery)",
            "flusing_issue_date": "Issue Date (Flushing)", "flusing_due_date": "Due Date (Flushing)", "fuel_tank_flush": "Fuel Tank Flush", "radiator_flush": "Radiator Flush",
            "greasing_issue_date": "Issue Date (Greasing)", "greasing_due_date": "Due Date (Greasing)", "trs_and_suspension": "TRS and Suspension","engine_part": "Engine Part", "steering_lever_Pts": "Steering Lever Pts", 
            "wash": "Wash", "oil_level_check": "Oil Level Check", "lubrication_of_parts": "Lubrication of Parts",
            "air_cleaner": "Air Cleaner", "fuel_filter": "Fuel Filter", "french_chalk": "French Chalk", "tr_adjustment": "TR Adjustment",
            "overhaul_current_milage": "Current Milage (Overhaul)", "overhaul_due_milage": "Due Milage (Overhaul)", 
            "overhaul_remarks_input": "Status",
            "created_by": "Created By", "created_at": "Created At"
        }

        # Define your main header grouping in the order you want:
        self.main_header = {
            'Basic Details': ['Category', 'BA No.', 'Make Type', 'Engine No.'], 
            'Oil Filter' : ["Issue Date (Oil Filter)", "Due Date (Oil Filter)",  "Current Mileage (Oil Filter)", "Due Mileage (Oil Filter)"],
            'Fuel Filter': ["Issue Date (Fuel Filter)", "Due Date (Fuel Filter)", "Current Mileage (Fuel Filter)", "Due Mileage (Fuel Filter)"],
            'Air Filter': ["Issue Date (Air Filter)", "Due Date (Air Filter)", "Current Mileage (Air Filter)", "Due Mileage (Air Filter)"],
            'Transmission Filter': ["Issue Date (Transmission Filter)", "Due Date (Transmission Filter)", "Current Mileage (Transmission Filter)", "Due Mileage (Transmission Filter)"],
            'Differential Oil': ["Issue Date (Differential Oil)", "Due Date (Differential Oil)", "Current Mileage (Differential Oil)", "Due Mileage (Differential Oil)"],
            'Battery Info': ["Issue Date (Battery)", "Due Date (Battery)"],
            'Flushing Info': ["Issue Date (Flushing)", "Due Date (Flushing)", "Fuel Tank Flush", "Radiator Flush"],
            'Greasing Info': ["Issue Date (Greasing)", "Due Date (Greasing)", "TRS and Suspension", "Engine Part", "Steering Lever Pts"],
            'General Maint': ["Wash", "Oil Level Check", "Lubrication of Parts", "Air Cleaner", "Fuel Filter", "French Chalk", "TR Adjustment"],
            'Overhaul': ["Current Milage (Overhaul)", "Due Milage (Overhaul)"],
            'Status & Creation Details': ["Status", "Created By", "Created At"]
        }
        self.rpt_obj = Report(db_to_display=self.db_to_display, main_heading=self.main_header)
        self.tbL_data_font = QFont("Arial", 12)
        self.initUI()


    def initUI(self):
        """Initialize UI and load the data table."""
        self.setup_ui()   # Setup UI elements
        self.header_setup()
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
            QTableWidgetItem { padding: 12px; }
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

        # Export Button
        export_button = QPushButton(" Export")
        export_button.setFixedSize(100, 45)  # Set button size
        export_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #218838; }
        """)
        export_button.setIcon(QIcon(get_asset_path("assets/icons/xlsx.png")))
        export_button.setIconSize(QSize(20, 20))
        export_button.clicked.connect(self.report_all_vehicle)
        header_layout.addWidget(export_button)

        #Import Button
        import_button = QPushButton(" Import")
        import_button.setFixedSize(100, 45)  # Set button size
        import_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #218838; }
        """)
        import_button.setIcon(QIcon(get_asset_path("assets/icons/import_excel.png")))
        import_button.setIconSize(QSize(20, 20))
        import_button.clicked.connect(self.show_import_vehicle_dialog)
        header_layout.addWidget(import_button)

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
        self.table_widget.setAlternatingRowColors(True)

        # Replace the default horizontal header with our custom header
        header = MultiLevelHeaderView(Qt.Horizontal, self.table_widget)
        self.table_widget.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignCenter)

        layout.addWidget(self.table_widget)

        # --- Pagination Controls ---
        pagination_layout = QHBoxLayout()
        # Label to show "Showing x to y of z entries"
        self.entries_label = QLabel("Showing 0 to 0 of 0 entries")
        self.entries_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 12px; border-radius: 4px;")
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
        
        layout.addLayout(pagination_layout)

        self.setLayout(layout)


    def header_setup(self):
        """Fetches and populates the table with vehicle data."""
        # Build the flat list of columns based on the main_header order.
        columns, group_headers = [], []
        current_index = 0
        for group, cols in self.main_header.items():
            span = len(cols)
            columns.extend(cols)
            group_headers.append((current_index, span, group))
            current_index += span
        self.columns = columns.copy()
        # Append the Actions column (not part of any group)
        self.flat_headers = columns + ["Actions"]

        # Set up the table dimensions.
        self.table_widget.setColumnCount(len(self.flat_headers))
        self.table_widget.setHorizontalHeaderLabels(self.flat_headers)

        # Set the group headers in the custom header.
        header = self.table_widget.horizontalHeader()
        if isinstance(header, MultiLevelHeaderView):
            header.setGroupHeaders(group_headers)


    def populate_table(self):
        # Fetch the data from the database.
        all_vehicle_data = self.db_obj.get_all_vehicle(self.current_page, self.page_size)
        self.data = []
        for row in all_vehicle_data:
            # Build the record in the same order as columns.
            record = {display_col: row.get(db_col) for db_col, display_col in self.db_to_display.items() if display_col in self.columns}
            record["id"] = row["id"]  # Keep ID for actions
            self.data.append(record)

        self.table_widget.setRowCount(len(self.data))
        
        # Fill table cells.        
        for row_index, row_data in enumerate(self.data):
            for col_index, col_name in enumerate(self.columns):
                cell_value = row_data.get(col_name, "")
                if cell_value and ("Date" in col_name or "Created At" in col_name):
                    try:
                        if isinstance(cell_value, datetime):
                            cell_value = cell_value.strftime('%d-%m-%Y')
                        else:
                            dt = datetime.strptime(cell_value, '%Y-%m-%d')
                            # cell_value = dt.strftime('%d-%m-%Y') #(in My SQL only)
                            cell_value = dt.date() #(in SQLITE only)
                        row_data[col_name] = cell_value #(in SQLITE only)
                    except Exception:
                        pass

                issue_due_mapping = {
                    'Due Date (Oil Filter)': 6,
                    'Due Date (Fuel Filter)': 12,
                    'Due Date (Air Filter)': 18,
                    'Due Date (Transmission Filter)': 18,
                    'Due Date (Differential Oil)': 18,
                    'Due Date (Battery)': 42,
                    'Due Date (Flushing)': 4,
                    'Due Date (Greasing)': 3,
                }

                item = QTableWidgetItem(str(cell_value))
                item.setFont(self.tbL_data_font)
                item.setTextAlignment(Qt.AlignCenter)

                if col_name in issue_due_mapping:
                    previous_cell_value = row_data.get(self.columns[col_index-1], "")
                    self.date_rules(previous_cell_value, row_index, col_index, item, issue_due_mapping[col_name], 20)
                else:
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

            self.table_widget.setCellWidget(row_index, len(self.flat_headers) - 1, action_widget)

        # Adjust Column Width for the Actions column.
        action_col_index = self.table_widget.columnCount() - 1
        self.table_widget.setColumnWidth(action_col_index, 280)

        # Update pagination button state based on returned data.
        self.update_pagination_buttons()


    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()


    def next_page(self):
        total_count = self.db_obj.get_vehicle_count()
        total_pages = math.ceil(total_count['total'] / self.page_size)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.populate_table()


    def go_to_page(self, page):
        self.current_page = page
        self.populate_table()


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


    def date_rules(self, previous_cell_value, row_index, col_index, item, no_of_month, no_of_days):
        difference = relativedelta(date.today(), previous_cell_value)
        months_diff = difference.years * 12 + difference.months
        days_diff = difference.days

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


    def report_all_vehicle(self):
        is_generated = self.rpt_obj.generate_report()
        if is_generated:
            message = "Report saved successfully to Downloads"
        else:
            message = "Error while generating Report."
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Report Generated")
        msg.exec_()


    def show_import_vehicle_dialog(self):
        dialog = ImportVehiclesFE(user_session=self.user_session, db_to_display = self.db_to_display)
        if dialog.exec_():  # If user clicks Save
            self.populate_table()  # Refresh user table