from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from app_classes import StyledFrame
from calc_objects import CalcSelector


class ApplicationWindow(QtWidgets.QWidget):
    DARK_COLORS = ("#151719;", "#C0C0C0;", "#404d59;", "#CCCC99;", "#2f353b;", "#008B8B;", "#293133;",
                   "#00CED1;", "#1b1116;", "#00CC99;", "#191c16;", "#DB7093;")

    LIGHT_COLORS = ("#f8f8ff;", "#131313;", "#badbad;", "#464544;", "#f5f5f5;", "#121111;", "#f8f4ff;",
                    "#1e1e1e;", "#bde0ff;", "#26231c;", "#fdeaa8;", "#302112;")

    COLOR_COLORS = ("#013a33;", "#ffa343;", "#9f2b68;", "#1974d2;", "#ffa420;", "#93aa00;", "#1e90ff;",
                    "#ccff00;", "#7fffd4;", "#6a5acd;", "#dda0dd;", "#9400d3;")

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
        box = QtWidgets.QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.main_menu)
        box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.selector_frame = StyledFrame(self)
        self.selector_frame.setGeometry(5, 35, 225, 600)
        self.calc_frame = StyledFrame(self)
        self.calc_frame.setGeometry(245, 35, 1035, 600)

        self.set_light_style()

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
        submenu_edit = QtWidgets.QMenu("Правка", main_menu)
        submenu_view = QtWidgets.QMenu("Вид", main_menu)
        submenu_help = QtWidgets.QMenu("Справка", main_menu)

        calc_air = QtGui.QAction("Калькулятор пыль", submenu_file)
        calc_air.triggered.connect(CalcSelector.select_air_calc)
        submenu_file.addAction(calc_air)

        themes = submenu_view.addMenu("Тема")
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
        main_menu.addMenu(submenu_edit)
        main_menu.addMenu(submenu_view)
        main_menu.addMenu(submenu_help)
        main_menu.show()
        return frame


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("calc_type.ico"))
    app_window = ApplicationWindow()
    sys.exit(app.exec())
