from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from controllers.load_assets import *

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()

        issue_layout = QVBoxLayout()
        issue_layout.addWidget(QLabel("Issue Date:"))

        issue_date = QDateEdit()
        issue_date.setCalendarPopup(True)
        issue_date.setDate(QDate.currentDate())
        issue_date.setMinimumDate(QDate.currentDate().addYears(-5))
        issue_date.setMaximumDate(QDate.currentDate().addYears(5))
        issue_date.setDisplayFormat("dd-MM-yyyy")

        calendar_icon_path = get_asset_path("assets/icons/calendar.png")

        # Apply Stylesheet with Calendar Icon
        issue_date.setStyleSheet(f"""
            QDateEdit {{ border: 2px solid #0078D7; border-radius: 5px; padding: 5px; background-color: white; font-size: 14px; }}
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; }}
            QDateEdit::drop-down {{ width: 20px; border: none; background: transparent; image: url({calendar_icon_path});}}
            QCalendarWidget QWidget {{ alternate-background-color: #f0f0f0; background-color: white; border-radius: 5px; }}
            QCalendarWidget QToolButton {{ color: white; background-color: #0078D7; border: none; padding: 5px; border-radius: 3px; }}
            QCalendarWidget QToolButton:hover {{ background-color: #005bb5; }}
            QCalendarWidget QTableView {{ selection-background-color: #0078D7; color: black; }}
            QCalendarWidget QHeaderView::section {{ background-color: #0078D7; color: white;}}
        """)

        issue_layout.addWidget(issue_date)
        self.setLayout(issue_layout)

app = QApplication([])
window = CalendarWidget()
window.show()
app.exec_()

