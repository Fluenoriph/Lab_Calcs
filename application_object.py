from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import sys
from winpath import get_desktop
from functools import partial
import constants as ct
from calculators_objects import (AtmosphericAirDust, VentilationEfficiency, NoiseLevelsWithBackground,
                                 AbstractBaseCalc as cb, Factors)


class ProtocolView(QtWidgets.QTableView):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.name = name
        self.factor_titles = ct.data_library["Журналы"][self.name]["Столбцы"]
        self.n = len(self.factor_titles)

        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setWindowTitle(self.name)
        self.resize(ct.data_library["Размер представления"])

        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setWordWrap(True)
        self.verticalHeader().hide()

        self.data_model = QtSql.QSqlTableModel(self)
        self.data_model.setTable(ct.data_library["Журналы"][self.name]["Представление"])
        self.data_model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.data_model.select()
        self.setModel(self.data_model)

        [self.data_model.setHeaderData(_, ct.data_library["Ориентация"], ct.data_library["Журналы"]["Основной регистратор"]["Столбцы"][_]) for _ in
         range(7)]
        [self.data_model.setHeaderData(_ + 7, ct.data_library["Ориентация"], self.factor_titles[_]) for _ in range(self.n)]
        self.data_model.setHeaderData(self.n + 7, ct.data_library["Ориентация"], "Ф.И.О. ответс.")

        self.horizontalHeader().setDefaultAlignment(ct.data_library["Позиция левый-центр"])
        self.horizontalHeader().setMinimumSectionSize(70)
        self.horizontalHeader().resizeSection(0, 70)
        [self.horizontalHeader().resizeSection(_, 80) for _ in (1, 2, 6)]
        self.horizontalHeader().resizeSection(3, 200)
        [self.horizontalHeader().resizeSection(_, 150) for _ in (4, self.n + 7)]
        self.horizontalHeader().resizeSection(5, 250)

        for _ in range(self.n):
            self.horizontalHeader().resizeSection(_ + 7, 70)
            self.horizontalHeader().setSectionResizeMode(_ + 7, QtWidgets.QHeaderView.ResizeMode.Fixed)

        self.horizontalHeader().setStretchLastSection(True)

    def update_data(self):
        return self.data_model.select()


class BaseAbstractController(QtWidgets.QWidget):
    def __init__(self, calcs_names, calcs_objects, icon_path, tooltips):
        super().__init__()
        self.calcs_names = calcs_names
        self.calcs_objects = calcs_objects
        self.icon_path = icon_path
        self.tooltips = tooltips

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])

        self.calcs_area = QtWidgets.QTabWidget(self)
        self.calcs_area.setCurrentIndex(0)
        self.calcs_area.setUsesScrollButtons(False)

        x = len(self.calcs_names)
        if x == 2:
            y = x
        else:
            y = 0

        [self.calcs_area.addTab(self.calcs_objects[_], self.calcs_names[_]) for _ in range(x)]
        self.box.addWidget(self.calcs_area, 0, y, 8, 1, alignment=ct.data_library["Позиция левый-верхний"])

        self.buttons = []
        frame = QtWidgets.QWidget(self)
        frame.setFixedSize(ct.data_library["Размер виджета кнопок"])
        box = QtWidgets.QVBoxLayout(frame)
        x = self.box.columnCount()

        for _ in range(3):
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(self.icon_path[_]))
            button.setToolTip(self.tooltips[_])
            button.setToolTipDuration(3000)
            button.setIconSize(ct.data_library["Размеры кнопок"])
            button.setAutoDefault(True)
            self.buttons.append(button)
            box.addWidget(button, alignment=ct.data_library["Позиция центр"])

        self.box.addWidget(frame, 1, x, 8, 1, ct.data_library["Позиция левый-верхний"])


