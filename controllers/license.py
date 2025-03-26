from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys, platform, uuid, hashlib, wmi
from database import VMS_DB
from templates.welcome import WelcomePage
from controllers.load_assets import *

class License:
    def __init__(self):
        self.os_name = None
        self.mac_address = None
        self.motherboard_serial = None
        self.cpu_id = None
        self.disk_serial = None
        self.license_key = None
        self.activation_date = None
        self.expiration_date = None
        self.allowed_os = ["Windows"]


    def get_motherboard_serial_win(self):
        c = wmi.WMI()
        for board in c.Win32_BaseBoard():
            return board.SerialNumber

    def get_cpu_id_win(self):
        c = wmi.WMI()
        for processor in c.Win32_Processor():
            return processor.ProcessorId.strip()

    def get_disk_serial_win(self):
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            return disk.SerialNumber.strip()


    def process(self):
        self.os_name = platform.system()
        if self.os_name not in self.allowed_os:
            QMessageBox.warning(self, "Error", "App cannot be run on this OS.")
            return
        mac = uuid.getnode()
        self.mac_address ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
        if self.os_name == self.allowed_os[0]:
            self.motherboard_serial = self.get_motherboard_serial_win()
            self.cpu_id = self.cpu_id_win()
            self.disk_serial = self.get_disk_serial_win()

            hardware_string = f"{mac}{motherboard_serial}{cpu_id}{disk_serial}"
            hardware_hash = hashlib.sha256(hardware_string.encode()).hexdigest()
            return hardware_hash


if __name__ == "__main__":
    license_obj = License()
    license_obj.process()



