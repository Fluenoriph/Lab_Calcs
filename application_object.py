from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import sys
from winpath import get_desktop
import constants as ct
from calculators_objects import (AtmosphericAirDust, VentilationEfficiency, NoiseLevelsWithBackground, MainRegister,
                                 FactorsRegister, AbstractBaseCalc as calc_base, AbstractRegister as ar)


class BaseAbstractController(QtWidgets.QWidget):
    def __init__(self, calcs_names, calcs_objects, icon_path, tooltips):
        super().__init__()
        self.calcs_names = calcs_names
        self.calcs_objects = calcs_objects
        self.icon_path = icon_path
        self.tooltips = tooltips

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])

        self.calcs_area = self.create_options()
        self.setFixedSize(1200, 1000)        # dynamics

        self.buttons = self.create_control_buttons()

    def create_options(self):
        area = QtWidgets.QTabWidget(self)
        area.setCurrentIndex(0)
        area.setUsesScrollButtons(False)

        y = self.box.columnCount()
        x = len(self.calcs_names)
        if x == 2:
            y = 2

        [area.addTab(self.calcs_objects[_], self.calcs_names[_]) for _ in range(x)]
        self.box.addWidget(area, 0, y, 8, 1, alignment=ct.data_library["Позиция левый-верхний"])
        return area

    def create_control_buttons(self):
        buttons = []
        self.box.setColumnStretch(self.box.columnCount(), 50)
        x = self.box.columnCount()

        for _ in range(3):
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(self.icon_path[_]))
            button.setToolTip(self.tooltips[_])
            button.setToolTipDuration(3000)
            button.setIconSize(ct.data_library["Размеры кнопок"])
            button.setAutoDefault(True)
            buttons.append(button)
            self.box.addWidget(button, _ + 1, x, 3, 1, ct.data_library["Позиция левый-верхний"])
        return buttons

class RegistersController(BaseAbstractController):
    n = list(ct.data_library["Журналы"].keys())

    def __init__(self):
        super().__init__(self.n[1:3],(FactorsRegister(),
        FactorsRegister(ct.data_library["Журналы"]["Радиационные факторы"]["Параметры"])),
        ct.data_library["Элементы управления"]["Иконки журнала"], ct.data_library["Элементы управления"]["Подсказки журнала"])

        self.box.setHorizontalSpacing(50)  # dyn
        self.register = MainRegister()
        self.box.addWidget(self.register, 0, 0, 8, 2, alignment=ct.data_library["Позиция левый-верхний"])

        self.calcs_area.currentChanged.connect(self.clear_number_to_move)

        self.buttons[0].clicked.connect(self.save_protocol)
        self.buttons[1].clicked.connect(self.clear_fields)
        self.buttons[2].clicked.connect(self.run_protocols_view)

    def record_main_data(self):
        x = QtSql.QSqlQuery()
        y = self.calcs_area.currentIndex()

        protocol_data = [_.text() for _ in self.register.entry_objects[:6]]
        [protocol_data.append(_.itemData(_.currentIndex())) for _ in self.register.entry_objects[6:]]

        x.prepare(f"INSERT INTO {ct.data_library["Журналы"]["Основной регистратор"]["Тип журнала"][y]} "
                  f"VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)")
        [x.addBindValue(_) for _ in protocol_data]
        return x.exec()

    def record_factors_data(self):
        n = self.calcs_area.currentIndex()       # refactor all  в функции ?
        x = QtSql.QSqlQuery()

        for i in range(self.calcs_objects[n].sum):
            x.prepare(f"INSERT INTO {ct.data_library["Журналы"][self.calcs_names[n]]["Таблицы"][i]} VALUES(NULL, ?, ?)")
            [x.addBindValue(self.calcs_objects[n].entry_objects[_][i].value()) for _ in range(2)]
            if not x.exec():
                return ar.error_message(self, 1)

    @QtCore.pyqtSlot()
    def save_protocol(self):
        n = self.calcs_area.currentIndex()
        x = [i for i, x in enumerate(self.calcs_objects[n].entry_objects[0]) if x.value() > 0]

        if (self.register.entry_objects[0].text() == "" or [i for i, x in enumerate(self.register.entry_objects[3:6]) if x.text() == ""]
                or [i for i, x in enumerate(self.register.entry_objects[6:]) if x.currentIndex() == 0] or not x or
                [i for i in x if self.calcs_objects[n].entry_objects[0][i].value()
                                             < self.calcs_objects[n].entry_objects[1][i].value()]):
            return ar.error_message(self, 0)
        else:
            if self.record_main_data():
                self.record_factors_data()
            else:
                return ar.error_message(self, 1)

    @QtCore.pyqtSlot()
    def clear_fields(self):
        [_.clear() for _ in self.register.entry_objects[:6]]
        [_.setCurrentIndex(0) for _ in self.register.entry_objects[6:]]

        for _ in range(2):
            [j.clear() for i in self.calcs_objects[_].entry_objects for j in i]
            [j.setValue(0) for i in self.calcs_objects[_].entry_objects for j in i]

    @QtCore.pyqtSlot()
    def clear_number_to_move(self):
        return self.register.entry_objects[0].clear()

    @QtCore.pyqtSlot()
    def run_protocols_view(self):
        i = self.calcs_area.currentIndex()
        d = ct.data_library["Журналы"][self.calcs_names[i]]["Столбцы"]
        x = QtCore.Qt.Orientation.Horizontal  # in dict
        n = self.calcs_objects[i].sum * 2 # ??

        view_type = QtWidgets.QTableView(self)
        view_type.setWindowFlags(QtCore.Qt.WindowType.Window)
        view_type.resize(1400, 600) # ????
        header = view_type.horizontalHeader()
        view_type.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        view_type.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        view_type.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        view_type.setWordWrap(True)

        data_model = QtSql.QSqlTableModel()
        data_model.setTable(ct.data_library["Журналы"]["Представления"][i])
        data_model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        data_model.select()
        view_type.setModel(data_model)

        [data_model.setHeaderData(_, x, ct.data_library["Журналы"]["Основной регистратор"]["Столбцы"][_]) for _ in range(7)]
        [data_model.setHeaderData(_ + 7, x, d[_]) for _ in range(n)]
        data_model.setHeaderData(n + 7, x, "Ф.И.О. ответс.")

        header.resizeSection(0, 60)
        [header.resizeSection(_, 70) for _ in (1, 2, 6)]
        header.resizeSection(3, 180)
        [header.resizeSection(_, 100) for _ in (4, n + 7)]
        header.resizeSection(5, 200)
        [header.resizeSection(_ + 7, 60) for _ in range(n)]

        view_type.setWindowTitle(self.calcs_names[i])
        view_type.show()


