from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QLabel, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from database import VMS_DB
from templates.vehicle_report import VehicleReport
from templates.update_a_vehicle_fit import UpdateAVehicleFit
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from controllers.load_assets import *
from controllers.report_all_a_vehicles_fit import Report
from templates.import_a_vehicles_fit_fe import ImportAVehiclesFitFE
from templates.a_vehicle_report_view import AVehicleReportView
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
            "Cooling Sys": QColor("#33A1FF"),     # Blue
            "Hyd Ramp": QColor("#28B463"),    # Green
            "Lub Sys": QColor("#F1C40F"),     # Yellow
            "Tr Sys": QColor("#8E44AD"),  # Purple
            "Bty & Assys": QColor("#E67E22"),  # Orange
            "Boggy Wh": QColor("#2C3E50"),  # Dark Blue
            "Brk Sys": QColor("#D35400"),  # Dark Orange
            "Elec Sys": QColor("#C0392B"),  # Dark Red
            "Air Intake Sys": QColor("#16A085"),  # Teal
            "Tx Sys": QColor("#7F8C8D"),         # Gray
            "Steering Con": QColor("#A569BD"),
            "Fuel Sys": QColor("#5D6D7E"), 
            "Creation Details": QColor("#F1C40F")
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
            painter.drawText(text_rect, Qt.AlignCenter, str(text))