class RegistersController(BaseAbstractController):
    def __init__(self):
        super().__init__(("Физические факторы", "Радиационные факторы"),(Factors(ct.data_library["Журналы"]["Физические факторы"]["Параметры"]),
        Factors(ct.data_library["Журналы"]["Радиационные факторы"]["Параметры"])),
        ct.data_library["Элементы управления"]["Иконки журнала"], ct.data_library["Элементы управления"]["Подсказки журнала"])

        self.connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connect.setDatabaseName('registers_data.db')
        if not self.connect.open():
            self.error_message(2)

        [self.box.addWidget(QtWidgets.QLabel(ct.data_library["Журналы"]["Основной регистратор"]["Параметры"][_], self),
                            _, 0, ct.data_library["Позиция левый-центр"]) for _ in range(8)]

        self.entry_objects = []
        self.entry_objects.append(QtWidgets.QLineEdit(self))
        [self.entry_objects.append(QtWidgets.QDateEdit(self)) for _ in range(2)]
        [self.entry_objects.append(QtWidgets.QLineEdit(self)) for _ in range(3)]
        [self.entry_objects.append(QtWidgets.QComboBox(self)) for _ in range(2)]

        [_.setFixedSize(ct.data_library["Размеры поля ввода инфо. протокола"]) for _ in self.entry_objects[:3]]
        [_.setFixedSize(ct.data_library["Размеры поля ввода инфо. объекта"]) for _ in self.entry_objects[3:6]]
        self.entry_objects[6].setFixedSize(ct.data_library["Размеры поля ввода инфо. протокола"])
        self.entry_objects[7].setFixedSize(ct.data_library["Размеры поля ввода инфо. объекта"])

        [self.box.addWidget(self.entry_objects[_], _, 1, ct.data_library["Позиция левый-центр"]) for _ in range(8)]

        for _ in self.entry_objects[1:3]:
            _.setDate(ct.data_library["Текущий период"])
            _.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)

        [self.entry_objects[6].addItem(ct.data_library["Журналы"]["Основной регистратор"]["Тип выполнения"][_], _) for _
         in range(7)]
        [self.entry_objects[7].addItem(ct.data_library["Журналы"]["Основной регистратор"]["Сотрудники"][_], _) for _
         in range(5)]

        self.factors_tables = (ProtocolView(self.calcs_names[0], self), ProtocolView(self.calcs_names[1], self))

        self.error_message = lambda x: QtWidgets.QMessageBox.critical(self, " ", ct.data_library["Журналы"]["Критические сообщения"][x])

        self.calcs_area.currentChanged.connect(self.clear_number_to_move)

        self.buttons[0].clicked.connect(self.save_protocol)
        self.buttons[1].clicked.connect(self.clear_fields)
        self.buttons[2].clicked.connect(self.run_protocols_view)

    def record_main_data(self):
        x = QtSql.QSqlQuery()
        n = self.calcs_area.currentIndex()

        protocol_data = [_.text() for _ in self.entry_objects[:6]]
        [protocol_data.append(_.itemData(_.currentIndex())) for _ in self.entry_objects[6:]]

        x.prepare(f"INSERT INTO {ct.data_library["Журналы"]["Основной регистратор"]["Тип журнала"][n]} "
                  f"VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)")
        [x.addBindValue(_) for _ in protocol_data]
        return x.exec()

    def record_factors_data(self):
        n = self.calcs_area.currentIndex()
        x = QtSql.QSqlQuery()

        for i in self.calcs_objects[n].r:
            x.prepare(f"INSERT INTO {ct.data_library["Журналы"][self.calcs_names[n]]["Таблицы"][i]} VALUES(NULL, ?, ?)")
            [x.addBindValue(self.calcs_objects[n].entry_objects[_][i].value()) for _ in range(2)]
            if not x.exec():
                return self.error_message(1)

    @QtCore.pyqtSlot()
    def save_protocol(self):
        n = self.calcs_area.currentIndex()

        if (self.entry_objects[0].text() == "" or [i for i, j in enumerate(self.entry_objects[3:6]) if j.text() == ""]
                or [i for i, j in enumerate(self.entry_objects[6:]) if j.currentIndex() == 0] or not self.calcs_objects[n].validate_values()):
            return self.error_message(0)
        else:
            if self.record_main_data():
                self.record_factors_data()
                self.factors_tables[n].update_data()
            else:
                return self.error_message(1)

    @QtCore.pyqtSlot()
    def clear_fields(self):
        [_.clear() for _ in self.entry_objects[:6]]
        [_.setCurrentIndex(0) for _ in self.entry_objects[6:]]

        for _ in range(2):
            [j.clear() for i in self.calcs_objects[_].entry_objects for j in i]
            [j.setValue(0) for i in self.calcs_objects[_].entry_objects for j in i]

    @QtCore.pyqtSlot()
    def run_protocols_view(self):
        return self.factors_tables[self.calcs_area.currentIndex()].show()

    @QtCore.pyqtSlot()
    def clear_number_to_move(self):
        return self.entry_objects[0].clear()


