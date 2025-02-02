from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from winpath import get_desktop
import constants as ct
from calculators_objects import (AtmosphericAirDust, VentilationEfficiency, NoiseLevelsWithBackground, MainRegister,
                                 FactorsRegister, AbstractInputZone as az)


class BaseAbstractController(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])

    def create_calcs(self, calcs_list, calc_variant=True):
        area = QtWidgets.QTabWidget(self)
        area.setCurrentIndex(0)
        area.setDocumentMode(True)
        area.setUsesScrollButtons(False)
        area.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)

        if calc_variant:
            names = list(ct.data_library["Калькуляторы"].keys())
        else:
            temp = list(ct.data_library["Журналы"].keys())
            names = temp[1:3]

        for i, j in enumerate(calcs_list):
            area.addTab(j, names[i])

        self.box.addWidget(area, 0, self.box.columnCount(), 8, 1, alignment=ct.data_library["Позиция левый-верхний"])
        return area

    def create_control_buttons(self, calc_variant=True):
        buttons = []
        row_start = 1
        column_start = self.box.columnCount()

        if calc_variant:
            r = range(3)
            icons = ct.data_library["Иконки"][0:3]
            tooltips = ct.data_library["Иконки"][4:7]
        else:
            r = range(2)
            icons = list(ct.data_library["Иконки"][1:3])
            icons.reverse()
            tooltips = ct.data_library["Иконки"][7:9]

        for i in r:
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(icons[i]))
            button.setToolTip(tooltips[i])
            button.setToolTipDuration(3000)
            button.setIconSize(ct.data_library["Размеры кнопок"])
            button.setAutoDefault(True)
            buttons.append(button)
            self.box.addWidget(button, row_start, column_start, ct.data_library["Позиция левый-верхний"])
            row_start += 1

        return buttons


class RegistersController(BaseAbstractController):
    def __init__(self):
        super().__init__()
        self.registers = (MainRegister(), FactorsRegister(), FactorsRegister(ct.data_library["Журналы"]["Радиационные факторы"]))
        self.box.addWidget(self.registers[0], 0, 0, 11, 2, alignment=ct.data_library["Позиция левый-верхний"])

        self.options_zone = self.create_calcs(self.registers[1:], False)
        #self.options_zone.currentChanged.connect(self.clear_protocol_number)

        self.controls = self.create_control_buttons(False)





'''def save_physical_protocol(self):
        self.base_register_area.connection_with_database.open()

        queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
                        self.base_register_area.ready_insert_to_dates_of_research_table(),
                        self.base_register_area.ready_insert_to_objects_names_table(),
                        self.base_register_area.ready_insert_to_objects_addresses_table(),
                        self.physical_register_options.ready_insert_to_microclimate_table(),
                        self.physical_register_options.ready_insert_to_light_table(),
                        self.physical_register_options.ready_insert_to_noise_table(),
                        self.physical_register_options.ready_insert_to_vibration_table(),
                        self.physical_register_options.ready_insert_to_emf_table(),
                        self.physical_register_options.ready_insert_to_aeroionics_table(),
                        self.physical_register_options.ready_insert_to_ventilation_table())

        self.check_read_to_database(queries_list)
        self.base_register_area.connection_with_database.close()

    def save_radiation_protocol(self):
        self.base_register_area.connection_with_database.open()

        queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
                        self.base_register_area.ready_insert_to_dates_of_research_table(),
                        self.base_register_area.ready_insert_to_objects_names_table(),
                        self.base_register_area.ready_insert_to_objects_addresses_table(),
                        self.radiation_control_register_options.ready_insert_to_gamma_radiation_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_volume_activity_table(),
                        self.radiation_control_register_options.ready_insert_to_eeva_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_flux_density_table())

        self.check_read_to_database(queries_list)
        self.base_register_area.connection_with_database.close()

    def check_read_to_database(self, queries):
        for query in queries:
            check = query.exec()
            if not check:
                self.show_database_error()

    def show_database_error(self):
        QtWidgets.QMessageBox.critical(self, " ", "Ошибка записи в базу данных."
                                                  "\nНекоторые данные могли не сохраниться !")

    @QtCore.pyqtSlot()
    def select_insert_command(self):
        match self.options_area.currentIndex():
            case 0:
                self.save_physical_protocol()
            case 1:
                self.save_radiation_protocol()

    @QtCore.pyqtSlot()
    def clear_registers_values(self):
        for _ in self.base_register_area.entry_objects_dates:
            _.clear()
        for _ in self.base_register_area.entry_objects_others:
            _.clear()
        for _ in self.physical_register_options.entry_objects:
            _.clear()
        for _ in self.radiation_control_register_options.entry_objects:
            _.clear()

    @QtCore.pyqtSlot()
    def clear_protocol_number(self):
        self.base_register_area.entry_objects_others[0].clear()'''