class CalculatorsController(BaseAbstractController):
    def __init__(self):
        super().__init__(list(ct.data_library["Калькуляторы"].keys()),
        (AtmosphericAirDust(), AtmosphericAirDust(ct.data_library["Калькуляторы"]["Пыль в воздухе рабочей зоны"]["Параметры"],
        ct.data_library["Калькуляторы"]["Пыль в воздухе рабочей зоны"]["Результаты"]), VentilationEfficiency(),
         NoiseLevelsWithBackground()), ct.data_library["Элементы управления"]["Иконки калькулятора"],
                         ct.data_library["Элементы управления"]["Подсказки калькулятора"])

        self.buttons[0].clicked.connect(self.calculating)
        self.buttons[1].clicked.connect(self.clearing)
        self.buttons[2].clicked.connect(self.saving)

        self.message = lambda: QtWidgets.QMessageBox.information(self, " ",
                                                                 f"{ct.data_library["Отчет"][4]}\'{ct.data_library["Отчет"][self.calcs_area.currentIndex()][1:]}\'")

    def ready_to_calculate_airs(self):
        calc = self.calcs_objects[self.calcs_area.currentIndex()]

        if [i for i, x in enumerate(calc.entry_objects) if x.text() == ""]:
            return
        else:
            calc.calculate()

    def clear_basic_calc(self):
        calc = self.calcs_objects[self.calcs_area.currentIndex()]

        [_.clear() for _ in calc.entry_objects]
        [calc_base.reset_value(_) for _ in calc.entry_objects]
        calc.result_area.clear()

    def save_basic_calc(self):
        calc = self.calcs_objects[self.calcs_area.currentIndex()]

        if calc.result_area.text() != "":
            data = [calc.parameters[_] + ': ' + calc.entry_objects[_].text() + '\n' for _ in range(len(calc.parameters))]
            data.append('\n' + calc.result_area.text() + ct.data_library["Отчет"][5])

            self.message()
            self.write_to_file(data)
        else:
            return

    def save_noise_calc(self):
        if self.calcs_objects[3].octave_table[3][0].text() != "":
            data = ["".ljust(23)]
            [data.append(_.ljust(8)) for _ in ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Октавные полосы"]]
            data.append('\n')
            data.append("".ljust(23))
            [data.append("----".ljust(8)) for _ in range(10)]
            data.append('\n')

            for n, i in enumerate(self.calcs_objects[3].octave_table):
                data.append(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Результаты"][n].ljust(23))
                [data.append(j.text().ljust(8)) for j in i]
                data.append('\n')
            data.append(ct.data_library["Отчет"][5])

            self.message()
            self.write_to_file(data)
        else:
            return

    def write_to_file(self, data):
        with open(get_desktop() + ct.data_library["Отчет"][self.calcs_area.currentIndex()], "a", encoding="utf-8") as txt:
            txt.writelines(data)

    @QtCore.pyqtSlot()
    def calculating(self):
        match self.calcs_area.currentIndex():
            case 2:
                if ([i for i, x in enumerate(self.calcs_objects[2].entry_objects[0:3]) if x.text() == ""] or
                        not self.calcs_objects[2].set_hole_checks()):
                    return
                else:
                    self.calcs_objects[2].calculate()
            case 3:
                self.calcs_objects[3].calculate()
            case _:
                self.ready_to_calculate_airs()

    @QtCore.pyqtSlot()
    def clearing(self):
        if self.calcs_area.currentIndex() == 3:
            [j.clear() for i in self.calcs_objects[3].octave_table for j in i]
            [calc_base.reset_value(j) for i in self.calcs_objects[3].octave_table for j in i]
        else:
            self.clear_basic_calc()

    @QtCore.pyqtSlot()
    def saving(self):
        if self.calcs_area.currentIndex() == 3:
            self.save_noise_calc()
        else:
            self.save_basic_calc()


class ApplicationType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings(QtCore.QSettings.Format.IniFormat, QtCore.QSettings.Scope.UserScope, "Ivan_Bogdanov",
                        "Calculators__2.1.0__Beta", self)
        self.data_dict_names = list(ct.data_library.keys())

        self.setWindowTitle("Калькуляторы")
        self.move(self.width() * -2, 0)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(0, 0, 0, 5)
        self.box.setColumnMinimumWidth(0, 1)

        self.menu_area = self.create_main_menu()
        self.selector_area = self.create_selector_panel()
        self.registers_area = RegistersController()
        self.calculators_area = CalculatorsController()

        self.box.addWidget(self.menu_area, 0, 0, 1, 4)
        for i, j in enumerate((self.selector_area, self.calculators_area)):
            self.box.addWidget(j, 1, i + 1, ct.data_library["Позиция левый-верхний"])

        self.current_style_value = self.settings.value("Style", 1)
        if int(self.current_style_value) == 1:
            self.set_style(ct.data_library["Цвета светлой темы"])
        else:
            self.set_style(ct.data_library["Цвета темной темы"])
            self.menu_area.change_style.toggle()

        self.show()

        self.selector_area.setFixedSize(150, self.height())

    def set_style(self, colors):
        self.setStyleSheet("* {outline: 0; border-style: none; background: "+colors[0]+" font: 13px arial, sans-serif;} "                                                  
             
             "QMenuBar, QMenu {background: "+colors[0]+" color: "+colors[2]+"} QLabel {color: "+colors[6]+"} "   
             "QMenuBar {border-bottom: 1px solid "+colors[2]+"} "
             "QMenuBar::item:selected {background: "+colors[3]+"} "
             "QMenu::separator {border-bottom: 1px solid "+colors[2]+"} "                                      
             "QMenu::item:selected {background: "+colors[3]+"} "    
                          
             "QToolTip {color: "+colors[2]+"} "
                                                        
             "QMessageBox QLabel {color: "+colors[2]+"} "
             "QMessageBox .QPushButton {border-radius: 5px; padding: 6px 16px 6px 16px; background: "+colors[3]+" color: "+colors[2]+"} "                             
             "QMessageBox .QPushButton:pressed {background: "+colors[4]+"}"    
             
             "QPushButton {border-radius: 9px; padding: 3px;} "
             "QPushButton:hover {background: "+colors[3]+"} "
             "QPushButton:pressed {background: "+colors[4]+"} "

             "QListView {border-radius: 9px; background: "+colors[1]+"} "       
             "QListView::item {border-radius: 5px; padding: 2px; color: "+colors[2]+"} "
             "QListView::item:hover {background: "+colors[3]+"} "
             "QListView::item:selected {background: " + colors[3] + " color: " + colors[4] + "}"

             "QTabWidget:pane {border-style: none;} "
             "QTabBar:tab {border-radius: 5px; padding: 5px; background: "+colors[9]+" color: "+colors[5]+"} "     
             "QTabBar:tab::hover {background: "+colors[3]+"} "
             "QTabBar:tab::selected {background: "+colors[3]+" color: "+colors[4]+"} "   
                                                                                                           
             "QLineEdit, QDateEdit, QSpinBox, QComboBox {border-radius: 5px; background: "+colors[7]+" color: "+colors[8]+"} "                                                           
             
             "QLineEdit:focus {background: "+colors[1]+"} "
             "QDateEdit:focus {background: "+colors[1]+"} "
             "QComboBox:selected {background: "+colors[1]+"} "
             "QSpinBox:focus {background: "+colors[1]+"} "          
                                                                                                                                                                               
             "QLabel#result_field {border-radius: 9px; background: "+colors[9]+" color: "+colors[10]+"} "
             "QLabel#result_field_noise {border-radius: 5px; background: "+colors[9]+" color: "+colors[10]+"}"
             
             "QTableView {font: 10px arial, sans-serif; background: blue;} "
             "QTableView::item:selected {background: red;} "
             "QTableView QHeaderView::section {border: 0px; font: 10px arial, sans-serif; background: "+colors[1]+"} "
             "QTableView QTableCornerButton::section {border: 0px; background: "+colors[1]+"} "
             "QTableView QScrollBar:horizontal {border: 0px; background: transparent;}"

                           )

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        main_menu.setFixedHeight(22)

        main_menu.submenu_file = QtWidgets.QMenu(ct.data_library["Главное меню"][0], main_menu)
        main_menu.submenu_help = QtWidgets.QMenu(ct.data_library["Главное меню"][2], main_menu)
        main_menu.change_style = QtGui.QAction(ct.data_library["Главное меню"][3], main_menu)
        main_menu.change_style.setCheckable(True)
        main_menu.change_style.toggled.connect(self.change_app_style)

        main_menu.addMenu(main_menu.submenu_file)
        main_menu.addMenu(main_menu.submenu_help)
        main_menu.addAction(main_menu.change_style)

        main_menu.set_calculators_act = QtGui.QAction(self.data_dict_names[24], main_menu.submenu_file)
        main_menu.set_calculators_act.triggered.connect(self.calculators_show_fixed)
        main_menu.set_registers_act = QtGui.QAction(self.data_dict_names[25], main_menu.submenu_file)
        main_menu.set_registers_act.triggered.connect(self.registers_show_fixed)
        main_menu.exit_act = QtGui.QAction(ct.data_library["Главное меню"][1], main_menu.submenu_file)
        main_menu.exit_act.triggered.connect(sys.exit)

        main_menu.submenu_file.addAction(main_menu.set_registers_act)
        main_menu.submenu_file.addAction(main_menu.set_calculators_act)
        main_menu.submenu_file.addSeparator()
        main_menu.submenu_file.addAction(main_menu.exit_act)

        main_menu.help_link = QtGui.QAction(self.data_dict_names[1], main_menu.submenu_help)
        main_menu.help_link.triggered.connect(self.open_help_message)

        main_menu.about = QtGui.QAction(self.data_dict_names[2], main_menu.submenu_help)
        main_menu.about.triggered.connect(self.open_about_app_message)

        main_menu.submenu_help.addAction(main_menu.help_link)
        main_menu.submenu_help.addSeparator()
        main_menu.submenu_help.addAction(main_menu.about)

        return main_menu

    def create_selector_panel(self):
        selector_panel = QtWidgets.QListView(self)
        selector_panel.setSpacing(10)

        selector_panel.names = (self.data_dict_names[24], self.data_dict_names[25])
        selector_panel.model_type = QtCore.QStringListModel(selector_panel.names)
        selector_panel.setModel(selector_panel.model_type)

        selector_panel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        selector_panel.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        selector_panel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        selector_panel.calculators_index = selector_panel.model_type.index(0, 0)
        selector_panel.registers_index = selector_panel.model_type.index(1, 0)
        selector_panel.clicked.connect(self.select_calcs_type)
        selector_panel.setCurrentIndex(selector_panel.calculators_index)

        return selector_panel

    @QtCore.pyqtSlot()
    def change_app_style(self):
        match self.menu_area.change_style.isChecked():
            case True:
                self.set_style(ct.data_library["Цвета темной темы"])
                self.settings.setValue(ct.data_library["Настройки"], 2)
                self.settings.sync()
            case False:
                self.set_style(ct.data_library["Цвета светлой темы"])
                self.settings.setValue(ct.data_library["Настройки"], 1)
                self.settings.sync()

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, self.data_dict_names[2], ct.data_library["О программе"])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, self.data_dict_names[1], ct.data_library["Справка"])

    @QtCore.pyqtSlot()
    def calculators_show_fixed(self):
        self.registers_area.close()
        self.box.replaceWidget(self.registers_area, self.calculators_area)
        self.calculators_area.show()

    @QtCore.pyqtSlot()
    def registers_show_fixed(self):
        self.calculators_area.close()
        self.box.replaceWidget(self.calculators_area, self.registers_area)
        self.registers_area.show()

    @QtCore.pyqtSlot()
    def select_calcs_type(self):
        match self.selector_area.currentIndex():    # refactor index !!!
            case self.selector_area.calculators_index:
                self.calculators_show_fixed()
            case self.selector_area.registers_index:
                self.registers_show_fixed()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("images/calc_logo.ico"))
    app_calcs = ApplicationType()
    sys.exit(app.exec())