class CalculatorsController(BaseAbstractController):
    def __init__(self):
        super().__init__(list(ct.data_library["Калькуляторы"].keys()),
        (AtmosphericAirDust(), AtmosphericAirDust(ct.data_library["Калькуляторы"]["Пыль в воздухе рабочей зоны"]["Параметры"],
        ct.data_library["Калькуляторы"]["Пыль в воздухе рабочей зоны"]["Результаты"]), VentilationEfficiency(),
         NoiseLevelsWithBackground()), ct.data_library["Элементы управления"]["Иконки калькулятора"],
                         ct.data_library["Элементы управления"]["Подсказки калькулятора"])

        self.log_file = lambda: f"\\{self.calcs_names[self.calcs_area.currentIndex()]}_отчет.txt"
        self.separator = f"\n{'-' * 101}\n"
        self.message = lambda: QtWidgets.QMessageBox.information(self, " ",
            f"Данные рассчета будут сохранены\nна рабочий стол в файл \'{self.log_file[1:]}\'")

        self.buttons[0].clicked.connect(self.calculating)
        self.buttons[1].clicked.connect(self.clearing)
        self.buttons[2].clicked.connect(self.saving)

    def ready_to_calculate_airs(self):
        n = self.calcs_area.currentIndex()

        if [i for i, j in enumerate(self.calcs_objects[n].entry_objects) if j.text() == ""]:
            return
        else:
            self.calcs_objects[n].calculate()

    def clear_basic_calc(self):
        n = self.calcs_area.currentIndex()

        [_.clear() for _ in self.calcs_objects[n].entry_objects]
        [cb.reset_value(_) for _ in self.calcs_objects[n].entry_objects]
        self.calcs_objects[n].result_area.clear()

    def save_basic_calc(self):
        n = self.calcs_area.currentIndex()

        if self.calcs_objects[n].result_area.text() != "":
            data = [self.calcs_objects[n].parameters[_] + ': ' + self.calcs_objects[n].entry_objects[_].text() +
                    '\n' for _ in range(len(self.calcs_objects[n].parameters))]
            data.append('\n' + self.calcs_objects[n].result_area.text() + self.separator)

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
            [data.append("----".ljust(8)) for _ in self.calcs_objects[3].sum]
            data.append('\n')

            for n, i in enumerate(self.calcs_objects[3].octave_table):
                data.append(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Результаты"][n].ljust(23))
                [data.append(j.text().ljust(8)) for j in i]
                data.append('\n')
            data.append(self.separator)

            self.message()
            self.write_to_file(data)
        else:
            return

    def write_to_file(self, data):
        with open(get_desktop() + self.log_file, "a", encoding="utf-8") as txt:
            txt.writelines(data)

    @QtCore.pyqtSlot()
    def calculating(self):
        match self.calcs_area.currentIndex():
            case 2:
                if ([i for i, j in enumerate(self.calcs_objects[2].entry_objects[0:3]) if j.text() == ""] or
                        not self.calcs_objects[2].check_hole_data()):
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
            [cb.reset_value(j) for i in self.calcs_objects[3].octave_table for j in i]
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
        self.resize(ct.data_library["Размер главного окна"])

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(0, 0, 0, 8)
        self.box.setRowStretch(1, 1)
        self.box.setColumnStretch(1, 1)
        self.box.setColumnStretch(2, 15)

        self.main_menu = QtWidgets.QMenuBar(self)
        self.main_menu.submenu_file = QtWidgets.QMenu(ct.data_library["Главное меню"][0], self.main_menu)
        self.main_menu.submenu_help = QtWidgets.QMenu(ct.data_library["Главное меню"][2], self.main_menu)
        self.main_menu.change_style = QtGui.QAction(ct.data_library["Главное меню"][3], self.main_menu)
        self.main_menu.change_style.setCheckable(True)

        self.main_menu.addMenu(self.main_menu.submenu_file)
        self.main_menu.addMenu(self.main_menu.submenu_help)
        self.main_menu.addAction(self.main_menu.change_style)
        self.set_style_act = self.main_menu.change_style
        self.main_menu.change_style.toggled.connect(self.change_app_style)

        self.main_menu.set_calculators_act = QtGui.QAction(self.data_dict_names[27], self.main_menu.submenu_file)
        self.main_menu.set_calculators_act.triggered.connect(partial(self.set_selector_index, 0))
        self.main_menu.set_calculators_act.triggered.connect(self.select_calcs_type)

        self.main_menu.set_registers_act = QtGui.QAction(self.data_dict_names[28], self.main_menu.submenu_file)
        self.main_menu.set_registers_act.triggered.connect(partial(self.set_selector_index, 1))
        self.main_menu.set_registers_act.triggered.connect(self.select_calcs_type)

        self.main_menu.exit_act = QtGui.QAction(ct.data_library["Главное меню"][1], self.main_menu.submenu_file)
        self.main_menu.exit_act.triggered.connect(sys.exit)

        self.main_menu.submenu_file.addAction(self.main_menu.set_calculators_act)
        self.main_menu.submenu_file.addAction(self.main_menu.set_registers_act)
        self.main_menu.submenu_file.addSeparator()
        self.main_menu.submenu_file.addAction(self.main_menu.exit_act)

        self.main_menu.help_link = QtGui.QAction(self.data_dict_names[1], self.main_menu.submenu_help)
        self.main_menu.help_link.triggered.connect(self.open_help_message)

        self.main_menu.about = QtGui.QAction(self.data_dict_names[2], self.main_menu.submenu_help)
        self.main_menu.about.triggered.connect(self.open_about_app_message)

        self.main_menu.submenu_help.addAction(self.main_menu.help_link)
        self.main_menu.submenu_help.addSeparator()
        self.main_menu.submenu_help.addAction(self.main_menu.about)
        self.box.addWidget(self.main_menu, 0, 0, 1, 4)

        self.selector_panel = QtWidgets.QListView(self)
        self.selector_panel.setSpacing(10)
        self.selector_panel.setFixedSize(150, 675)

        self.selector_panel.model_type = QtCore.QStringListModel((self.data_dict_names[27], self.data_dict_names[28]))
        self.selector_panel.setModel(self.selector_panel.model_type)

        self.selector_panel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.selector_panel.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.selector_panel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        self.selector_model = self.selector_panel.model_type
        self.selector_panel.setCurrentIndex(self.selector_model.index(0, 0))
        self.selector_panel.clicked.connect(self.select_calcs_type)

        self.controllers = (CalculatorsController(), RegistersController())

        for i, j in enumerate((self.selector_panel, self.controllers[0])):
            self.box.addWidget(j, 1, i + 1, ct.data_library["Позиция левый-верхний"])

        x = int(self.settings.value(ct.data_library["Настройки"], 0))
        self.set_style(ct.data_library["Цвета"][x])
        if x == 1:
            self.main_menu.change_style.setChecked(True)

        self.set_sizes(ct.data_library["Расстояние по умолчанию"])
        self.show()

    def changeEvent(self, x):
        if x.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.isMaximized():
                self.set_sizes(ct.data_library["Расстояние максимальное"])
            else:
                self.set_sizes(ct.data_library["Расстояние по умолчанию"])

        QtWidgets.QWidget.changeEvent(self, x)

    def set_sizes(self, distance):
        [self.controllers[0].calcs_objects[_].box.setHorizontalSpacing(distance[0]) for _ in range(3)]
        [self.controllers[0].calcs_objects[_].box.setVerticalSpacing(distance[1]) for _ in range(3)]
        self.controllers[0].calcs_objects[3].setFixedSize(distance[2])

        self.controllers[1].box.setHorizontalSpacing(distance[3])
        self.controllers[1].box.setVerticalSpacing(distance[1])

        [self.controllers[1].calcs_objects[_].box.setHorizontalSpacing(distance[1]) for _ in range(2)]
        [self.controllers[1].calcs_objects[_].box.setVerticalSpacing(distance[4]) for _ in range(2)]

    def set_style(self, colors):
        self.setStyleSheet("* {outline: none; border-style: none; background: "+colors[0]+" font: 13px arial, sans-serif;} "                                                  
            
            "QLabel {color: "+colors[6]+"} "
            "QToolTip {color: "+colors[2]+"} "
                                          
            "QMenuBar {background: "+colors[0]+" color: "+colors[2]+"} "   
            "QMenuBar::item:selected {border-radius: 5px; background: "+colors[3]+"} "
            "QMenu {border-radius: 5px; background: "+colors[7]+" color: "+colors[2]+"} "
            "QMenu::separator {border-bottom: 1px solid "+colors[5]+"} "                                      
            "QMenu::item:selected {background: transparent; color: "+colors[4]+"} "                     
            "QMenuBar::item:pressed {color: "+colors[4]+"} "
            "QMenuBar::item {margin: 2px 2px 2px 2px; padding: 7px 7px 7px 7px;} "
                                                                    
            "QMessageBox QLabel {color: "+colors[2]+"} "
            "QMessageBox .QPushButton {border-radius: 5px; padding: 6px 16px 6px 16px; background: "+colors[3]+" color: "+colors[2]+"} "                             
            "QMessageBox .QPushButton:pressed {background: "+colors[4]+"}"    
             
            "QPushButton {border-radius: 9px; padding: 3px;} "
            "QPushButton:hover {background: "+colors[3]+"} "
            "QPushButton:pressed {background: "+colors[4]+"} "

            "QListView {border-radius: 9px; background: "+colors[5]+"} "       
            "QListView::item {border-radius: 5px; padding: 2px; color: "+colors[2]+"} "
            "QListView::item:hover {background: "+colors[3]+"} "
            "QListView::item:selected {background: "+colors[3]+" color: "+colors[4]+"}"

            "QTabWidget:pane {border-style: none;} "
            "QTabBar:tab {border-radius: 5px; margin-left: 7px; margin-right: 7px; padding: 5px; background: "+colors[5]+" color: "+colors[2]+"} "     
            "QTabBar:tab::hover {background: "+colors[3]+"} "
            "QTabBar:tab::selected {background: "+colors[3]+" color: "+colors[4]+"} "   
                                                                                                           
            "QLineEdit, QDateEdit, QSpinBox, QComboBox {border-radius: 5px; background: "+colors[7]+" color: "+colors[8]+"} "                                                           
             
            "QLineEdit:focus {background: "+colors[1]+"} "
            "QDateEdit:focus {background: "+colors[1]+"} "
            "QComboBox:selected {background: "+colors[1]+"} "
            "QComboBox::drop-down {background: transparent;} "                           
            "QSpinBox:focus {background: "+colors[1]+"} "
                                                                                                                                                                                           
            "QLabel#result_field {border-radius: 9px; background: "+colors[9]+" color: "+colors[10]+"} "
            "QLabel#result_field_noise {border-radius: 5px; background: "+colors[9]+" color: "+colors[10]+"}")

        [_.setStyleSheet("QTableView {outline: none; font: 10px verdana, sans-serif; "
                         "gridline-color: "+colors[8]+" background: "+colors[5]+" color: "+colors[2]+"} "
            "QTableView::item:selected {background: "+colors[3]+" color: "+colors[4]+"} "
            "QHeaderView::section {border: 0px; font: 10px verdana, sans-serif; background: "+colors[0]+" color: "+colors[6]+"} "
            "QTableCornerButton::section {border: 0px; background: "+colors[0]+"} "
            "QScrollBar {background: transparent;} "                            
            "QScrollBar::add-page {border: 0px; background: "+colors[7]+"} "
            "QScrollBar::sub-page {border: 0px; background: "+colors[7]+"} "
            "QScrollBar::handle {border: 0px; border-radius: 5px; background: "+colors[9]+"} "
            "QScrollBar::handle:hover {background: "+colors[3]+"}") for _ in self.controllers[1].factors_tables]

    @QtCore.pyqtSlot()
    def change_app_style(self):
        i = int(self.set_style_act.isChecked())

        self.set_style(ct.data_library["Цвета"][i])
        self.settings.setValue(ct.data_library["Настройки"], i)
        self.settings.sync()

    @QtCore.pyqtSlot()
    def set_selector_index(self, x):
        return self.selector_panel.setCurrentIndex(self.selector_model.index(x, 0))

    @QtCore.pyqtSlot()
    def select_calcs_type(self):
        x = [0, 1]
        if self.selector_panel.currentIndex().row() == 1:
            x.reverse()

        self.controllers[x[1]].close()
        self.box.replaceWidget(self.controllers[x[1]], self.controllers[x[0]])
        self.controllers[x[0]].show()

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        return QtWidgets.QMessageBox.about(self, self.data_dict_names[2], ct.data_library["О программе"])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        return QtWidgets.QMessageBox.information(self, self.data_dict_names[1], ct.data_library["Справка"])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icons/calc_logo.ico"))
    app_calcs = ApplicationType()
    sys.exit(app.exec())
