import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
from calculators_objects import


class ApplicationType(QtWidgets.QMainWindow):
    def __init__(self, calc_frame=None, selector_frame=None):
        super().__init__()
        self.calc_frame = calc_frame
        self.selector_frame = selector_frame

        self.setWindowTitle("Калькуляторы")
        self.resize(1285, 670)
        self.move(self.width() * -2, 0)
        self.setWindowOpacity(0.98)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()
        self.show()

        self.create_main_menu()
        self.create_selector_frame()
        self.create_calc_frame()
        CalcSelector(self.selector_frame, self.calc_frame)

        self.set_app_style(ApplicationWindow.LIGHT_COLORS)

    @QtCore.pyqtSlot()
    def open_about_message(self):
        QtWidgets.QMessageBox.about(self, "О программе", "Калькулятор Лабораторный 2.0\n\n"
                                    "Свободное ПО с окрытым исходным кодом\n\nИван Богданов, 2024\n"
                                                         "fluenoriph@gmail.com")

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, "Справка", ApplicationWindow.HELP_INFO)

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        submenu_file = QtWidgets.QMenu("Файл", main_menu)
        submenu_view = QtWidgets.QMenu("Вид", main_menu)
        submenu_help = QtWidgets.QMenu("Помощь", main_menu)
        main_menu.addMenu(submenu_file)
        main_menu.addMenu(submenu_view)
        main_menu.addMenu(submenu_help)
        main_menu.show()

        exit_programm = QtGui.QAction("Выход", submenu_file)
        exit_programm.triggered.connect(sys.exit)
        submenu_file.addAction(exit_programm)

        themes = submenu_view.addMenu("Темы")
        dark_style = QtGui.QAction("Темная", themes)
        dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        light_style = QtGui.QAction("Светлая", themes)
        light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))
        themes.addAction(dark_style)
        themes.addSeparator()
        themes.addAction(light_style)

        link = QtGui.QAction("Справка", submenu_help)
        link.triggered.connect(self.open_help_message)
        about = QtGui.QAction("О программе", submenu_help)
        about.triggered.connect(self.open_about_message)

        submenu_help.addAction(link)
        submenu_help.addSeparator()
        submenu_help.addAction(about)

    def create_selector_frame(self):
        self.selector_frame = QtWidgets.QWidget(self)
        self.selector_frame.setGeometry(5, 35, 225, 600)
        self.selector_frame.show()

    def create_calc_frame(self):
        self.calc_frame = QtWidgets.QWidget(self)
        self.calc_frame.setGeometry(245, 35, 1035, 600)
        self.calc_frame.show()

    @QtCore.pyqtSlot()
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
                                      colors_list[9] + "}")


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
        self.resize(220, 160)
        self.show()

        self.index_calculators = self.model_type.index(0, 0)


        self.select_list.activated.connect(self.click_air_calc)
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
            self.noise_calc.show()

