from PyQt5.QtWidgets import (
    QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QGroupBox, QApplication
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
import sys

class AVehicleReportView(QWidget):
    def __init__(self, data=None, main_header=None, parent=None):
        super().__init__(parent)

        self.data = data if data else {}
        self.main_header = main_header if main_header else {}
        
        self.setWindowTitle("Vehicle Fitness Check Report")
        self.setMinimumSize(1000, 800)  # Adjust as needed

        # Main layout is a scroll area so large content can scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(10, 10,  10, 10)
        self.main_layout.setSpacing(15)

        # 1) Title / Header
        self.create_title_header()

        # 2) VEH BASIC INFO Section
        self.create_basic_info_section()

        # 3) VEH FITNESS CHECK Section
        self.create_fitness_check_section()

        # 4) FITNESS REPORT Section
        self.create_fitness_report_section()

        # Add a stretch at the end
        self.main_layout.addStretch()

        scroll.setWidget(container)

        # Set main layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def create_title_header(self):
        title_label = QLabel("A VEH FITNESS CHECK MODULE")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""background-color: #2E86C1; color: white; font-size: 24px; font-weight: bold; padding: 12px; border-radius: 4px;""")
        self.main_layout.addWidget(title_label)

    def create_basic_info_section(self):
        basic_info_group = QGroupBox("VEH BASIC INFO")
        basic_info_group.setStyleSheet("""
            QGroupBox {background-color: #AED6F1; font-weight: bold; border: 2px solid #2E86C1; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #154360;}
        """)
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # For each item in Basic Details, create a mini-box with label + value
        basic_details = self.main_header.get("Basic Details", [])
        for field in basic_details:
            value = self.data.get(field, "")
            field_widget = self.create_field_widget(field, value)
            layout.addWidget(field_widget)

        basic_info_group.setLayout(layout)
        self.main_layout.addWidget(basic_info_group)

    def create_fitness_check_section(self):
        """
        Creates the big "VEH FITNESS CHECK" area with sub-sections
        (Cooling Sys, Hyd Ramp, Lub Sys, etc.)
        """
        fitness_group = QGroupBox("VEH FITNESS CHECK")
        fitness_group.setStyleSheet("""
            QGroupBox { background-color: #FAD7A0; font-weight: bold; border: 2px solid #DC7633; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #6E2C00; }
        """)
        # We can use a grid layout or flow-like layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)

        # We want to skip "Basic Details" and "Creation Details" 
        # because they go in other sections
        exclude_sections = ["Basic Details", "Creation Details"]
        categories = [cat for cat in self.main_header.keys() if cat not in exclude_sections]

        # We'll place them in rows & columns. Adjust to your preference:
        # for example, 3 columns of sub-group boxes
        row = 0
        col = 0
        max_columns = 3 

        for cat in categories:
            sub_group = self.create_sub_section(cat, self.main_header[cat])
            grid.addWidget(sub_group, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        fitness_group.setLayout(grid)
        self.main_layout.addWidget(fitness_group)

    def create_sub_section(self, title, fields):
        """
        Creates a sub group box for each category (e.g. "Cooling Sys")
        containing a vertical list or small grid of the items + status
        """
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox { background-color: #FCF3CF; font-weight: normal; border: 1px solid #B7950B; border-radius: 3px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #7D6608; }
        """)

        # Use a simple grid or vertical layout for the fields
        layout = QGridLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 10, 5, 10)

        row = 0
        for field in fields:
            value = self.data.get(field, "")
            # Field label
            lbl_field = QLabel(field)
            lbl_field.setStyleSheet("font-weight: bold;")

            # Value label with color-coded background for Svc/Unsvc
            lbl_value = self.create_status_label(value)

            layout.addWidget(lbl_field, row, 0)
            layout.addWidget(lbl_value, row, 1)
            row += 1

        group_box.setLayout(layout)
        return group_box

    def create_status_label(self, value):
        """
        Returns a QLabel for the item value, color-coded for Svc/Unsvc/None
        """
        lbl = QLabel(str(value))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedWidth(80)

        # Color-code based on value
        if value == "Svc":
            lbl.setStyleSheet("background-color: #ABEBC6; color: black; border: 1px solid #58D68D;")
        elif value == "Unsvc":
            lbl.setStyleSheet("background-color: #F5B7B1; color: black; border: 1px solid #EC7063;")
        else:
            # For None or empty, just gray out
            lbl.setStyleSheet("background-color: #D5D8DC; color: black; border: 1px solid #BDC3C7;")

        return lbl

    def create_fitness_report_section(self):
        """
        Creates the "FITNESS REPORT" section at the bottom with dummy values
        (Overall Score, Total Tests, Fitness %, Download, etc.)
        """
        report_group = QGroupBox("FITNESS REPORT")
        report_group.setStyleSheet("""
            QGroupBox { background-color: #D6EAF8; font-weight: bold; border: 2px solid #5DADE2; border-radius: 5px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;  padding: 0 3px; color: #1B4F72; }
        """)
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # Dummy data: "Overall Score: 120 / 166", "Total Tests: 13", etc.
        # You can style these similarly as needed
        dummy_labels = [
            "Overall Score: 120 / 166",
            "Total Tests: 13",
            "Fitness %: 72%",
            "Download: PDF | Excel",
            "Edit/Update: Veh Summary"
        ]

        for text in dummy_labels:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size: 14px; font-weight: normal;")
            layout.addWidget(lbl)

        report_group.setLayout(layout)
        self.main_layout.addWidget(report_group)

    def create_field_widget(self, label_text, value_text):
        """
        A helper to create a small VBox with label on top and the value below
        to mimic the "BA NO" -> "5465" style from the Basic Info section
        """
        w = QWidget()
        vbox = QVBoxLayout(w)
        vbox.setSpacing(5)
        vbox.setContentsMargins(0, 0, 0, 0)

        lbl_field = QLabel(label_text)
        lbl_field.setAlignment(Qt.AlignCenter)
        lbl_field.setStyleSheet(""" background-color: #F4D03F; color: #1B2631; font-weight: bold; border: 1px solid #B7950B; border-radius: 3px; padding: 5px; """)

        lbl_value = QLabel(str(value_text))
        lbl_value.setAlignment(Qt.AlignCenter)
        lbl_value.setStyleSheet(""" background-color: #FDEBD0; color: #1B2631; font-weight: normal; border: 1px solid #B7950B; border-radius: 3px; padding: 5px; """)

        vbox.addWidget(lbl_field)
        vbox.addWidget(lbl_value)
        return w


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Sample data
    data = {
        'BA NO': '5465', 'Make': '5465', 'Type': '4654', 'CI': '6546', 'In Svc': '54654',
        'Fins': 'Svc', 'Rad Paint': 'Svc', 'Coolant': 'Unsvc', 'Leakage': 'Svc',
        'Rad Cap': 'Svc', 'Fan Belt': 'Svc', 'Hyd Oil Lvl': 'Svc', 'TGS Oil Lvl': 'Unsvc',
        'Tx Oil': 'Svc', 'Tx Filter': 'Svc', 'Fan Mech Oil': 'Svc', 'Eng Oil': 'Svc',
        'EO Cond': 'Svc', 'Oil Sump': 'Svc', 'Oil Grade': 'Svc', 'Lub': 'Svc',
        'Tr Chain Adj': 'Svc', 'Tr Chain Play': 'Svc', 'Tr Pin Adj': 'Svc', 
        'Tr Pad Thickness': 'Svc', 'Sproket Wh Life': 'Svc', 'Tr Tensioner': None, 
        'Cradle Fitting': 'Svc', 'Electolyte Lvl': 'Svc', 'Terminals': 'Unsvc', 
        'Mineral Jelly': 'Svc', 'Vent Plug': 'Svc', 'Bty Ser (LB)': 'Svc', 
        'Rubber Cond': 'Svc', 'Lub Pts': 'Svc', 'Inner / Outer Bearing': 'Unsvc',
        'Brk Fluid': 'Svc', 'Brk Lever': 'Svc', 'Ign Sw': 'Unsvc', 
        'Water Temp Guage': 'Svc', 'Fuse Box': 'Svc', 'Fuse Svc': 'Svc', 
        'Oil Pressure Guage': 'Svc', 'RPM Guage': 'Svc', 'Oil Temp Guage': 'Unsvc', 
        'Self-Starter Motor': 'Svc', 'Alternator Func': 'Svc', 'Fuel Guage': 'Svc', 
        'Electric Harness': 'Svc', 'Alternator Fan Belt': 'Svc', 
        'Alternator Noise': 'Unsvc', 'Horn': 'Svc', 'Blower Heater': 'Svc', 
        'Air Cleaner Cond': 'Svc', 'Air Cleaner Seal': 'Svc', 'Hoses & Valves': 'Svc', 
        'Bluge Pump': 'Svc', 'BP Dust Cover': 'Svc', 'Hyd Oil Lvl Check': 'Unsvc', 
        'TGC Lvl Check': 'Svc', 'TGC Oil Cond': 'Svc', 'Stall Test': 'Svc', 
        'Steering Planetary Gear': 'Svc', 'Final Drive Func': 'Svc', 
        'Tx Oil Lvl': 'Svc', 'Tx Oil Cond': 'Svc', 'Stick Lever Shift': 'Unsvc', 
        'Stick Play': 'Svc', 'Connect Rod Adj': 'Svc', 'Steering Linkages': 'Svc', 
        'Steering Pump': 'Svc', 'Fuel Filter Cond': 'Svc', 'Fuel Lines Leakage': 'Svc', 
        'Fuel Filter Body': 'Svc', 'Fuel Tk Strainer': 'Svc', 'Fuel Distr Cork': 'Svc', 
        'Fuel Tk Cap': 'Svc', 'Tk Inner Cond': 'Svc', 'Created By': 'Zahid Hameed', 
        'Created At': '2025-02-20 07:43:32', 'id': 1
    }

    main_header = {
        "Basic Details": ["BA NO", "Make", "Type", "CI", "In Svc"],
        "Cooling Sys": ["Fins", "Rad Paint", "Coolant", "Leakage", "Rad Cap", "Fan Belt"],
        "Hyd Ramp": ["Hyd Oil Lvl", "TGS Oil Lvl", "Tx Oil", "Tx Filter", "Fan Mech Oil"],
        "Lub Sys": ["Eng Oil", "EO Cond", "Oil Sump", "Leakage", "Oil Grade", "Lub"],
        "Tr Sys": ["Tr Chain Adj", "Tr Chain Play", "Tr Pin Adj", "Tr Pad Thickness", 
                   "Sproket Wh Life", "Tr Tensioner"],
        "Bty & Assys": ["Cradle Fitting", "Electolyte Lvl", "Terminals", 
                        "Mineral Jelly", "Vent Plug", "Bty Ser (LB)"],
        "Boggy Wh": ["Rubber Cond", "Lub Pts", "Inner / Outer Bearing"],
        "Brk Sys": ["Brk Fluid", "Brk Lever"],
        "Elec Sys": ["Ign Sw", "Water Temp Guage", "Fuse Box", "Fuse Svc", 
                     "Oil Pressure Guage", "RPM Guage", "Oil Temp Guage", 
                     "Self-Starter Motor", "Alternator Func", "Fuel Guage", 
                     "Electric Harness", "Alternator Fan Belt", "Alternator Noise", 
                     "Horn", "Blower Heater"],
        "Air Intake Sys": ["Air Cleaner Cond", "Air Cleaner Seal", "Hoses & Valves", 
                           "Bluge Pump", "BP Dust Cover", "Hyd Oil Lvl Check", 
                           "TGC Lvl Check", "TGC Oil Cond"],
        "Tx Sys": ["Stall Test", "Steering Planetary Gear", "Final Drive Func", 
                   "Tx Oil Lvl", "Tx Oil Cond"],
        "Steering Con": ["Stick Lever Shift", "Stick Play", "Connect Rod Adj", 
                         "Steering Linkages", "Steering Pump"],
        "Fuel Sys": ["Fuel Filter Cond", "Fuel Lines Leakage", "Fuel Filter Body", 
                     "Fuel Tk Strainer", "Fuel Guage", "Fuel Distr Cork", 
                     "Fuel Tk Cap", "Tk Inner Cond"],
        "Creation Details": ["Created By", "Created At"]
    }

    window = AVehicleReportView(data=data, main_header=main_header)
    window.show()
    sys.exit(app.exec_())
