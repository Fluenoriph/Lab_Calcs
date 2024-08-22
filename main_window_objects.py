from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
from calc_objects import CalcAir, CalcZone, CalcFlow, CalcNoise


class ApplicationWindow(QtWidgets.QWidget):
    DARK_COLORS = ("#0a0a0a;", "#dbd7d2;", "#414a4c;", "#2c3337;", "#00bfff;", "#1a0000;", "#00b300;",
                   "#1c1c1c;", "#022027;", "#9d9101;")

    LIGHT_COLORS = ("#fcfcee;", "#18171c;", "#f5f5f5;", "#f0f8ff;", "#140f0b;", "#afeeee;", "#003399;",
                    "#e28090;", "#eedc82;", "#282828;")

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

        self.set_app_style(ApplicationWindow.DARK_COLORS)

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        submenu_file = QtWidgets.QMenu("Файл", main_menu)
        submenu_view = QtWidgets.QMenu("Вид", main_menu)
        submenu_help = QtWidgets.QMenu("Справка", main_menu)

        calc_air = QtGui.QAction("Выход", submenu_file)
        calc_air.triggered.connect(quit)
        submenu_file.addAction(calc_air)

        themes = submenu_view.addMenu("Темы")
        dark_style = QtGui.QAction("Темная", themes)
        dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        light_style = QtGui.QAction("Светлая", themes)
        light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))

        themes.addAction(dark_style)
        themes.addSeparator()
        themes.addAction(light_style)

        main_menu.addMenu(submenu_file)
        main_menu.addMenu(submenu_view)
        main_menu.addMenu(submenu_help)
        main_menu.show()

    def create_selector_frame(self):
        self.selector_frame = QtWidgets.QWidget(self)
        self.selector_frame.setGeometry(5, 35, 225, 600)
        self.selector_frame.show()

    def create_calc_frame(self):
        self.calc_frame = QtWidgets.QWidget(self)
        self.calc_frame.setGeometry(245, 35, 1035, 600)
        self.calc_frame.show()

    def set_app_style(self, colors_list):
        self.setStyleSheet("* {background-color: " + colors_list[0] + "font: 14px arial, sans-serif;} "
                           ".QListView {font: 12px arial, sans-serif;} QMenuBar, QMenu {font: 12px arial, sans-serif; "
                           "color: " + colors_list[1] + "}")

        self.selector_frame.setStyleSheet("background-color: " + colors_list[2] + "color: " + colors_list[1])

        self.calc_frame.setStyleSheet("* {background-color: " + colors_list[3] + "color: " + colors_list[4] +
                                      "} QLineEdit {background-color: " + colors_list[5] + "color: " + colors_list[6] +
                                      "} QPushButton {border-style: outset; border-radius: 7px; padding: 5px; "
                                      "background-color: " + colors_list[7] +
                                      "} QFrame>QFrame {background-color: " + colors_list[8] + "color: " +
                                      colors_list[9] + "}")


class CalcSelector(QtWidgets.QWidget):
    def __init__(self, parent, calc_parent):
        super().__init__(parent)
        self.calc_parent = calc_parent
        self.air_calc = CalcAir(self.calc_parent)
        self.zone_calc = CalcZone(self.calc_parent)
        self.flow_calc = CalcFlow(self.calc_parent)
        self.noise_calc = CalcNoise(self.calc_parent)

        self.list_names = ['Пыль в атмосферном воздухе', 'Пыль в воздухе рабочей зоны',
                           'Эффективность вентиляции', 'Учет влияния фонового шума']
        self.select_list = QtWidgets.QListView(self)
        self.model_type = QtCore.QStringListModel(self.list_names)
        self.select_list.setModel(self.model_type)
        self.select_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.select_list.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.select_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.select_list.setSpacing(10)
        self.select_list.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        self.select_list.setTabKeyNavigation(True)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.select_list, QtCore.Qt.AlignmentFlag.AlignTop)
        self.box.setContentsMargins(3, 5, 3, 3)
        self.resize(220, 160)
        self.show()

        self.index_air = self.model_type.index(0, 0)
        self.index_zone = self.model_type.index(1, 0)
        self.index_flow = self.model_type.index(2, 0)
        self.index_noise = self.model_type.index(3, 0)

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
