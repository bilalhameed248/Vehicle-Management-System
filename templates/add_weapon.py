from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from database import VMS_DB  
from templates.view_all_vehicles import ViewALLVehicles
from controllers.load_assets import *

class AddWeapon(QWidget):

    def __init__(self, user_session=None, parent=None):
        super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username')
        # print("self.user_id:",self.user_id)
        # print("self.username:",self.username)
        self.main_parent_welcome = parent
        self.initUI()
        self.db_obj = VMS_DB() 


    def initUI(self):
        self.setWindowTitle("Weapon Maintenance Form")
        calendar_icon_path = get_asset_path("assets/icons/calendar.png").replace("\\", "/")
        combo_dd_icon_path = get_asset_path("assets/icons/combo_dd.png").replace("\\", "/")

        self.setStyleSheet(f"""QWidget {{ background-color: #f4f4f4; font-size: 18px; }}
            QLabel {{ font-weight: bold; }}
            QLineEdit, QTextEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px;}}
            QPushButton {{ background-color: #007BFF; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #0056b3; }}
            QPushButton:pressed {{ background-color: #004085; }}
            QGroupBox {{font-weight: bold; border: 2px solid #007BFF; padding: 10px; margin-top: 20px;margin-bottom: 20px; border-radius: 8px; }}
            QGroupBox title {{ color: #007BFF; font-size: 16px; }}
            QScrollBar:vertical {{border: none; background: #f0f0f0; width: 20px; margin: 0px 0px 0px 0px;}}
            QScrollBar::handle:vertical {{background: blue; min-height: 20px; border-radius: 5px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{background: none;}}
            QScrollBar:horizontal {{border: none; background: #f0f0f0; height: 10px; margin: 0px 0px 0px 0px; }}
            QScrollBar::handle:horizontal {{ background: blue; min-width: 20px; border-radius: 5px; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{background: none;}}
            
            QDateEdit {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px; }}
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path}); }}
            QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
            QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
            QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
            QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
            QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white; }}

            QComboBox {{ padding: 5px; border: 1px solid #0078D7; border-radius: 4px; background-color: white; font-size: 18px; }}
            QComboBox::down-arrow {{ width: 20px; border: none; background: transparent; image: url({combo_dd_icon_path}); }}
            QComboBox QAbstractItemView {{ background-color: white; border: 1px solid #4a90e2; selection-background-color: #4a90e2; selection-color: white;}}
            QComboBox::item {{ padding: 8px; }}
            QComboBox::item:selected {{ background-color: #4a90e2; color: white; }}
        """)

        self.basic_details = {}
        self.T_Pod_fields = {}
        self.T_Unit_fields = {}
        self.OS_fields = {}
        self.DMGS_fields = {}
        self.L_Tube_fields = {}
        self.TVPC_fields = {}
        self.Bty_BB_287_fields = {}
        self.NVS_fields = {}
        self.BPC_fields = {}
        self.VPC_fields = {}
        self.L_Bty_fields = {}
        self.Doc_fields = {}
        self.Status_fields = {}

        layout = QVBoxLayout()
        
        form_layout = QGridLayout()
        form_layout.setSpacing(6)

        def combo_input(title, items):
            combo_layout = QVBoxLayout()
            combo_layout.addWidget(QLabel(title))
            self.blocked_combo = QComboBox()
            self.blocked_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.blocked_combo.addItem("--Select--")
            self.blocked_combo.setItemData(0, 0, Qt.UserRole - 1)  # Disable the first item
            self.blocked_combo.addItems(items)
            self.blocked_combo.setCurrentIndex(0)
            combo_layout.addWidget(self.blocked_combo)
            return combo_layout, self.blocked_combo


        def add_basic_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            Wpn_No_layout = QVBoxLayout()
            Wpn_No_layout.addWidget(QLabel("Wpn No."))
            self.Wpn_No_input = QLineEdit()
            Wpn_No_layout.addWidget(self.Wpn_No_input)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(Wpn_No_layout)

            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)

            # # Store references to input fields
            self.basic_details[title] = {
                f"Wpn_No_input": self.Wpn_No_input
            }


        def T_Pod_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.T_Pod_Leg_lock_handle_layout, self.T_Pod_Leg_lock_handle = combo_input("Leg lock handle", combo_items)
            self.T_Pod_Anchor_claw_layout, self.T_Pod_Anchor_claw = combo_input("Anchor claw", combo_items)
            self.T_Pod_Leveling_Bubbles_layout, self.T_Pod_Leveling_Bubbles = combo_input("Leveling Bubbles", combo_items)
            self.T_Pod_Lubrication_layout, self.T_Pod_Lubrication = combo_input("Lubrication", combo_items)
            self.T_Pod_Pull_tube_layout, self.T_Pod_Pull_tube = combo_input("Pull tube", combo_items)
            self.T_Pod_Detent_stop_lever_layout, self.T_Pod_Detent_stop_lever = combo_input("Detent stop lever", combo_items)
            self.T_Pod_Foot_pad_legs_body_condition_layout, self.T_Pod_Foot_pad_legs_body_condition = combo_input("Foot pad/ legs body condition", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.T_Pod_Leg_lock_handle_layout)
            row1_layout.addLayout(self.T_Pod_Anchor_claw_layout)
            row1_layout.addLayout(self.T_Pod_Leveling_Bubbles_layout)
            row1_layout.addLayout(self.T_Pod_Lubrication_layout)
            row1_layout.addLayout(self.T_Pod_Pull_tube_layout)
            row1_layout.addLayout(self.T_Pod_Detent_stop_lever_layout)
            row1_layout.addLayout(self.T_Pod_Foot_pad_legs_body_condition_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)

            # Store references to input fields
            self.T_Pod_fields[title] = {
                f"T_Pod_Leg_lock_handle": self.T_Pod_Leg_lock_handle,
                f"T_Pod_Anchor_claw": self.T_Pod_Anchor_claw,
                f"T_Pod_Leveling_Bubbles": self.T_Pod_Leveling_Bubbles,
                f"T_Pod_Lubrication": self.T_Pod_Lubrication,
                f"T_Pod_Pull_tube": self.T_Pod_Pull_tube,
                f"T_Pod_Detent_stop_lever": self.T_Pod_Detent_stop_lever,
                f"T_Pod_Foot_pad_legs_body_condition": self.T_Pod_Foot_pad_legs_body_condition,
            }
    
    
        def T_Unit_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()  

            combo_items = ["Svc", "Unsvc"]
            self.T_Unit_Traversing_Lock_layout, self.T_Unit_Traversing_Lock = combo_input("Traversing Lock", combo_items)
            self.T_Unit_Elevation_lock_check_layout, self.T_Unit_Elevation_lock_check = combo_input("Elevation lock check", combo_items)
            self.T_Unit_Elevation_lock_handle_layout, self.T_Unit_Elevation_lock_handle = combo_input("Elevation lock handle", combo_items)
            self.T_Unit_Viscosity_of_Viscos_damper_layout, self.T_Unit_Viscosity_of_Viscos_damper = combo_input("Viscosity of Viscos damper", combo_items)
            self.T_Unit_Azimuth_lock_check_layout, self.T_Unit_Azimuth_lock_check = combo_input("Azimuth lock check", combo_items)
            self.T_Unit_Lubrication_layout, self.T_Unit_Lubrication = combo_input("Lubrication", combo_items)
            self.T_Unit_Protective_cover_layout, self.T_Unit_Protective_cover = combo_input("Protective cover", combo_items)
            self.T_Unit_Coil_Card_layout, self.T_Unit_Coil_Card = combo_input("Coil Card", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.T_Unit_Traversing_Lock_layout)
            row1_layout.addLayout(self.T_Unit_Elevation_lock_check_layout)
            row1_layout.addLayout(self.T_Unit_Elevation_lock_handle_layout)
            row1_layout.addLayout(self.T_Unit_Viscosity_of_Viscos_damper_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.T_Unit_Azimuth_lock_check_layout)
            row2_layout.addLayout(self.T_Unit_Lubrication_layout)
            row2_layout.addLayout(self.T_Unit_Protective_cover_layout)
            row2_layout.addLayout(self.T_Unit_Coil_Card_layout)
            
            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            # group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)

            # Store references to input fields
            self.T_Unit_fields[title] = {
                f"T_Unit_Traversing_Lock": self.T_Unit_Traversing_Lock,
                f"T_Unit_Elevation_lock_check": self.T_Unit_Elevation_lock_check,
                f"T_Unit_Elevation_lock_handle": self.T_Unit_Elevation_lock_handle,
                f"T_Unit_Viscosity_of_Viscos_damper": self.T_Unit_Viscosity_of_Viscos_damper,
                f"T_Unit_Azimuth_lock_check": self.T_Unit_Azimuth_lock_check,
                f"T_Unit_Lubrication": self.T_Unit_Lubrication,
                f"T_Unit_Protective_cover": self.T_Unit_Protective_cover,
                f"T_Unit_Coil_Card": self.T_Unit_Coil_Card
            }

        
        def OS_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["Svc", "Unsvc"]
            self.OS_Eye_Shield_layout, self.OS_Eye_Shield = combo_input("Eye Shield",combo_items)
            self.OS_Focusing_knob_layout, self.OS_Focusing_knob = combo_input("Focusing knob",combo_items)
            self.OS_Sillica_gel_condition_layout, self.OS_Sillica_gel_condition = combo_input("Sillica gel condition",combo_items)
            self.OS_Reticle_lamp_layout, self.OS_Reticle_lamp = combo_input("Reticle lamp",combo_items)
            self.OS_Body_condition_layout, self.OS_Body_condition = combo_input("Body condition",combo_items)
            self.OS_N2_purg_filling_connection_layout, self.OS_N2_purg_filling_connection = combo_input("N2 purg / filling connection",combo_items)
            self.OS_Reticle_switch_layout, self.OS_Reticle_switch = combo_input("Reticle switch",combo_items)
            self.OS_Cable_connector_layout, self.OS_Cable_connector = combo_input("Cable connector",combo_items)
            self.OS_Locking_device_layout, self.OS_Locking_device = combo_input("Locking device",combo_items)
            self.OS_Lens_cover_layout, self.OS_Lens_cover = combo_input("Lens cover",combo_items)
            self.OS_Objective_lens_layout, self.OS_Objective_lens = combo_input("Objective lens",combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.OS_Eye_Shield_layout)
            row1_layout.addLayout(self.OS_Focusing_knob_layout)
            row1_layout.addLayout(self.OS_Sillica_gel_condition_layout)
            row1_layout.addLayout(self.OS_Reticle_lamp_layout)
            row1_layout.addLayout(self.OS_Body_condition_layout)
            row1_layout.addLayout(self.OS_N2_purg_filling_connection_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.OS_Reticle_switch_layout)
            row2_layout.addLayout(self.OS_Cable_connector_layout)
            row2_layout.addLayout(self.OS_Locking_device_layout)
            row2_layout.addLayout(self.OS_Lens_cover_layout)
            row2_layout.addLayout(self.OS_Objective_lens_layout)
            

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.OS_fields[title] = {
                f"OS_Eye_Shield": self.OS_Eye_Shield,
                f"OS_Focusing_knob": self.OS_Focusing_knob,
                f"OS_Sillica_gel_condition": self.OS_Sillica_gel_condition,
                f"OS_Reticle_lamp": self.OS_Reticle_lamp,
                f"OS_Body_condition": self.OS_Body_condition,
                f"OS_N2_purg_filling_connection": self.OS_N2_purg_filling_connection,
                f"OS_Reticle_switch": self.OS_Reticle_switch,
                f"OS_Cable_connector": self.OS_Cable_connector,
                f"OS_Locking_device": self.OS_Locking_device,
                f"OS_Lens_cover": self.OS_Lens_cover,
                f"OS_Objective_lens": self.OS_Objective_lens
            }


        def DMGS_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.DMGS_Meter_indicator_AZ_Elev_layout, self.DMGS_Meter_indicator_AZ_Elev = combo_input("Meter indicator (AZ & Elev)", combo_items)
            self.DMGS_Sockets_layout, self.DMGS_Sockets = combo_input("Sockets", combo_items)
            self.DMGS_MGS_DMGS_case_layout, self.DMGS_MGS_DMGS_case = combo_input("MGS/ DMGS case", combo_items)
            self.DMGS_Protective_cover_layout, self.DMGS_Protective_cover = combo_input("Protective cover", combo_items)
            self.DMGS_Cable_layout, self.DMGS_Cable = combo_input("Cable", combo_items)
            self.DMGS_Bty_connector_layout, self.DMGS_Bty_connector = combo_input("Bty connector", combo_items)
            self.DMGS_Self_test_layout, self.DMGS_Self_test = combo_input("Self/ test", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.DMGS_Meter_indicator_AZ_Elev_layout)
            row1_layout.addLayout(self.DMGS_Sockets_layout)
            row1_layout.addLayout(self.DMGS_MGS_DMGS_case_layout)
            row1_layout.addLayout(self.DMGS_Protective_cover_layout)
            row1_layout.addLayout(self.DMGS_Cable_layout)
            row1_layout.addLayout(self.DMGS_Bty_connector_layout)
            row1_layout.addLayout(self.DMGS_Self_test_layout)            

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)

            # Store references to input fields
            self.DMGS_fields[title] = {
                f"DMGS_Meter_indicator_AZ_Elev": self.DMGS_Meter_indicator_AZ_Elev,
                f"DMGS_Sockets": self.DMGS_Sockets,
                f"DMGS_MGS_DMGS_case": self.DMGS_MGS_DMGS_case,
                f"DMGS_Protective_cover": self.DMGS_Protective_cover,
                f"DMGS_Cable": self.DMGS_Cable,
                f"DMGS_Bty_connector": self.DMGS_Bty_connector,
                f"DMGS_Self_test": self.DMGS_Self_test
            }


        def L_Tube_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            combo_items = ["Svc", "Unsvc"]
            self.L_Tube_Body_Condition_layout, self.L_Tube_Body_Condition = combo_input("Body Condition", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.L_Tube_Body_Condition_layout)

            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.L_Tube_fields[title] = {
                f"L_Tube_Body_Condition": self.L_Tube_Body_Condition
            }

        
        def TVPC_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.TVPC_Body_Condition_layout, self.TVPC_Body_Condition = combo_input("Body Condition", combo_items)
            self.TVPC_Fly_Net_layout, self.TVPC_Fly_Net = combo_input("Fly Net", combo_items)
            self.TVPC_On_Off_Switch_layout, self.TVPC_On_Off_Switch = combo_input("On/Off Switch", combo_items)
            self.TVPC_Indicator_It_layout, self.TVPC_Indicator_It = combo_input("Indicator It", combo_items)
            self.TVPC_Connector_layout, self.TVPC_Connector = combo_input("Connector", combo_items)
            self.TVPC_Voltage_layout, self.TVPC_Voltage = combo_input("Voltage", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.TVPC_Body_Condition_layout)
            row1_layout.addLayout(self.TVPC_Fly_Net_layout)
            row1_layout.addLayout(self.TVPC_On_Off_Switch_layout)
            row1_layout.addLayout(self.TVPC_Indicator_It_layout)
            row1_layout.addLayout(self.TVPC_Connector_layout)
            row1_layout.addLayout(self.TVPC_Voltage_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 3)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.TVPC_fields[title] = {
                f"TVPC_Body_Condition": self.TVPC_Body_Condition,
                f"TVPC_Fly_Net": self.TVPC_Fly_Net,
                f"TVPC_On_Off_Switch": self.TVPC_On_Off_Switch,
                f"TVPC_Indicator_It": self.TVPC_Indicator_It,
                f"TVPC_Connector": self.TVPC_Connector,
                f"TVPC_Voltage": self.TVPC_Voltage
            }


        def Bty_BB_287_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.Bty_BB_287_Bty_connector_layout, self.Bty_BB_287_Bty_connector = combo_input("Bty connector", combo_items)
            self.Bty_BB_287_Voltage_24V_sec_layout, self.Bty_BB_287_Voltage_24V_sec = combo_input("Voltage +24 V sec", combo_items)
            self.Bty_BB_287_Voltage_50V_layout, self.Bty_BB_287_Voltage_50V = combo_input("Voltage +50 V", combo_items)
            self.Bty_BB_287_Voltage_50V_sec_layout, self.Bty_BB_287_Voltage_50V_sec = combo_input("Voltage +50 V sec", combo_items)
            self.Bty_BB_287_Bty_condition_layout, self.Bty_BB_287_Bty_condition = combo_input("Bty condition", combo_items)
            self.Bty_BB_287_Bty_Tvpc_layout, self.Bty_BB_287_Bty_Tvpc = combo_input("TVPC", combo_items)
            self.Bty_BB_287_Power_cable_condition_layout, self.Bty_BB_287_Power_cable_condition = combo_input("Power cable condition", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.Bty_BB_287_Bty_connector_layout)
            row1_layout.addLayout(self.Bty_BB_287_Voltage_24V_sec_layout)
            row1_layout.addLayout(self.Bty_BB_287_Voltage_50V_layout)
            row1_layout.addLayout(self.Bty_BB_287_Voltage_50V_sec_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.Bty_BB_287_Bty_condition_layout)
            row2_layout.addLayout(self.Bty_BB_287_Bty_Tvpc_layout)
            row2_layout.addLayout(self.Bty_BB_287_Power_cable_condition_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 2)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.Bty_BB_287_fields[title] = {
                f"Bty_BB_287_Bty_connector": self.Bty_BB_287_Bty_connector,
                f"Bty_BB_287_Voltage_24V_sec": self.Bty_BB_287_Voltage_24V_sec,
                f"Bty_BB_287_Voltage_50V": self.Bty_BB_287_Voltage_50V,
                f"Bty_BB_287_Voltage_50V_sec": self.Bty_BB_287_Voltage_50V_sec,
                f"Bty_BB_287_Bty_condition": self.Bty_BB_287_Bty_condition,
                f"Bty_BB_287_Bty_Tvpc": self.Bty_BB_287_Bty_Tvpc,
                f"Bty_BB_287_Power_cable_condition": self.Bty_BB_287_Power_cable_condition
            }


        def NVS_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.NVS_Coolant_unit_layout, self.NVS_Coolant_unit = combo_input("Coolant unit", combo_items)
            self.NVS_Eye_piece_layout, self.NVS_Eye_piece = combo_input("Eye piece", combo_items)
            self.NVS_Cable_connector_layout, self.NVS_Cable_connector = combo_input("Cable connector", combo_items)
            self.NVS_Lens_assy_layout, self.NVS_Lens_assy = combo_input("Lens assy", combo_items)
            self.NVS_Power_cable_condition_layout, self.NVS_Power_cable_condition = combo_input("Power cable condition", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.NVS_Coolant_unit_layout)
            row1_layout.addLayout(self.NVS_Eye_piece_layout)
            row1_layout.addLayout(self.NVS_Cable_connector_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.NVS_Lens_assy_layout)
            row2_layout.addLayout(self.NVS_Power_cable_condition_layout)
            

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 2)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.NVS_fields[title] = {
                f"NVS_Coolant_unit": self.NVS_Coolant_unit,
                f"NVS_Eye_piece": self.NVS_Eye_piece,
                f"NVS_Cable_connector": self.NVS_Cable_connector,
                f"NVS_Lens_assy": self.NVS_Lens_assy,
                f"NVS_Power_cable_condition": self.NVS_Power_cable_condition
            }


        def BPC_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.BPC_Body_layout, self.BPC_Body = combo_input("Body", combo_items)
            self.BPC_Cables_layout, self.BPC_Cables = combo_input("Cables", combo_items)
            self.BPC_On_Off_Switch_layout, self.BPC_On_Off_Switch = combo_input("On/Off Switch", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.BPC_Body_layout)
            row1_layout.addLayout(self.BPC_Cables_layout)
            row1_layout.addLayout(self.BPC_On_Off_Switch_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.BPC_fields[title] = {
                f"BPC_Body": self.BPC_Body,
                f"BPC_Cables": self.BPC_Cables,
                f"BPC_On_Off_Switch": self.BPC_On_Off_Switch
            }


        def VPC_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc"]
            self.VPC_Body_layout, self.VPC_Body = combo_input("Body", combo_items)
            self.VPC_Switch_layout, self.VPC_Switch = combo_input("Switch", combo_items)
            self.VPC_VPC_Power_Cable_layout, self.VPC_VPC_Power_Cable = combo_input("VPC Power Cable", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.VPC_Body_layout)
            row1_layout.addLayout(self.VPC_Switch_layout)
            row1_layout.addLayout(self.VPC_VPC_Power_Cable_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.VPC_fields[title] = {
                f"VPC_Body": self.VPC_Body,
                f"VPC_Switch": self.VPC_Switch,
                f"VPC_VPC_Power_Cable": self.VPC_VPC_Power_Cable
            } 


        def L_Bty_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            combo_items = ["Svc", "Unsvc"]
            self.L_Bty_Bty_Voltage_layout, self.L_Bty_Bty_Voltage = combo_input("Bty Voltage", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.L_Bty_Bty_Voltage_layout)

            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.L_Bty_fields[title] = {
                f"L_Bty_Bty_Voltage": self.L_Bty_Bty_Voltage
            }


        def Doc_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["Complete", "Incomplete"]
            self.Doc_6_Monthly_verification_record_layout, self.Doc_6_Monthly_verification_record = combo_input("6 Monthly verification record", combo_items)
            self.Doc_Last_ATI_pts_has_been_killed_layout, self.Doc_Last_ATI_pts_has_been_killed = combo_input("Last ATI pts has been killed", combo_items)
            self.Doc_Bty_charging_record_layout, self.Doc_Bty_charging_record = combo_input("Bty charging record", combo_items)
            self.Doc_Storage_temp_Humidity_record_layout, self.Doc_Storage_temp_Humidity_record = combo_input("Storage temp & Humidity record", combo_items)
            self.Doc_Firing_record_check_layout, self.Doc_Firing_record_check = combo_input("Firing record check", combo_items)
            self.Doc_Svc_ability_Completeness_of_tools_accy_layout, self.Doc_Svc_ability_Completeness_of_tools_accy = combo_input("Svc ability & Completeness of tools & accy", combo_items)
            self.Doc_Self_test_record_check_layout, self.Doc_Self_test_record_check = combo_input("Self test record check", combo_items)
            self.Doc_Is_eARMS_fully_func_layout, self.Doc_Is_eARMS_fully_func = combo_input("Is eARMS fully func and all the processes involved are being carried out through eARMS", combo_items)
            self.Doc_Complete_eqpt_inventory_update_on_eARMS_layout, self.Doc_Complete_eqpt_inventory_update_on_eARMS = combo_input("Complete eqpt inventory update on eARMS", combo_items)
            self.Doc_DRWO_work_order_being_processed_on_eARMS_layout, self.Doc_DRWO_work_order_being_processed_on_eARMS = combo_input("DRWO/ work order being processed on eARMS", combo_items)
            self.Doc_Are_Log_book_maintain_properly_layout, self.Doc_Are_Log_book_maintain_properly = combo_input("Are Log book maintain properly", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.Doc_6_Monthly_verification_record_layout)
            row1_layout.addLayout(self.Doc_Last_ATI_pts_has_been_killed_layout)
            row1_layout.addLayout(self.Doc_Bty_charging_record_layout)
            
            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.Doc_Storage_temp_Humidity_record_layout)
            row2_layout.addLayout(self.Doc_Firing_record_check_layout)
            row2_layout.addLayout(self.Doc_Svc_ability_Completeness_of_tools_accy_layout)
            
            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.Doc_Self_test_record_check_layout)
            row3_layout.addLayout(self.Doc_Is_eARMS_fully_func_layout)
            
            row4_layout = QHBoxLayout()
            row4_layout.addLayout(self.Doc_Complete_eqpt_inventory_update_on_eARMS_layout)
            row4_layout.addLayout(self.Doc_DRWO_work_order_being_processed_on_eARMS_layout)
            row4_layout.addLayout(self.Doc_Are_Log_book_maintain_properly_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.Doc_fields[title] = {
                f"Doc_6_Monthly_verification_record": self.Doc_6_Monthly_verification_record,
                f"Doc_Last_ATI_pts_has_been_killed": self.Doc_Last_ATI_pts_has_been_killed,
                f"Doc_Bty_charging_record": self.Doc_Bty_charging_record,
                f"Doc_Storage_temp_Humidity_record": self.Doc_Storage_temp_Humidity_record,
                f"Doc_Firing_record_check": self.Doc_Firing_record_check,
                f"Doc_Svc_ability_Completeness_of_tools_accy": self.Doc_Svc_ability_Completeness_of_tools_accy,
                f"Doc_Self_test_record_check": self.Doc_Self_test_record_check,
                f"Doc_Is_eARMS_fully_func": self.Doc_Is_eARMS_fully_func,
                f"Doc_Complete_eqpt_inventory_update_on_eARMS": self.Doc_Complete_eqpt_inventory_update_on_eARMS,
                f"Doc_DRWO_work_order_being_processed_on_eARMS": self.Doc_DRWO_work_order_being_processed_on_eARMS,
                f"Doc_Are_Log_book_maintain_properly": self.Doc_Are_Log_book_maintain_properly
            }

        
        def Status_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            combo_items = ["Svc", "Unsvc"]
            self.Status_layout, self.Status = combo_input("Status", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.Status_layout)

            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)

            # # Store references to input fields
            self.Status_fields[title] = {
                f"Status": self.Status
            }

        # Maintenance Sections
        add_basic_section("Basic Details", 0, 0)
        T_Pod_Section("T.Pod", 2, 0)
        T_Unit_Section("T. Unit", 4, 0)
        OS_Section("OS", 6, 0)
        DMGS_Section("DMGS", 8, 0)
        L_Tube_section("L-Tube", 10, 0)
        TVPC_Section("TVPC", 10, 1)
        Bty_BB_287_Section("Bty BB-287", 12, 0)
        NVS_Section("NVS", 12, 2)
        BPC_Section("BPC", 14, 0)
        VPC_Section("VPC", 14, 1)
        L_Bty_section("L.Bty", 14, 2)
        Doc_section("Doc", 16, 0)
        Status_section("Status", 18, 0)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(" Save")
        save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        save_button.setIconSize(QSize(20, 20))
        save_button.clicked.connect(self.save_weapon)

        clear_button = QPushButton(" Clear/Reset")
        clear_button.setIcon(QIcon(get_asset_path("assets/icons/clear.png")))
        clear_button.setIconSize(QSize(20, 20))
        clear_button.clicked.connect(self.clear_fields)

        cancel_button = QPushButton(" Cancel")
        cancel_button.setIcon(QIcon(get_asset_path("assets/icons/cancel.png")))
        cancel_button.setIconSize(QSize(20, 20))
        # cancel_button.clicked.connect(self.cancel_add_weapon)

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(cancel_button)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        form_container = QWidget()
        form_container.setLayout(form_layout)
        scroll_area.setWidget(form_container)

        # Add widgets to layout
        layout.addWidget(scroll_area)
        layout.addLayout(button_layout)
        self.setLayout(layout)


    def save_weapon(self):
        """ Inserts user into the database """
        add_weapon_data = {}

        if not (self.basic_details['Basic Details']['Wpn_No_input'].text().strip()):
            QMessageBox.warning(self, "Error", "Wpn No required!")
            return
        
        field_categories = [
            self.basic_details, self.T_Pod_fields, self.T_Unit_fields, self.OS_fields, 
            self.DMGS_fields, self.L_Tube_fields, self.TVPC_fields, self.Bty_BB_287_fields, 
            self.NVS_fields, self.BPC_fields, self.VPC_fields, self.L_Bty_fields, 
            self.Doc_fields, self.Status_fields
        ]
        
        for category in field_categories:
            for fields in category.values():
                for key, widget in fields.items():
                    if isinstance(widget, QLineEdit):
                        add_weapon_data[key] = widget.text().strip()
                    elif isinstance(widget, QComboBox):
                        selected_text = widget.currentText().strip()
                        add_weapon_data[key] = None if selected_text == "--Select--" else selected_text

        add_weapon_data['created_by'] = self.user_id

        is_data_inserted = self.db_obj.insert_weapon(add_weapon_data)
        if not is_data_inserted:
            QMessageBox.warning(self, "Failed", "Error while saving the data..! Please Try Again")
            return
        else:
            QMessageBox.information(self, "Success", "Weapon added successfully!")
            return
        
    def clear_fields(self):
        pass