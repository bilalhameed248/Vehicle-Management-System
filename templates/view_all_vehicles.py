from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QSize
from database import VMS_DB
from templates.vehicle_report import VehicleReport
import datetime

class ViewALLVehicles(QWidget):
    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        print("self.user_id:", self.user_id)
        print("self.username:", self.username)
        
        self.vr_obj = VehicleReport()
        self.db_obj = VMS_DB()  # Assuming this is where data comes from
        self.initUI()

    def initUI(self):
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

        # Create a layout
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_label = QLabel("All Vehicles")
        header_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 12px; border-radius: 4px;")
        header_layout.addWidget(header_label)
        
        # Add a stretch to push the search box to the far right
        header_layout.addStretch()

        # Create the search box
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setObjectName("searchLineEdit")
        self.search_line_edit.setPlaceholderText("Search...")
        self.search_line_edit.setFixedWidth(200)
        self.search_line_edit.textChanged.connect(self.filter_table)
        header_layout.addWidget(self.search_line_edit)
        
        layout.addLayout(header_layout)

        # Set column headers
        self.columns = [
            'Category', 'BA No.', 'Make Type', 'Engine No.', 
            'Issue Date (Oil Filter)', 'Due Date (Oil Filter)', 'Current Mileage (Oil Filter)', 'Due Mileage (Oil Filter)', 
            'Issue Date (Fuel Filter)', 'Due Date (Fuel Filter)', 'Current Mileage (Fuel Filter)', 'Due Mileage (Fuel Filter)', 
            'Issue Date (Air Filter)', 'Due Date (Air Filter)', 'Current Mileage (Air Filter)', 'Due Mileage (Air Filter)', 
            'Issue Date (Transmission Filter)', 'Due Date (Transmission Filter)', 'Current Mileage (Transmission Filter)', 'Due Mileage (Transmission Filter)', 
            'Issue Date (Differential Oil)', 'Due Date (Differential Oil)', 'Current Mileage (Differential Oil)', 'Due Mileage (Differential Oil)', 
            'Battery Issue Date', 'Battery Due Date', 
            'Flushing Issue Date', 'Flushing Due Date', 'Fuel Tank Flush', 'Radiator Flush', 
            'Greasing Issue Date', 'Greasing Due Date', 
            'TRS and Suspension', 'Engine Part', 'Steering Lever Pts', 'Wash', 'Oil Level Check', 'Lubrication of Parts', 
            'Air Cleaner', 'Fuel Filter', 'French Chalk', 'TR Adjustment', 
            'Current Milage (Overhaul)', 'Due Milage  (Overhaul)', 'Remarks',
            'Created By', 'Created At'
        ]
        # Add an extra column for Actions
        headers = self.columns.copy()
        headers.append("Actions")
        
        # Create the table widget
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_widget.verticalHeader().setVisible(False)

        # Adjust header appearance
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        # Fetch data from the database (or use dummy data)
        # data = self.db_obj.fetch_vehicle_data()
        import json
        with open('./random_data.json', 'r') as file:
            data = json.load(file)
        # data = [
        #     {
        #         'Category': 'Truck', 'BA No.': 'BA123', 'Make Type': 'Volvo', 'Engine No.': 'ENG456',
        #         'Issue Date (Oil Filter)': '2023-01-10', 'Due Date (Oil Filter)': '2023-06-10', 'Current Mileage (Oil Filter)': '5000', 'Due Mileage (Oil Filter)': '15000',
        #         'Issue Date (Fuel Filter)': '2023-02-15', 'Due Date (Fuel Filter)': '2023-07-15', 'Current Mileage (Fuel Filter)': '6000', 'Due Mileage (Fuel Filter)': '16000',
        #         'Issue Date (Air Filter)': '2023-03-20', 'Due Date (Air Filter)': '2023-08-20', 'Current Mileage (Air Filter)': '7000', 'Due Mileage (Air Filter)': '17000',
        #         'Issue Date (Transmission Filter)': '2023-04-25', 'Due Date (Transmission Filter)': '2023-09-25', 'Current Mileage (Transmission Filter)': '8000', 'Due Mileage (Transmission Filter)': '18000',
        #         'Issue Date (Differential Oil)': '2023-05-30', 'Due Date (Differential Oil)': '2023-10-30', 'Current Mileage (Differential Oil)': '9000', 'Due Mileage (Differential Oil)': '19000',
        #         'Battery Issue Date': '2023-06-05', 'Battery Due Date': '2023-11-05',
        #         'Flushing Issue Date': '2023-06-05', 'Flushing Due Date': '2023-11-05', 'Fuel Tank Flush': 'Yes', 'Radiator Flush': 'No', 
        #         'Greasing Issue Date': '2023-07-10', 'Greasing Due Date': '2023-12-10', 'TRS and Suspension': 'Good', 'Engine Part': 'Replaced', 'Steering Lever Pts': 'Aligned', 
        #         'Wash': 'Done', 'Oil Level Check': 'OK', 'Lubrication of Parts': 'Completed', 'Air Cleaner': 'Replaced', 'Fuel Filter': 'Cleaned', 'French Chalk': 'N/A', 'TR Adjustment': 'Adjusted', 
        #         'Current Milage (Overhaul)': '5000', 'Due Milage  (Overhaul)': '7000', 'Remarks': 'Overall progress is good.',
        #         'Created By': 'Admin', 'Created At': '2023-01-01'
        #     },
        #     # You can add more sample data rows here
        # ]
        self.data = data
        self.table_widget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            # Populate data columns
            for col_index, col_name in enumerate(self.columns):
                cell_value = str(row_data.get(col_name, ""))
                item = QTableWidgetItem(cell_value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, col_index, item)
            
            # Create a widget to hold the action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(4)
            
            # Create buttons for Edit, Delete, View, and Report
            btn_edit = QPushButton("Edit")
            btn_edit.setIcon(QIcon("assets/icons/edit_2.png"))
            btn_edit.setIconSize(QSize(20, 20))

            btn_delete = QPushButton("Delete")
            btn_delete.setIcon(QIcon("assets/icons/delete.png"))
            btn_delete.setIconSize(QSize(20, 20))

            btn_report = QPushButton("Report")
            btn_report.setIcon(QIcon("assets/icons/pdf_view.png"))
            btn_report.setIconSize(QSize(20, 20))
            
            # Connect button signals (passing the current row index)
            btn_edit.clicked.connect(lambda checked, r=row_index: self.edit_row(r))
            btn_delete.clicked.connect(lambda checked, r=row_index: self.delete_row(r))
            btn_report.clicked.connect(lambda checked, r=row_index: self.report_row(r))
            
            # Add the buttons to the layout
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addWidget(btn_report)
            action_layout.addStretch()
            
            # Set the widget in the action column
            self.table_widget.setCellWidget(row_index, len(self.columns), action_widget)

        # Set a fixed width for the Action column to ensure buttons are visible
        action_col_index = self.table_widget.columnCount() - 1
        self.table_widget.setColumnWidth(action_col_index, 280)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

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
        # Implement your edit functionality here
        print(f"Editing row: {row}")

    def delete_row(self, row):
        # Implement your delete functionality here
        print(f"Deleting row: {row}")

    def report_row(self, row):
        row_data = {}
        for col_index, col_name in enumerate(self.columns):
            item = self.table_widget.item(row, col_index)
            row_data[col_name] = item.text() if item else ""
        self.vr_obj.generate_vehicle_pdf_report_updated(row_data)
        # filename = f"vehicle_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        # # print(f"filename : {filename} \n {row_data}")
        # self.vr_obj.generate_vehicle_pdf_report(row_data, filename)