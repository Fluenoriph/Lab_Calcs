from PyQt6 import QtWidgets, QtCore, QtGui
from app_classes import StyledFrame
from calc_objects import CalcAir, CalcZone, CalcFlow, CalcNoise


class ApplicationWindow(QtWidgets.QWidget):
    DARK_COLORS = ("#151719;", "#C0C0C0;", "#404d59;", "#CCCC99;", "#2f353b;", "#008B8B;", "#293133;",
                   "#00CED1;", "#1b1116;", "#00CC99;", "#191c16;", "#DB7093;")

    LIGHT_COLORS = ("#f8f8ff;", "#131313;", "#badbad;", "#464544;", "#f5f5f5;", "#121111;", "#f8f4ff;",
                    "#1e1e1e;", "#bde0ff;", "#26231c;", "#fdeaa8;", "#302112;")

    COLOR_COLORS = ("#013a33;", "#ffa343;", "#465945;", "#efcdb8;", "#c04000;", "#93aa00;", "#1e90ff;",
                    "#ccff00;", "#7fffd4;", "#231a24;", "#dda0dd;", "#00008b;")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькуляторы")
        self.resize(1285, 700)
        self.move(self.width() * -2, 0)
        self.setWindowOpacity(0.98)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()
        self.show()

        self.main_menu = self.create_main_menu()
        self.main_menu.setFixedHeight(23)
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.addWidget(self.main_menu)
        self.box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.selector_frame = StyledFrame(self)
        self.selector_frame.setGeometry(5, 35, 225, 600)

        self.calc_frame = StyledFrame(self)
        self.calc_frame.setGeometry(245, 35, 1035, 600)
       # Шрифты !
        self.set_light_style()
        #self.setStyleSheet("* {border-style: solid; border-width: 1px;}")

        CalcSelector(self.selector_frame, self.calc_frame)

    def set_app_style(self, colors_list):
        self.setStyleSheet("background-color: " + colors_list[0])

        self.main_menu.setStyleSheet("* {background-color: " + colors_list[0] + " font: 12px arial; color: "
                                     + colors_list[1] + "}")

        self.selector_frame.setStyleSheet("QWidget>QListView {background-color: " + colors_list[4] +
                                          "font: 12px arial, sans-serif; color: " + colors_list[3] +
                                          "} QFrame {background-color: " + colors_list[4] +
                                          "} * {color: " + colors_list[5] + "}")

        self.calc_frame.setStyleSheet("* {background-color: " + colors_list[6] +
                                      "font: 14px arial, sans-serif; color: " + colors_list[7] +
                                      "} .QLineEdit {background-color: " + colors_list[8] + " color: " +
                                      colors_list[9] + "} .QWidget>QLabel, .QWidget {background-color: " +
                                      colors_list[10] + " color: " + colors_list[11] +
                                      "} .QPushButton {background-color: " + colors_list[2] + "}")

    @QtCore.pyqtSlot()
    def set_dark_style(self):
        self.set_app_style(ApplicationWindow.DARK_COLORS)

    @QtCore.pyqtSlot()
    def set_colors_style(self):
        self.set_app_style(ApplicationWindow.COLOR_COLORS)

    @QtCore.pyqtSlot()
    def set_light_style(self):
        self.set_app_style(ApplicationWindow.LIGHT_COLORS)

    def create_main_menu(self):
        frame = StyledFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        main_menu = QtWidgets.QMenuBar(frame)
        main_menu.move(1, 1)

        submenu_file = QtWidgets.QMenu("Файл", main_menu)
        submenu_view = QtWidgets.QMenu("Вид", main_menu)
        submenu_help = QtWidgets.QMenu("Справка", main_menu)

        calc_air = QtGui.QAction("Выход", submenu_file)
        calc_air.triggered.connect(quit)
        submenu_file.addAction(calc_air)

        themes = submenu_view.addMenu("Темы")
        dark_style = QtGui.QAction("Темная", themes)
        dark_style.triggered.connect(self.set_dark_style)
        light_style = QtGui.QAction("Светлая", themes)
        light_style.triggered.connect(self.set_light_style)
        color_style = QtGui.QAction("Цветная", themes)
        color_style.triggered.connect(self.set_colors_style)

        themes.addAction(dark_style)
        themes.addSeparator()
        themes.addAction(light_style)
        themes.addSeparator()
        themes.addAction(color_style)

        main_menu.addMenu(submenu_file)
        main_menu.addMenu(submenu_view)
        main_menu.addMenu(submenu_help)
        main_menu.show()
        return frame


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
