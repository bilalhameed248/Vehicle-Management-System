from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QVBoxLayout, QPushButton, QTableView, QHBoxLayout, QComboBox,
    QLineEdit, QHeaderView, QStyledItemDelegate, QHBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import QTimer, QSize

class UserFilterProxy(QSortFilterProxyModel):
    """ Custom filter to search multiple columns """
    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        
        name_index = model.index(source_row, 1, source_parent)
        username_index = model.index(source_row, 2, source_parent)
        blocked_index = model.index(source_row, 3, source_parent)

        name_text = model.data(name_index, Qt.DisplayRole)
        username_text = model.data(username_index, Qt.DisplayRole)
        blocked_text = model.data(blocked_index, Qt.DisplayRole)
        search_text = self.filterRegExp().pattern().lower()
        return any(search_text in str(text).lower() for text in (name_text, username_text, blocked_text))
    

class ButtonDelegate(QStyledItemDelegate):
    """ Custom delegate to add buttons inside QTableView """
    def paint(self, painter, option, index):
        pass  # Don't paint default text (we replace with buttons)

    def create_buttons(self, table, row):
        """ Creates a QWidget with buttons to be used in setIndexWidget """
        widget = QWidget(table)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        edit_button = QPushButton(" Edit")
        edit_button.setIcon(QIcon("assets/icons/edit_user.png"))
        edit_button.setIconSize(QSize(20, 20))
        edit_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px; padding: 4px;")
        edit_button.clicked.connect(lambda: table.parent().edit_user(row))

        delete_button = QPushButton(" Delete")
        delete_button.setIcon(QIcon("assets/icons/delete_user.png"))
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setStyleSheet("background-color: #dc3545; color: white; border-radius: 5px; padding: 4px;")
        delete_button.clicked.connect(lambda: table.parent().delete_user(row))

        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)
        return widget
    
    def setModelData(self, editor, model, index):
        """ Override to prevent default model updates """
        pass