class ViewALLAVehiclesFit(QWidget):

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
            "ba_no_input": "BA NO","make_input": "Make","type_input": "Type","CI_input": "CI", "In_Svc_input": "In Svc",
            "Cooling_Fins": "Fins","Cooling_Rad_Paint": "Rad Paint", "Cooling_Coolant": "Coolant", "Cooling_Leakage": "CS Leakage", "Cooling_Rad_Cap": "Rad Cap", "Cooling_Fan_Belt": "Fan Belt",
            "HydRamp_Hyd_Oil_Lvl": "Hyd Oil Lvl", "HydRamp_TGS_Oil_Lvl": "TGS Oil Lvl", "HydRamp_Tx_Oil": "Tx Oil", "HydRamp_Tx_Filter": "Tx Filter", "HydRamp_Fan_Mech_Oil": "Fan Mech Oil",
            "LubSys_Eng_Oil": "Eng Oil","LubSys_EO_Cond": "EO Cond","LubSys_Oil_Sump": "Oil Sump", "LubSys_Leakage": "LS Leakage", "LubSys_Oil_Grade": "Oil Grade","LubSys_Lub": "Lub",
            "TrSys_Tr_Chain_Adj": "Tr Chain Adj", "TrSys_Tr_Chain_Play": "Tr Chain Play", "TrSys_Tr_Pin_Adj": "Tr Pin Adj","TrSys_Tr_Pad_Thickness": "Tr Pad Thickness",
            "TrSys_Sproket_Wh_Life": "Sproket Wh Life",
            "TrSys_Tr_Tensioner": "Tr Tensioner",
            "BtyAssys_Cradle_Fitting": "Cradle Fitting", "BtyAssys_Electrolyte_Lvl": "Electolyte Lvl", "BtyAssys_Terminals": "Terminals",
            "BtyAssys_Mineral_Jelly": "Mineral Jelly", "BtyAssys_Vent_Plug": "Vent Plug", "BtyAssys_Bty_Ser_LB": "Bty Ser (LB)",
            "BoggyWh_Rubber_Cond": "Rubber Cond", "BoggyWh_Lub_Pts": "Lub Pts", "BoggyWh_Inner_Outer_Bearing": "Inner / Outer Bearing",
            "BrkSys_Brk_Fluid": "Brk Fluid", "BrkSys_Brk_Lever": "Brk Lever", "ElecSys_Ign_Sw": "Ign Sw",
            "ElecSys_Water_Temp_Guage": "Water Temp Guage", "ElecSys_Fuse_Box": "Fuse Box",
            "ElecSys_Fuse_Svc": "Fuse Svc", "ElecSys_Oil_Pressure_Guage": "Oil Pressure Guage",
            "ElecSys_RPM_Guage": "RPM Guage", "ElecSys_Oil_Temp_Guage": "Oil Temp Guage",
            "ElecSys_Self_Starter_Motor": "Self-Starter Motor", "ElecSys_Alternator_Func": "Alternator Func",
            "ElecSys_Fuel_Guage": "ES Fuel Guage", "ElecSys_Electric_Harness": "Electric Harness",
            "ElecSys_Alternator_Fan_Belt": "Alternator Fan Belt", "ElecSys_Alternator_Noise": "Alternator Noise",
            "ElecSys_Horn": "Horn", "ElecSys_Blower_Heater": "Blower Heater",
            "AirIntakeSys_Air_Cleaner_Cond": "Air Cleaner Cond", "AirIntakeSys_Air_Cleaner_Seal": "Air Cleaner Seal",
            "AirIntakeSys_Hoses_Valves": "Hoses & Valves", "AirIntakeSys_Bluge_Pump": "Bluge Pump",
            "AirIntakeSys_BP_Dust_Cover": "BP Dust Cover", "AirIntakeSys_Hyd_Oil_Lvl_Check": "Hyd Oil Lvl Check",
            "AirIntakeSys_TGC_Lvl_Check": "TGC Lvl Check", "AirIntakeSys_TGC_Oil_Cond": "TGC Oil Cond",
            "TxSys_Stall_Test": "Stall Test","TxSys_Steering_Planetary_Gear": "Steering Planetary Gear", "TxSys_Final_Drive_Func": "Final Drive Func","TxSys_Tx_Oil_Lvl": "Tx Oil Lvl", "TxSys_Tx_Oil_Cond": "Tx Oil Cond",
            "SteeringCon_Stick_Lever_Shift": "Stick Lever Shift", "SteeringCon_Stick_Play": "Stick Play", "SteeringCon_Connect_Rod_Adj": "Connect Rod Adj", "SteeringCon_Steering_Linkages": "Steering Linkages", "SteeringCon_Steering_Pump": "Steering Pump",
            "FuelSys_Fuel_Filter_Cond": "Fuel Filter Cond", "FuelSys_Fuel_Lines_Leakage": "Fuel Lines Leakage", "FuelSys_Fuel_Filter_Body": "Fuel Filter Body", "FuelSys_Fuel_Tk_Strainer": "Fuel Tk Strainer",
            "FuelSys_Fuel_Guage": "FS Fuel Guage", "FuelSys_Fuel_Distr_Cork": "Fuel Distr Cork",  "FuelSys_Fuel_Tk_Cap": "Fuel Tk Cap", "FuelSys_Tk_Inner_Cond": "Tk Inner Cond",
            "created_by": "Created By", "created_at": "Created At"
        }

        # Define your main header grouping in the order you want:
        self.main_header = {
            "Basic Details" : ["BA NO", "Make","Type","CI","In Svc"],
            "Cooling Sys": ["Fins","Rad Paint","Coolant", "CS Leakage", "Rad Cap",	"Fan Belt"],
            "Hyd Ramp": ["Hyd Oil Lvl","TGS Oil Lvl","Tx Oil","Tx Filter","Fan Mech Oil"],
            "Lub Sys": ["Eng Oil","EO Cond","Oil Sump", "LS Leakage", "Oil Grade","Lub"],
            "Tr Sys": [	"Tr Chain Adj","Tr Chain Play","Tr Pin Adj","Tr Pad Thickness","Sproket Wh Life","Tr Tensioner"],
            "Bty & Assys": ["Cradle Fitting","Electolyte Lvl","Terminals","Mineral Jelly","Vent Plug","Bty Ser (LB)"],
            "Boggy Wh": ["Rubber Cond","Lub Pts","Inner / Outer Bearing"],
            "Brk Sys": ["Brk Fluid","Brk Lever"],
            "Elec Sys":	["Ign Sw","Water Temp Guage","Fuse Box","Fuse Svc","Oil Pressure Guage","RPM Guage","Oil Temp Guage","Self-Starter Motor",
                        "Alternator Func","ES Fuel Guage","Electric Harness","Alternator Fan Belt","Alternator Noise","Horn","Blower Heater"],
            "Air Intake Sys": ["Air Cleaner Cond",	"Air Cleaner Seal",	"Hoses & Valves","Bluge Pump","BP Dust Cover","Hyd Oil Lvl Check", 
                         "TGC Lvl Check","TGC Oil Cond"],
            "Tx Sys": ["Stall Test", "Steering Planetary Gear","Final Drive Func", "Tx Oil Lvl", "Tx Oil Cond" ],
            "Steering Con": ["Stick Lever Shift","Stick Play","Connect Rod Adj","Steering Linkages","Steering Pump"],
            "Fuel Sys": ["Fuel Filter Cond","Fuel Lines Leakage","Fuel Filter Body","Fuel Tk Strainer","FS Fuel Guage","Fuel Distr Cork","Fuel Tk Cap","Tk Inner Cond"],
            "Creation Details": ["Created By", "Created At"]
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
        export_button = QPushButton("Export")
        export_button.setFixedSize(100, 45)  # Set button size
        export_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #218838; }
        """)
        export_button.setIcon(QIcon(get_asset_path("assets/icons/xlsx.png")))
        export_button.setIconSize(QSize(20, 20))
        export_button.clicked.connect(self.report_all_a_vehicle_fit)
        header_layout.addWidget(export_button)

        # Import Button
        import_button = QPushButton("Import")
        import_button.setFixedSize(100, 45)  # Set button size
        import_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #218838; }
        """)
        import_button.setIcon(QIcon(get_asset_path("assets/icons/xlsx.png")))
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
        """Fetches and populates the table with vehicle data."""

        # Fetch the data from the database.
        all_vehicle_data = self.db_obj.get_all_a_vehicle_fit(self.current_page, self.page_size)
        self.data = []
        for row in all_vehicle_data:
            # Build the record in the same order as columns.
            record = {col: row.get(key) for key, col in self.db_to_display.items() if col in self.columns}
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
                    
                if col_name not in  ["BA NO", "Make","Type","CI","In Svc", "Created By", "Created At"]:
                    self.date_rules(cell_value, row_index, col_index)
        
                else:
                    item = QTableWidgetItem(str(cell_value))
                    item.setFont(self.tbL_data_font)
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
        total_count = self.db_obj.get_a_vehicle_fit_count()
        total_pages = math.ceil(total_count['total'] / self.page_size)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.populate_table()


    def go_to_page(self, page):
        self.current_page = page
        self.populate_table()


    def update_pagination_buttons(self):
        # Get the total count from the database.
        total_count = self.db_obj.get_a_vehicle_fit_count()
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


    def date_rules(self, cell_value, row_index, col_index):
        item = QTableWidgetItem(str(cell_value))
        item.setTextAlignment(Qt.AlignCenter)

        if cell_value in ["Unsvc", "Incomplete",  "Unsatisfactory", "Down"]:
            item.setBackground(QColor(255, 0, 0)) 
            item.setForeground(QColor(255, 255, 255))
        item.setFont(self.tbL_data_font)
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
        pass
        if hasattr(self.main_parent, "update_a_vehicle_fit_obj") and self.main_parent.update_a_vehicle_fit_obj is not None:
            self.main_parent.content_area.removeWidget(self.main_parent.update_a_vehicle_fit_obj)
            self.main_parent.update_a_vehicle_fit_obj.deleteLater()
            self.main_parent.update_a_vehicle_fit_obj = None  # Reset the reference

        # Create new instance and switch view
        self.main_parent.update_a_vehicle_fit_obj = UpdateAVehicleFit(user_session = self.user_session, data = row, parent = self.main_parent)
        self.main_parent.content_area.addWidget(self.main_parent.update_a_vehicle_fit_obj)
        self.main_parent.content_area.setCurrentWidget(self.main_parent.update_a_vehicle_fit_obj)


    def delete_row(self, row):
        vehicle_id = row['id']
        vehicle_ba_no = row['BA NO']
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Delete Vehicle")
        confirm.setWindowIcon(QIcon(get_asset_path("assets/icons/delete.png")))  # Replace with your actual icon path
        confirm.setText(f"Are you sure you want to delete vehicle {vehicle_ba_no}?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = confirm.exec_()
        if result == QMessageBox.Yes:
            is_deleted_result  = self.db_obj.delete_a_vehicle_fit(vehicle_id)
            if is_deleted_result:
                self.populate_table()  # Refresh table after deletion
            else:
                QMessageBox.warning(self, "Error", "Failed to delete vehicle.")


    def report_row(self, row):
        # print("edit_row parent:",self.main_parent, "\n\n")
        if hasattr(self.main_parent, "a_veh_rpt_view_obj") and self.main_parent.a_veh_rpt_view_obj is not None:
            self.main_parent.content_area.removeWidget(self.main_parent.a_veh_rpt_view_obj)
            self.main_parent.a_veh_rpt_view_obj.deleteLater()
            self.main_parent.a_veh_rpt_view_obj = None  # Reset the reference

        # Create new instance and switch view
        self.main_parent.a_veh_rpt_view_obj = AVehicleReportView(user_session=self.user_session, parent=self.main_parent, data = row, db_to_display = self.db_to_display, main_heading = self.main_header)
        self.main_parent.content_area.addWidget(self.main_parent.a_veh_rpt_view_obj)
        self.main_parent.content_area.setCurrentWidget(self.main_parent.a_veh_rpt_view_obj)
        # self.vr_obj.generate_vehicle_pdf_report_updated(row)


    def report_all_a_vehicle_fit(self):
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
        dialog = ImportAVehiclesFitFE(user_session=self.user_session, db_to_display = self.db_to_display)
        if dialog.exec_():  # If user clicks Save
            self.populate_table()  # Refresh user table