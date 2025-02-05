from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from database import VMS_DB

class ViewALLVehicles(QWidget):
    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        print("self.user_id:", self.user_id)
        print("self.username:", self.username)
        
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
                           
            QScrollBar:horizontal {border: none; background: #f0f0f0; height: 12px; margin: 0px 0px 0px 0px; border-radius: 4px;}
            QScrollBar::handle:horizontal {background: #007BFF; min-width: 20px; border-radius: 4px;}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {background: none; border: none; width: 0px; }
            QScrollBar:vertical {border: none; background: #f0f0f0; width: 8px; margin: 0px 0px 0px 0px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #007BFF; min-height: 20px; border-radius: 4px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; border: none; height: 0px;}
        """)

        # Create a layout
        layout = QVBoxLayout()
        header_label = QLabel("All Vehicles")
        layout.addWidget(header_label)

        # Set column headers
        self.columns = [
            'Category', 'BA No.', 'Make Type', 'Engine No.', 'Issue Date (Oil Filter)', 'Due Date (Oil Filter)', 'Current Mileage (Oil Filter)', 
            'Due Mileage (Oil Filter)', 'Issue Date (Fuel Filter)', 'Due Date (Fuel Filter)', 'Current Mileage (Fuel Filter)', 
            'Due Mileage (Fuel Filter)', 'Issue Date (Air Filter)', 'Due Date (Air Filter)', 'Current Mileage (Air Filter)', 
            'Due Mileage (Air Filter)', 'Issue Date (Transmission Filter)', 'Due Date (Transmission Filter)', 'Current Mileage (Transmission Filter)', 
            'Due Mileage (Transmission Filter)', 'Issue Date (Differential Oil)', 'Due Date (Differential Oil)', 'Current Mileage (Differential Oil)', 
            'Due Mileage (Differential Oil)', 'Flushing Issue Date', 'Flushing Due Date', 'Fuel Tank Flush', 'Radiator Flush', 'Greasing Issue Date', 
            'Greasing Due Date', 'TRS and Suspension', 'Engine Part', 'Steering Lever Pts', 'Wash', 'Oil Level Check', 'Lubrication of Parts', 
            'Air Cleaner', 'Fuel Filter', 'French Chalk', 'TR Adjustment', 'Created By', 'Created At'
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
        data = []  # Replace this with actual data
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
            btn_delete = QPushButton("Delete")
            btn_view = QPushButton("View")
            btn_report = QPushButton("Report")
            
            # Connect button signals (passing the current row index)
            btn_edit.clicked.connect(lambda checked, r=row_index: self.edit_row(r))
            btn_delete.clicked.connect(lambda checked, r=row_index: self.delete_row(r))
            btn_view.clicked.connect(lambda checked, r=row_index: self.view_row(r))
            btn_report.clicked.connect(lambda checked, r=row_index: self.report_row(r))
            
            # Add the buttons to the layout
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addWidget(btn_view)
            action_layout.addWidget(btn_report)
            action_layout.addStretch()
            
            # Set the widget in the action column
            self.table_widget.setCellWidget(row_index, len(self.columns), action_widget)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def edit_row(self, row):
        # Implement your edit functionality here
        print(f"Editing row: {row}")

    def delete_row(self, row):
        # Implement your delete functionality here
        print(f"Deleting row: {row}")

    def view_row(self, row):
        # Implement your view functionality here
        print(f"Viewing row: {row}")

    def report_row(self, row):
        # Implement your report functionality here
        print(f"Reporting row: {row}")