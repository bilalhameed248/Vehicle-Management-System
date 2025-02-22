from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QDateEdit, QTextEdit, QGridLayout, QVBoxLayout, QComboBox,
    QPushButton, QScrollArea, QFormLayout, QHBoxLayout, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from database import VMS_DB  
from templates.view_all_vehicles import ViewALLVehicles
from controllers.load_assets import *

class AddAVehicleFit(QWidget):

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
        self.setWindowTitle("Vehicle Maintenance Form")
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

        self.add_basic_section_fields = {}
        self.Cooling_Section_fields = {}
        self.HydRamp_Section_fields = {}
        self.LubSys_Section_fields = {}
        self.TrSys_Section_fields = {}
        self.BtyAssys_section_fields = {}
        self.BoggyWh_Section_fields = {}
        self.BrkSys_Section_fields = {}
        self.ElecSys_Section_fields = {}
        self.AirIntakeSys_Section_fields = {}
        self.TxSys_Section_fields = {}
        self.SteeringCon_section_fields = {}
        self.FuelSys_section_fields = {}

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
        
        def text_input_fun(title):
            text_input_layout = QVBoxLayout()
            text_input_layout.addWidget(QLabel(title))
            self.text_input = QLineEdit()
            text_input_layout.addWidget(self.text_input)
            return text_input_layout, self.text_input


        def add_basic_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()
            self.ba_no_input_layout, self.ba_no_input = text_input_fun("BA NO")
            self.make_input_layout, self.make_input = text_input_fun("Make")
            self.type_input_layout, self.type_input = text_input_fun("Type")
            self.CI_input_layout, self.CI_input = text_input_fun("CI")
            self.In_Svc_input_layout, self.In_Svc_input = text_input_fun("In Svc")

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.ba_no_input_layout)
            row1_layout.addLayout(self.make_input_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.type_input_layout)
            row2_layout.addLayout(self.CI_input_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.In_Svc_input_layout)
            
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.add_basic_section_fields[title] = {
                f"ba_no_input": self.ba_no_input,
                f"make_input": self.make_input,
                f"type_input": self.type_input,
                f"CI_input": self.CI_input,
                f"In_Svc_input": self.In_Svc_input
            }


        def Cooling_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            
            self.Cooling_Fins_layout, self.Cooling_Fins = combo_input("Fins", combo_items)
            self.Cooling_Rad_Paint_layout, self.Cooling_Rad_Paint = combo_input("Rad Paint", combo_items)
            self.Cooling_Coolant_layout, self.Cooling_Coolant = combo_input("Coolant", combo_items)
            self.Cooling_Leakage_layout, self.Cooling_Leakage = combo_input("Leakage", combo_items)
            self.Cooling_Rad_Cap_layout, self.Cooling_Rad_Cap = combo_input("Rad Cap", combo_items)
            self.Cooling_Fan_Belt_layout, self.Cooling_Fan_Belt = combo_input("Fan Belt", combo_items)
            
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.Cooling_Fins_layout)
            row1_layout.addLayout(self.Cooling_Rad_Paint_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.Cooling_Coolant_layout)
            row2_layout.addLayout(self.Cooling_Leakage_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.Cooling_Rad_Cap_layout)
            row3_layout.addLayout(self.Cooling_Fan_Belt_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.Cooling_Section_fields[title] = {
                f"Cooling_Fins": self.Cooling_Fins,
                f"Cooling_Rad_Paint": self.Cooling_Rad_Paint,
                f"Cooling_Coolant": self.Cooling_Coolant,
                f"Cooling_Leakage": self.Cooling_Leakage,
                f"Cooling_Rad_Cap": self.Cooling_Rad_Cap,
                f"Cooling_Fan_Belt": self.Cooling_Fan_Belt
            }
    
    
        def HydRamp_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.HydRamp_Hyd_Oil_Lvl_layout, self.HydRamp_Hyd_Oil_Lvl = combo_input("Hyd Oil Lvl", combo_items)
            self.HydRamp_TGS_Oil_Lvl_layout, self.HydRamp_TGS_Oil_Lvl = combo_input("TGS Oil Lvl", combo_items)
            self.HydRamp_Tx_Oil_layout, self.HydRamp_Tx_Oil = combo_input("Tx Oil", combo_items)
            self.HydRamp_Tx_Filter_layout, self.HydRamp_Tx_Filter = combo_input("Tx Filter", combo_items)
            self.HydRamp_Fan_Mech_Oil_layout, self.HydRamp_Fan_Mech_Oil = combo_input("Fan Mech Oil", combo_items)
            
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.HydRamp_Hyd_Oil_Lvl_layout)
            row1_layout.addLayout(self.HydRamp_TGS_Oil_Lvl_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.HydRamp_Tx_Oil_layout)
            row2_layout.addLayout(self.HydRamp_Tx_Filter_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.HydRamp_Fan_Mech_Oil_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.HydRamp_Section_fields[title] = {
                f"HydRamp_Hyd_Oil_Lvl": self.HydRamp_Hyd_Oil_Lvl,
                f"HydRamp_TGS_Oil_Lvl": self.HydRamp_TGS_Oil_Lvl,
                f"HydRamp_Tx_Oil": self.HydRamp_Tx_Oil,
                f"HydRamp_Tx_Filter": self.HydRamp_Tx_Filter,
                f"HydRamp_Fan_Mech_Oil": self.HydRamp_Fan_Mech_Oil
            }

        
        def LubSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.LubSys_Eng_Oil_layout, self.LubSys_Eng_Oil = combo_input("Eng Oil",combo_items)
            self.LubSys_EO_Cond_layout, self.LubSys_EO_Cond = combo_input("EO Cond",combo_items)
            self.LubSys_Oil_Sump_layout, self.LubSys_Oil_Sump = combo_input("Oil Sump",combo_items)
            self.LubSys_Leakage_layout, self.LubSys_Leakage = combo_input("Leakage",combo_items)
            self.LubSys_Oil_Grade_layout, self.LubSys_Oil_Grade = combo_input("Oil Grade",combo_items)
            self.LubSys_Lub_layout, self.LubSys_Lub = combo_input("Lub",combo_items)
            

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.LubSys_Eng_Oil_layout)
            row1_layout.addLayout(self.LubSys_EO_Cond_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.LubSys_Oil_Sump_layout)
            row2_layout.addLayout(self.LubSys_Leakage_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.LubSys_Oil_Grade_layout)
            row3_layout.addLayout(self.LubSys_Lub_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.LubSys_Section_fields[title] = {
                f"LubSys_Eng_Oil": self.LubSys_Eng_Oil,
                f"LubSys_EO_Cond": self.LubSys_EO_Cond,
                f"LubSys_Oil_Sump": self.LubSys_Oil_Sump,
                f"LubSys_Leakage": self.LubSys_Leakage,
                f"LubSys_Oil_Grade": self.LubSys_Oil_Grade,
                f"LubSys_Lub": self.LubSys_Lub
            }


        def TrSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]

            self.TrSys_Tr_Chain_Adj_layout, self.TrSys_Tr_Chain_Adj = combo_input("Tr Chain Adj", combo_items)
            self.TrSys_Tr_Chain_Play_layout, self.TrSys_Tr_Chain_Play = combo_input("Tr Chain Play", combo_items)
            self.TrSys_Tr_Pin_Adj_layout, self.TrSys_Tr_Pin_Adj = combo_input("Tr Pin Adj", combo_items)
            self.TrSys_Tr_Pad_Thickness_layout, self.TrSys_Tr_Pad_Thickness = combo_input("Tr Pad Thickness", combo_items)
            self.TrSys_Sproket_Wh_Life_layout, self.TrSys_Sproket_Wh_Life = combo_input("Sproket Wh Life", combo_items)
            self.TrSys_Tr_Tensioner_layout, self.TrSys_Tr_Tensioner = combo_input("Tr Tensioner", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.TrSys_Tr_Chain_Adj_layout)
            row1_layout.addLayout(self.TrSys_Tr_Chain_Play_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.TrSys_Tr_Pin_Adj_layout)
            row2_layout.addLayout(self.TrSys_Tr_Pad_Thickness_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.TrSys_Sproket_Wh_Life_layout)
            row3_layout.addLayout(self.TrSys_Tr_Tensioner_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.TrSys_Section_fields[title] = {
                f"TrSys_Tr_Chain_Adj": self.TrSys_Tr_Chain_Adj,
                f"TrSys_Tr_Chain_Play": self.TrSys_Tr_Chain_Play,
                f"TrSys_Tr_Pin_Adj": self.TrSys_Tr_Pin_Adj,
                f"TrSys_Tr_Pad_Thickness": self.TrSys_Tr_Pad_Thickness,
                f"TrSys_Sproket_Wh_Life": self.TrSys_Sproket_Wh_Life,
                f"TrSys_Tr_Tensioner": self.TrSys_Tr_Tensioner
            }


        def BtyAssys_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.BtyAssys_Cradle_Fitting_layout, self.BtyAssys_Cradle_Fitting = combo_input("Cradle Fitting", combo_items)
            self.BtyAssys_Electrolyte_Lvl_layout, self.BtyAssys_Electrolyte_Lvl = combo_input("Electolyte Lvl", combo_items)
            self.BtyAssys_Terminals_layout, self.BtyAssys_Terminals = combo_input("Terminals", combo_items)
            self.BtyAssys_Mineral_Jelly_layout, self.BtyAssys_Mineral_Jelly = combo_input("Mineral Jelly", combo_items)
            self.BtyAssys_Vent_Plug_layout, self.BtyAssys_Vent_Plug = combo_input("Vent Plug", combo_items)
            self.BtyAssys_Bty_Ser_LB_layout, self.BtyAssys_Bty_Ser_LB = combo_input("Bty Ser (LB)", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.BtyAssys_Cradle_Fitting_layout)
            row1_layout.addLayout(self.BtyAssys_Electrolyte_Lvl_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.BtyAssys_Terminals_layout)
            row2_layout.addLayout(self.BtyAssys_Mineral_Jelly_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.BtyAssys_Vent_Plug_layout)
            row3_layout.addLayout(self.BtyAssys_Bty_Ser_LB_layout)

            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.BtyAssys_section_fields[title] = {
                f"BtyAssys_Cradle_Fitting": self.BtyAssys_Cradle_Fitting,
                f"BtyAssys_Electrolyte_Lvl": self.BtyAssys_Electrolyte_Lvl,
                f"BtyAssys_Terminals": self.BtyAssys_Terminals,
                f"BtyAssys_Mineral_Jelly": self.BtyAssys_Mineral_Jelly,
                f"BtyAssys_Vent_Plug": self.BtyAssys_Vent_Plug,
                f"BtyAssys_Bty_Ser_LB": self.BtyAssys_Bty_Ser_LB
            }

        
        def BoggyWh_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]

            self.BoggyWh_Rubber_Cond_layout, self.BoggyWh_Rubber_Cond = combo_input("Rubber Cond", combo_items)
            self.BoggyWh_Lub_Pts_layout, self.BoggyWh_Lub_Pts = combo_input("Lub Pts", combo_items)
            self.BoggyWh_Inner_Outer_Bearing_layout, self.BoggyWh_Inner_Outer_Bearing = combo_input("Inner / Outer Bearing", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.BoggyWh_Rubber_Cond_layout)
            row1_layout.addLayout(self.BoggyWh_Lub_Pts_layout)
            row1_layout.addLayout(self.BoggyWh_Inner_Outer_Bearing_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 2)

            # Store references to input fields
            self.BoggyWh_Section_fields[title] = {
                f"BoggyWh_Rubber_Cond": self.BoggyWh_Rubber_Cond,
                f"BoggyWh_Lub_Pts": self.BoggyWh_Lub_Pts,
                f"BoggyWh_Inner_Outer_Bearing": self.BoggyWh_Inner_Outer_Bearing
            }


        def BrkSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.BrkSys_Brk_Fluid_layout, self.BrkSys_Brk_Fluid = combo_input("Brk Fluid", combo_items)
            self.BrkSys_Brk_Lever_layout, self.BrkSys_Brk_Lever = combo_input("Brk Lever", combo_items)
            
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.BrkSys_Brk_Fluid_layout)
            row1_layout.addLayout(self.BrkSys_Brk_Lever_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # Store references to input fields
            self.BrkSys_Section_fields[title] = {
                f"BrkSys_Brk_Fluid": self.BrkSys_Brk_Fluid,
                f"BrkSys_Brk_Lever": self.BrkSys_Brk_Lever
            }


        def ElecSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.ElecSys_Ign_Sw_layout, self.ElecSys_Ign_Sw = combo_input("Ign Sw", combo_items)
            self.ElecSys_Water_Temp_Guage_layout, self.ElecSys_Water_Temp_Guage = combo_input("Water Temp Guage", combo_items)
            self.ElecSys_Fuse_Box_layout, self.ElecSys_Fuse_Box = combo_input("Fuse Box", combo_items)
            self.ElecSys_Fuse_Svc_layout, self.ElecSys_Fuse_Svc = combo_input("Fuse Svc", combo_items)
            self.ElecSys_Oil_Pressure_Guage_layout, self.ElecSys_Oil_Pressure_Guage = combo_input("Oil Pressure Guage", combo_items)
            self.ElecSys_RPM_Guage_layout, self.ElecSys_RPM_Guage = combo_input("RPM Guage", combo_items)
            self.ElecSys_Oil_Temp_Guage_layout, self.ElecSys_Oil_Temp_Guage = combo_input("Oil Temp Guage", combo_items)
            self.ElecSys_Self_Starter_Motor_layout, self.ElecSys_Self_Starter_Motor = combo_input("Self-Starter Motor", combo_items)
            self.ElecSys_Alternator_Func_layout, self.ElecSys_Alternator_Func = combo_input("Alternator Func", combo_items)
            self.ElecSys_Fuel_Guage_layout, self.ElecSys_Fuel_Guage = combo_input("Fuel Guage", combo_items)
            self.ElecSys_Electric_Harness_layout, self.ElecSys_Electric_Harness = combo_input("Electric Harness", combo_items)
            self.ElecSys_Alternator_Fan_Belt_layout, self.ElecSys_Alternator_Fan_Belt = combo_input("Alternator Fan Belt", combo_items)
            self.ElecSys_Alternator_Noise_layout, self.ElecSys_Alternator_Noise = combo_input("Alternator Noise", combo_items)
            self.ElecSys_Horn_layout, self.ElecSys_Horn = combo_input("Horn", combo_items)
            self.ElecSys_Blower_Heater_layout, self.ElecSys_Blower_Heater = combo_input("Blower Heater", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.ElecSys_Ign_Sw_layout)
            row1_layout.addLayout(self.ElecSys_Water_Temp_Guage_layout)
            row1_layout.addLayout(self.ElecSys_Fuse_Box_layout)
            row1_layout.addLayout(self.ElecSys_Fuse_Svc_layout)
            row1_layout.addLayout(self.ElecSys_Oil_Pressure_Guage_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.ElecSys_RPM_Guage_layout)
            row2_layout.addLayout(self.ElecSys_Oil_Temp_Guage_layout)
            row2_layout.addLayout(self.ElecSys_Self_Starter_Motor_layout)
            row2_layout.addLayout(self.ElecSys_Alternator_Func_layout)
            row2_layout.addLayout(self.ElecSys_Fuel_Guage_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.ElecSys_Electric_Harness_layout)
            row3_layout.addLayout(self.ElecSys_Alternator_Fan_Belt_layout)
            row3_layout.addLayout(self.ElecSys_Alternator_Noise_layout)
            row3_layout.addLayout(self.ElecSys_Horn_layout)
            row3_layout.addLayout(self.ElecSys_Blower_Heater_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.ElecSys_Section_fields[title] = {
                f"ElecSys_Ign_Sw": self.ElecSys_Ign_Sw,
                f"ElecSys_Water_Temp_Guage": self.ElecSys_Water_Temp_Guage,
                f"ElecSys_Fuse_Box": self.ElecSys_Fuse_Box,
                f"ElecSys_Fuse_Svc": self.ElecSys_Fuse_Svc,
                f"ElecSys_Oil_Pressure_Guage": self.ElecSys_Oil_Pressure_Guage,
                f"ElecSys_RPM_Guage": self.ElecSys_RPM_Guage,
                f"ElecSys_Oil_Temp_Guage": self.ElecSys_Oil_Temp_Guage,
                f"ElecSys_Self_Starter_Motor": self.ElecSys_Self_Starter_Motor,
                f"ElecSys_Alternator_Func": self.ElecSys_Alternator_Func,
                f"ElecSys_Fuel_Guage": self.ElecSys_Fuel_Guage,
                f"ElecSys_Electric_Harness": self.ElecSys_Electric_Harness,
                f"ElecSys_Alternator_Fan_Belt": self.ElecSys_Alternator_Fan_Belt,
                f"ElecSys_Alternator_Noise": self.ElecSys_Alternator_Noise,
                f"ElecSys_Horn": self.ElecSys_Horn,
                f"ElecSys_Blower_Heater": self.ElecSys_Blower_Heater
            }


        def AirIntakeSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.AirIntakeSys_Air_Cleaner_Cond_layout, self.AirIntakeSys_Air_Cleaner_Cond = combo_input("Air Cleaner Cond", combo_items)
            self.AirIntakeSys_Air_Cleaner_Seal_layout, self.AirIntakeSys_Air_Cleaner_Seal = combo_input("Air Cleaner Seal", combo_items)
            self.AirIntakeSys_Hoses_Valves_layout, self.AirIntakeSys_Hoses_Valves = combo_input("Hoses & Valves", combo_items)
            self.AirIntakeSys_Bluge_Pump_layout, self.AirIntakeSys_Bluge_Pump = combo_input("Bluge Pump", combo_items)
            self.AirIntakeSys_BP_Dust_Cover_layout, self.AirIntakeSys_BP_Dust_Cover = combo_input("BP Dust Cover", combo_items)
            self.AirIntakeSys_Hyd_Oil_Lvl_Check_layout, self.AirIntakeSys_Hyd_Oil_Lvl_Check = combo_input("Hyd Oil Lvl Check", combo_items)
            self.AirIntakeSys_TGC_Lvl_Check_layout, self.AirIntakeSys_TGC_Lvl_Check = combo_input("TGC Lvl Check", combo_items)
            self.AirIntakeSys_TGC_Oil_Cond_layout, self.AirIntakeSys_TGC_Oil_Cond = combo_input("TGC Oil Cond", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.AirIntakeSys_Air_Cleaner_Cond_layout)
            row1_layout.addLayout(self.AirIntakeSys_Air_Cleaner_Seal_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.AirIntakeSys_Hoses_Valves_layout)
            row2_layout.addLayout(self.AirIntakeSys_Bluge_Pump_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.AirIntakeSys_BP_Dust_Cover_layout)
            row3_layout.addLayout(self.AirIntakeSys_Hyd_Oil_Lvl_Check_layout)

            row4_layout = QHBoxLayout()
            row4_layout.addLayout(self.AirIntakeSys_TGC_Lvl_Check_layout)
            row4_layout.addLayout(self.AirIntakeSys_TGC_Oil_Cond_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)
            group_layout.addLayout(row4_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.AirIntakeSys_Section_fields[title] = {
                f"AirIntakeSys_Air_Cleaner_Cond": self.AirIntakeSys_Air_Cleaner_Cond,
                f"AirIntakeSys_Air_Cleaner_Seal": self.AirIntakeSys_Air_Cleaner_Seal,
                f"AirIntakeSys_Hoses_Valves": self.AirIntakeSys_Hoses_Valves,
                f"AirIntakeSys_Bluge_Pump": self.AirIntakeSys_Bluge_Pump,
                f"AirIntakeSys_BP_Dust_Cover": self.AirIntakeSys_BP_Dust_Cover,
                f"AirIntakeSys_Hyd_Oil_Lvl_Check": self.AirIntakeSys_Hyd_Oil_Lvl_Check,
                f"AirIntakeSys_TGC_Lvl_Check": self.AirIntakeSys_TGC_Lvl_Check,
                f"AirIntakeSys_TGC_Oil_Cond": self.AirIntakeSys_TGC_Oil_Cond
            }


        def TxSys_Section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout() 

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]

            self.TxSys_Stall_Test_layout, self.TxSys_Stall_Test = combo_input("Stall Test", combo_items)
            self.TxSys_Steering_Planetary_Gear_layout, self.TxSys_Steering_Planetary_Gear = combo_input("Steering Planetary Gear", combo_items)
            self.TxSys_Final_Drive_Func_layout, self.TxSys_Final_Drive_Func = combo_input("Final Drive Func", combo_items)
            self.TxSys_Tx_Oil_Lvl_layout, self.TxSys_Tx_Oil_Lvl = combo_input("Tx Oil Lvl", combo_items)
            self.TxSys_Tx_Oil_Cond_layout, self.TxSys_Tx_Oil_Cond = combo_input("Tx Oil Cond", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.TxSys_Stall_Test_layout)
            row1_layout.addLayout(self.TxSys_Steering_Planetary_Gear_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.TxSys_Final_Drive_Func_layout)
            row2_layout.addLayout(self.TxSys_Tx_Oil_Lvl_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.TxSys_Tx_Oil_Cond_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # Store references to input fields
            self.TxSys_Section_fields[title] = {
                f"TxSys_Stall_Test": self.TxSys_Stall_Test,
                f"TxSys_Steering_Planetary_Gear": self.TxSys_Steering_Planetary_Gear,
                f"TxSys_Final_Drive_Func": self.TxSys_Final_Drive_Func,
                f"TxSys_Tx_Oil_Lvl": self.TxSys_Tx_Oil_Lvl,
                f"TxSys_Tx_Oil_Cond": self.TxSys_Tx_Oil_Cond
            } 


        def SteeringCon_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()    

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]
            self.SteeringCon_Stick_Lever_Shift_layout, self.SteeringCon_Stick_Lever_Shift = combo_input("Stick Lever Shift", combo_items)
            self.SteeringCon_Stick_Play_layout, self.SteeringCon_Stick_Play = combo_input("Stick Play", combo_items)
            self.SteeringCon_Connect_Rod_Adj_layout, self.SteeringCon_Connect_Rod_Adj = combo_input("Connect Rod Adj", combo_items)
            self.SteeringCon_Steering_Linkages_layout, self.SteeringCon_Steering_Linkages = combo_input("Steering Linkages", combo_items)
            self.SteeringCon_Steering_Pump_layout, self.SteeringCon_Steering_Pump = combo_input("Steering Pump", combo_items)

            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.SteeringCon_Stick_Lever_Shift_layout)
            row1_layout.addLayout(self.SteeringCon_Stick_Play_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.SteeringCon_Connect_Rod_Adj_layout)
            row2_layout.addLayout(self.SteeringCon_Steering_Linkages_layout)

            row3_layout = QHBoxLayout()
            row3_layout.addLayout(self.SteeringCon_Steering_Pump_layout)

            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)
            group_layout.addLayout(row3_layout)

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 1)

            # # Store references to input fields
            self.SteeringCon_section_fields[title] = {
                f"SteeringCon_Stick_Lever_Shift": self.SteeringCon_Stick_Lever_Shift,
                f"SteeringCon_Stick_Play": self.SteeringCon_Stick_Play,
                f"SteeringCon_Connect_Rod_Adj": self.SteeringCon_Connect_Rod_Adj,
                f"SteeringCon_Steering_Linkages": self.SteeringCon_Steering_Linkages,
                f"SteeringCon_Steering_Pump": self.SteeringCon_Steering_Pump
            }


        def FuelSys_section(title, row, col):
            group_box = QGroupBox(title)
            group_layout = QVBoxLayout()

            combo_items = ["Svc", "Unsvc", "Ok", "Unsatisfactory", "Up", "Down", "Complete", "Incomplete"]

            self.FuelSys_Fuel_Filter_Cond_layout, self.FuelSys_Fuel_Filter_Cond = combo_input("Fuel Filter Cond", combo_items)
            self.FuelSys_Fuel_Lines_Leakage_layout, self.FuelSys_Fuel_Lines_Leakage = combo_input("Fuel Lines Leakage", combo_items)
            self.FuelSys_Fuel_Filter_Body_layout, self.FuelSys_Fuel_Filter_Body = combo_input("Fuel Filter Body", combo_items)
            self.FuelSys_Fuel_Tk_Strainer_layout, self.FuelSys_Fuel_Tk_Strainer = combo_input("Fuel Tk Strainer", combo_items)
            self.FuelSys_Fuel_Guage_layout, self.FuelSys_Fuel_Guage = combo_input("Fuel Guage", combo_items)
            self.FuelSys_Fuel_Distr_Cork_layout, self.FuelSys_Fuel_Distr_Cork = combo_input("Fuel Distr Cork", combo_items)
            self.FuelSys_Fuel_Tk_Cap_layout, self.FuelSys_Fuel_Tk_Cap = combo_input("Fuel Tk Cap", combo_items)
            self.FuelSys_Tk_Inner_Cond_layout, self.FuelSys_Tk_Inner_Cond = combo_input("Tk Inner Cond", combo_items)
            
            row1_layout = QHBoxLayout()
            row1_layout.addLayout(self.FuelSys_Fuel_Filter_Cond_layout)
            row1_layout.addLayout(self.FuelSys_Fuel_Lines_Leakage_layout)
            row1_layout.addLayout(self.FuelSys_Fuel_Filter_Body_layout)
            row1_layout.addLayout(self.FuelSys_Fuel_Tk_Strainer_layout)

            row2_layout = QHBoxLayout()
            row2_layout.addLayout(self.FuelSys_Fuel_Guage_layout)
            row2_layout.addLayout(self.FuelSys_Fuel_Distr_Cork_layout)
            row2_layout.addLayout(self.FuelSys_Fuel_Tk_Cap_layout)
            row2_layout.addLayout(self.FuelSys_Tk_Inner_Cond_layout)

            # Add rows to the group layout
            group_layout.addLayout(row1_layout)
            group_layout.addLayout(row2_layout)        

            group_box.setLayout(group_layout)
            form_layout.addWidget(group_box, row, col, 1, 4)
            # form_layout.addWidget(group_box, row, col)

            # Store references to input fields
            self.FuelSys_section_fields[title] = {
                f"FuelSys_Fuel_Filter_Cond": self.FuelSys_Fuel_Filter_Cond,
                f"FuelSys_Fuel_Lines_Leakage": self.FuelSys_Fuel_Lines_Leakage,
                f"FuelSys_Fuel_Filter_Body": self.FuelSys_Fuel_Filter_Body,
                f"FuelSys_Fuel_Tk_Strainer": self.FuelSys_Fuel_Tk_Strainer,
                f"FuelSys_Fuel_Guage": self.FuelSys_Fuel_Guage,
                f"FuelSys_Fuel_Distr_Cork": self.FuelSys_Fuel_Distr_Cork,
                f"FuelSys_Fuel_Tk_Cap": self.FuelSys_Fuel_Tk_Cap,
                f"FuelSys_Tk_Inner_Cond": self.FuelSys_Tk_Inner_Cond
            }


        # Maintenance Sections
        add_basic_section("Basic Details", 0, 0)
        Cooling_Section("Cooling Sys", 0, 1)
        HydRamp_Section("Hyd Ramp", 0, 2)
        LubSys_Section("Lub Sys", 2, 0)
        TrSys_Section("Tr Sys", 2, 1)
        BtyAssys_section("Bty & Assys", 2, 2)
        BoggyWh_Section("Boggy Wh", 4, 0)
        BrkSys_Section("Brk Sys", 4, 2)
        ElecSys_Section("Elec Sys", 6, 0)
        AirIntakeSys_Section("Air Intake Sys", 8, 0)
        TxSys_Section("Tx Sys", 8, 1)
        SteeringCon_section("Steering Con", 8, 2)
        FuelSys_section("Fuel Sys", 10, 0)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(" Save")
        save_button.setIcon(QIcon(get_asset_path("assets/icons/save.png")))
        save_button.setIconSize(QSize(20, 20))
        save_button.clicked.connect(self.save_a_vehicle_fit)

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


    def save_a_vehicle_fit(self):
        """ Inserts user into the database """
        add_a_vehicle_fit_data = {}

        required_fields = ['ba_no_input', 'make_input', 'type_input','CI_input', 'In_Svc_input']
        if not all(self.basic_details['Basic Details'][field].text().strip() for field in required_fields):
            QMessageBox.warning(self, "Error", "Basic Details required!")
            return

        field_categories = [
            self.add_basic_section_fields, self.Cooling_Section_fields, self.HydRamp_Section_fields,
            self.LubSys_Section_fields, self.TrSys_Section_fields, self.BtyAssys_section_fields,
            self.BoggyWh_Section_fields, self.BrkSys_Section_fields, self.ElecSys_Section_fields,
            self.AirIntakeSys_Section_fields, self.TxSys_Section_fields, self.SteeringCon_section_fields,
            self.FuelSys_section_fields
        ]

        for category in field_categories:
            for fields in category.values():
                for key, widget in fields.items():
                    if isinstance(widget, QLineEdit):
                        add_a_vehicle_fit_data[key] = widget.text().strip()
                    elif isinstance(widget, QComboBox):
                        selected_text = widget.currentText().strip()
                        add_a_vehicle_fit_data[key] = None if selected_text == "--Select--" else selected_text

        
        add_a_vehicle_fit_data['created_by'] = self.user_id

        is_data_inserted = self.db_obj.insert_a_vehicle_fit(add_a_vehicle_fit_data)
        if not is_data_inserted:
            QMessageBox.warning(self, "Failed", "Error while saving the data..! Please Try Again")
            return
        else:
            QMessageBox.information(self, "Success", "Vehicle added successfully!")
            return
       
        
    def clear_fields(self):
        pass