class CalculatorsController(BaseAbstractController):
    AIR = 0
    WORK_ZONE = 1
    FLOW = 2
    NOISE = 3

    def __init__(self):
        super().__init__()
        self.calcs = (AtmosphericAirDust(), AtmosphericAirDust(ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]),
                      VentilationEfficiency(), NoiseLevelsWithBackground())

        self.calcs_zone = self.create_calcs(self.calcs)

        self.controls = self.create_control_buttons()
        self.controls[0].clicked.connect(self.calculating)
        self.controls[1].clicked.connect(self.clearing)
        self.controls[2].clicked.connect(self.saving)

    def ready_to_calculate(self, calc_index=True):
        match calc_index:
            case 2:
                if az.check_fields(self.calcs[2].entry_objects[0:3]) and self.calcs[2].set_hole_checks():
                    self.calcs[2].calculate()
                else:
                    pass

            case _:
                if az.check_fields(self.calcs[calc_index].entry_objects):
                    self.calcs[calc_index].calculate()
                else:
                    pass

    def ready_to_save(self, calc_index):
        if calc_index != 3:
            result = self.calcs[calc_index].result_area.text()
        else:
            result = self.calcs[3].correct_result_area[0].text()

        if result != "":
            self.save_on_desktop(calc_index)
        else:
            pass

    def save_on_desktop(self, calc_index):
        data = []

        if calc_index != 3:
            for i, j in enumerate(self.calcs[calc_index].titles):
                data.append(j + ': ' + self.calcs[calc_index].entry_objects[i].text() + '\n')
            data.append('\n' + self.calcs[calc_index].result_area.text() + ct.data_library["Отчет"][5])

        else:
            [data.append(i + '|*|') for i in ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10]]
            data.append(ct.data_library["Отчет"][5])

            for j in (self.calcs[3].entry_objects_source, self.calcs[3].entry_objects_background,
                      self.calcs[3].delta_result_area, self.calcs[3].correct_result_area):
                [data.append(i.text() + '   ') for i in j]
                data.append('\n')
            data.append('\n')

        QtWidgets.QMessageBox.information(self, " ",
                                          f"{ct.data_library["Отчет"][4]}\'{ct.data_library["Отчет"][calc_index][1:]}\'")
        with open(get_desktop() + ct.data_library["Отчет"][calc_index], "a", encoding="utf-8") as txt:
            txt.writelines(data)

    @QtCore.pyqtSlot()
    def calculating(self):
        match self.calcs_zone.currentIndex():
            case 0:
                self.ready_to_calculate(self.AIR)
            case 1:
                self.ready_to_calculate(self.WORK_ZONE)
            case 2:
                self.ready_to_calculate(self.FLOW)
            case 3:
                self.calcs[3].calculate()

    @QtCore.pyqtSlot()
    def clearing(self):
        match self.calcs_zone.currentIndex():
            case 0:
                az.clear_fields(self.calcs[0].entry_objects)
                self.calcs[0].result_area.clear()
            case 1:
                az.clear_fields(self.calcs[1].entry_objects)
                self.calcs[1].result_area.clear()
            case 2:
                az.clear_fields(self.calcs[2].entry_objects)
                self.calcs[2].result_area.clear()
            case 3:
                az.clear_fields(self.calcs[3].entry_objects)
                az.clear_fields(self.calcs[3].result_area)

    @QtCore.pyqtSlot()
    def saving(self):
        match self.calcs_zone.currentIndex():
            case 0:
                self.ready_to_save(self.AIR)
            case 1:
                self.ready_to_save(self.WORK_ZONE)
            case 2:
                self.ready_to_save(self.FLOW)
            case 3:
                self.ready_to_save(self.NOISE)


