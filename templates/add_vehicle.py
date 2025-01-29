from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFormLayout, QLineEdit, QScrollArea, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem,QStackedWidget, QSizePolicy, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QColor, QFont, QIcon

class AddVehicle:

    def __init__(self):
        pass


    def add_new_vehicle(self):
        """Create the add new vehicle form."""
        # Create a QWidget to hold the form inside a scroll area
        form_container = QWidget()

        # Layout for the form
        form_layout = QFormLayout()

        # Vehicle Information Inputs
        self.vehicle_name_input = QLineEdit(self)
        self.vehicle_name_input.setPlaceholderText("Enter Vehicle Name")
        form_layout.addRow("Vehicle Name:", self.vehicle_name_input)

        self.vehicle_model_input = QLineEdit(self)
        self.vehicle_model_input.setPlaceholderText("Enter Vehicle Model")
        form_layout.addRow("Vehicle Model:", self.vehicle_model_input)

        self.registration_number_input = QLineEdit(self)
        self.registration_number_input.setPlaceholderText("Enter Registration Number")
        form_layout.addRow("Registration Number:", self.registration_number_input)

        self.manufacture_year_input = QLineEdit(self)
        self.manufacture_year_input.setPlaceholderText("Enter Manufacture Year")
        form_layout.addRow("Manufacture Year:", self.manufacture_year_input)

        self.vehicle_type_input = QLineEdit(self)
        self.vehicle_type_input.setPlaceholderText("Enter Vehicle Type")
        form_layout.addRow("Vehicle Type:", self.vehicle_type_input)

        # Add Save Record Button
        self.save_record_button = QPushButton("Save Record")
        self.save_record_button.clicked.connect(self.save_vehicle_record)
        form_layout.addRow(self.save_record_button)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Set the form container as the widget inside the scroll area
        form_container.setLayout(form_layout)
        scroll_area.setWidget(form_container)

        self.content_area.addWidget(scroll_area)  # Add scroll area to content area
        self.content_area.setCurrentWidget(scroll_area)  # Show the form (instead of the welcome message)