import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
import constants
from application_classes import MainControlField
from calculators_objects import CalculatorObjectManipulator as CalcsArea


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

        self.main_menu_area = MainMenu(self)
        self.selector_area = SelectorPanel(self)
        self.main_area = CalcsArea(self)
        self.control_area = MainControlField(self)

        #self.control_area.button_ok.clicked.connect(AtmosphericAirDust.calculate)

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.box.addWidget(self.main_menu_area, 0, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignTop)
        self.box.addWidget(self.selector_area, 1, 0, constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.main_area, 1, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.control_area, 1, 2, constants.ALIGNMENT_LEFT_CENTER)

        self.setStyleSheet("font: 13px arial, sans-serif")

        self.show()



    '''@QtCore.pyqtSlot()
    def set_app_style(self, colors_list):
        self.setStyleSheet("* {background-color: " + colors_list[0] + "font: 14px arial, sans-serif; color: " +
                           colors_list[1] + "} QPushButton {background-color: " + colors_list[7] + "} "
                           ".QListView {font: 12px arial, sans-serif;} "
                           "QMenuBar, QMenu {font: 12px arial, sans-serif; color: " +
                           colors_list[1] + "}")

        self.selector_frame.setStyleSheet("background-color: " + colors_list[2] + "color: " + colors_list[1])

        self.calc_frame.setStyleSheet("* {background-color: " + colors_list[3] + "color: " + colors_list[4] +
                                      "} QLineEdit {background-color: " + colors_list[5] + "color: " + colors_list[6] +
                                      "} QPushButton {border-style: outset; border-radius: 7px; padding: 5px; "
                                      "background-color: " + colors_list[7] +
                                      "} QFrame>QFrame {background-color: " + colors_list[8] + "color: " +
                                      colors_list[9] + "}")'''


class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.submenu_file = QtWidgets.QMenu("Файл", self)
        self.submenu_view = QtWidgets.QMenu("Вид", self)
        self.submenu_help = QtWidgets.QMenu("Помощь", self)

        self.addMenu(self.submenu_file)
        self.addMenu(self.submenu_view)
        self.addMenu(self.submenu_help)
        self.show()

        self.exit_act = QtGui.QAction("Выход", self.submenu_file)
        self.exit_act.triggered.connect(sys.exit)
        self.submenu_file.addAction(self.exit_act)

        self.themes = self.submenu_view.addMenu("Темы")
        self.dark = QtGui.QAction("Темная", self.themes)
        #dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        self.light = QtGui.QAction("Светлая", self.themes)
        #light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))
        self.themes.addAction(self.dark)
        self.themes.addSeparator()
        self.themes.addAction(self.light)

        self.help_link = QtGui.QAction(constants.HELP_INFO_MESSAGE[0], self.submenu_help)
        self.help_link.triggered.connect(self.open_help_message)

        self.about = QtGui.QAction(constants.ABOUT_INFO_MESSAGE[0], self.submenu_help)
        self.about.triggered.connect(self.open_about_app_message)

        self.submenu_help.addAction(self.help_link)
        self.submenu_help.addSeparator()
        self.submenu_help.addAction(self.about)

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, constants.ABOUT_INFO_MESSAGE[0], constants.ABOUT_INFO_MESSAGE[1])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, constants.HELP_INFO_MESSAGE[0], constants.HELP_INFO_MESSAGE[1])


class SelectorPanel(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.names = ("Калькуляторы", "Журналы")

        self.model_type = QtCore.QStringListModel(self.names)
        self.selector_object = QtWidgets.QListView(self)
        self.selector_object.setModel(self.model_type)
        self.selector_object.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.selector_object.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.selector_object.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.selector_object.setSpacing(10)
        self.selector_object.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        self.selector_object.setTabKeyNavigation(True)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.selector_object, QtCore.Qt.AlignmentFlag.AlignTop)
        self.box.setContentsMargins(3, 5, 3, 3)
        self.setFixedSize(constants.SIZE_SELECTOR_AREA)
        self.show()

        self.calculators_index = self.model_type.index(0, 0)

        '''self.select_list.activated.connect(self.click_air_calc)
        self.select_list.activated.connect(self.click_zone_calc)
        self.select_list.activated.connect(self.click_flow_calc)
        self.select_list.activated.connect(self.click_noise_calc)


    @QtCore.pyqtSlot()
    def click_air_calc(self):
        if self.select_list.currentIndex() == self.index_air:
            for calc in (self.zone_calc, self.flow_calc, self.noise_calc):
                calc.close()
            self.air_calc.show()

    @QtCore.pyqtSlot()
    def click_zone_calc(self):
        if self.select_list.currentIndex() == self.index_zone:
            for calc in (self.air_calc, self.flow_calc, self.noise_calc):
                calc.close()
            self.zone_calc.show()

    @QtCore.pyqtSlot()
    def click_flow_calc(self):
        if self.select_list.currentIndex() == self.index_flow:
            for calc in (self.zone_calc, self.air_calc, self.noise_calc):
                calc.close()
            self.flow_calc.show()

    @QtCore.pyqtSlot()
    def click_noise_calc(self):
        if self.select_list.currentIndex() == self.index_noise:
            for calc in (self.zone_calc, self.flow_calc, self.air_calc):
                calc.close()
            self.noise_calc.show()'''