class ApplicationType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        QtWidgets.QApplication.setOrganizationName("Ivan Bogdanov")
        QtWidgets.QApplication.setApplicationName("Calculators 2.1.0 Beta")
        settings = QtCore.QSettings(self)

        self.setWindowTitle("Калькуляторы")
        self.resize(1015, 550)
        self.move(self.width() * -2, 0)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()

        self.data_dict_names = list(ct.data_library.keys())

        self.menu_area = self.create_main_menu()
        self.selector_area = self.create_selector_panel()
        self.registers_area = RegistersController()
        self.calculators_area = CalculatorsController()
        self.registers_area.close()

        self.set_style(ct.data_library["Цвета светлой темы"])

        settings.beginWriteArray("Light Style")
        for i, el in enumerate(ct.data_library["Цвета светлой темы"]):
            settings.setArrayIndex(i)
            settings.setValue("Color", el)

        settings.endArray()
        settings.sync()

        self.box = QtWidgets.QGridLayout(self)
        self.box.setHorizontalSpacing(5)
        self.box.setVerticalSpacing(15)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.box.addWidget(self.menu_area, 0, 0, 1, 4)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, ct.data_library["Позиция левый-верхний"])
        self.box.addWidget(self.calculators_area, 1, 2, 1, 1, ct.data_library["Позиция левый-верхний"])

        self.box.setColumnMinimumWidth(0, 1)
        self.show()

    def set_style(self, colors):
        calcs_list = self.calculators_area.calcs + self.registers_area.registers
        result_area_style = lambda r: "border-radius: "+r+" background: "+colors[10]+" color: "+colors[11]

        self.setStyleSheet("* {outline: 0; border-style: none; background: "+colors[0]+" font: 13px arial, sans-serif; "
                                                                                       "color: "+colors[2]+"} "
                         
                           "QMenuBar, QMenu {background: "+colors[1]+"} "
                           "QMenuBar::item:selected {background: "+colors[3]+"} "
                           "QMenu::item:selected {background: "+colors[3]+"} "
                                                                         
                           "QPushButton {border-radius: 9px; padding: 3px;} "
                           "QPushButton:hover {background: "+colors[3]+"} "
                           "QPushButton:pressed {background: "+colors[4]+"} "                                     
                          
                           "QMessageBox .QPushButton {border-radius: 5px; padding: 6px 16px 6px 16px; "
                           "background: "+colors[3]+"} "
                           "QMessageBox .QPushButton:pressed {background: "+colors[4]+"}")

        self.selector_area.setStyleSheet("* {border-radius: 9px; background: "+colors[1]+"} "
                                         
                                         "QListView::item {border-radius: 5px; padding: 2px;} "
                                         "QListView::item:hover {background: "+colors[3]+"} "
                                         "QListView::item:selected {background: "+colors[3]+" color: "+colors[4]+"}")

        [_.setStyleSheet("* {color: "+colors[5]+"}") for _ in (self.calculators_area.calcs_zone, self.registers_area.options_zone)]

        [_.setStyleSheet("QLabel {color: "+colors[6]+"} "
                            "QLineEdit, QDateEdit, QSpinBox {border-radius: 5px; background: "+colors[7]+" color: "+colors[8]+"} "
                            "QLineEdit:focus {background: "+colors[9]+"} "
                            "QDateEdit:focus {background: "+colors[9]+"} "
                            "QSpinBox:focus {background: "+colors[9]+"}") for _ in calcs_list]

        [_.result_area.setStyleSheet(result_area_style("9px;")) for _ in calcs_list[0:3]]
        [_.setStyleSheet(result_area_style("5px;")) for _ in self.calculators_area.calcs[3].result_area]

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        main_menu.setFixedHeight(20)

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
        selector_panel.setFixedSize(ct.data_library["Размеры зоны выбора"])
        selector_panel.setSpacing(10)
        selector_panel.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)

        selector_panel.names = (self.data_dict_names[24], self.data_dict_names[25])
        selector_panel.model_type = QtCore.QStringListModel(selector_panel.names)
        selector_panel.setModel(selector_panel.model_type)

        selector_panel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        selector_panel.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        selector_panel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        selector_panel.calculators_index = selector_panel.model_type.index(0, 0)
        selector_panel.registers_index = selector_panel.model_type.index(1, 0)
        selector_panel.clicked.connect(self.click_on_selector_panel)

        return selector_panel

    @QtCore.pyqtSlot()
    def change_app_style(self):
        match self.menu_area.change_style.isChecked():
            case True:
                self.set_style(ct.data_library["Цвета темной темы"])
            case False:
                self.set_style(ct.data_library["Цвета светлой темы"])

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
    def click_on_selector_panel(self):
        match self.selector_area.currentIndex():
            case self.selector_area.calculators_index:
                self.calculators_show_fixed()
            case self.selector_area.registers_index:
                self.registers_show_fixed()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ct.data_library["Иконки"][3]))
    #print(type(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][16]))
    app_calcs = ApplicationType()
    sys.exit(app.exec())
