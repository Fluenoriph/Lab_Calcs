import sys
from PyQt6 import QtWidgets, QtCore, QtGui
import application_components
import constants
from application_classes import ResultField


class ApplicationType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная система")
        self.resize(1050, 600)
        self.move(self.width() * -2, 0)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()

        self.main_menu_area = application_components.MainMenu(self)
        self.app_object = LabSystemObject(self)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.box.addWidget(self.main_menu_area, QtCore.Qt.AlignmentFlag.AlignTop)
        self.box.addWidget(self.app_object, constants.ALIGNMENT_TOP_LEFT)

        self.setStyleSheet("font: 13px arial, sans-serif")

        self.show()


class LabSystemObject(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #fixedsize
        self.box = QtWidgets.QGridLayout(self)

        self.selector_area = application_components.SelectorPanel(self)
        self.main_work_area = application_components.CalculatorObjectManipulator(self)
        self.result_area = ResultField(self)
        self.control_area = application_components.MainControlField(self)

        self.box.addWidget(self.selector_area, 0, 0, 2, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.main_work_area, 0, 1, 1, 1)
        self.box.addWidget(self.result_area, 1, 1, 1, 1)
        self.box.addWidget(self.control_area, 0, 2, 2, 1)

        self.control_area.button_ok.clicked.connect(self.main_work_area.set_calculate_slot)











