from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from winpath import get_desktop
import constants as ct
from calculators_objects import (AtmosphericAirDust, VentilationEfficiency, NoiseLevelsWithBackground, MainRegister,
                                 FactorsRegister)


class BaseAbstractController(QtWidgets.QWidget):
    CALCS = 1
    REGISTERS = 2
    POSITION = ct.data_library["Позиция левый-верхний"]

    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])

    def create_calcs(self, calc_variant, calcs_list):
        area = QtWidgets.QTabWidget(self)
        area.setCurrentIndex(0)
        area.setDocumentMode(True)
        area.setUsesScrollButtons(False)
        area.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)

        match calc_variant:
            case 1:
                names = list(ct.data_library["Калькуляторы"].keys())

            case 2:
                temp = list(ct.data_library["Журналы"].keys())
                names = temp[1:3]
            case _:
                return

        for i, j in enumerate(calcs_list):
            area.addTab(j, names[i])

        column_start = self.box.columnCount()
        self.box.addWidget(area, 0, column_start, 8, 1, alignment=self.POSITION)
        return area

    def create_control_buttons(self, calc_variant):
        buttons = []
        row_start = 1
        column_start = self.box.columnCount()

        match calc_variant:
            case 1:
                r = range(3)
                icons = ct.data_library["Иконки"][0:3]
                tooltips = ct.data_library["Иконки"][4:7]
            case 2:
                r = range(2)
                icons = list(ct.data_library["Иконки"][1:3])
                icons.reverse()
                tooltips = ct.data_library["Иконки"][7:9]
            case _:
                return

        for i in r:
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(icons[i]))
            button.setToolTip(tooltips[i])
            button.setToolTipDuration(3000)
            button.setIconSize(ct.data_library["Размеры кнопок"])
            button.setAutoDefault(True)
            buttons.append(button)
            self.box.addWidget(button, row_start, column_start, self.POSITION)
            row_start += 1

        return buttons


class RegistersController(BaseAbstractController):
    def __init__(self):
        super().__init__()
        self.registers = (MainRegister(), FactorsRegister(), FactorsRegister(ct.data_library["Журналы"]["Радиационные факторы"]))
        self.box.addWidget(self.registers[0], 0, 0, 11, 2, alignment=self.POSITION)

        self.options_zone = self.create_calcs(self.REGISTERS, self.registers[1:])

        self.controls = self.create_control_buttons(self.REGISTERS)

        #self.options_area.currentChanged.connect(self.clear_protocol_number_entry_field)



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
    def clear_protocol_number_entry_field(self):
        self.base_register_area.entry_objects_others[0].clear()'''


class CalculatorsController(BaseAbstractController):
    def __init__(self):
        super().__init__()
        self.calcs = (AtmosphericAirDust(), AtmosphericAirDust(ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]),
                      VentilationEfficiency(), NoiseLevelsWithBackground())

        self.calcs_zone = self.create_calcs(self.CALCS, self.calcs)

        self.controls = self.create_control_buttons(self.CALCS)

        #self.calculate.clicked.connect(self.calculating)



    @staticmethod
    def clear_entry_fields(entry_objects):
        for _ in entry_objects:
            _.clear()
            _.value = None

    @staticmethod
    def create_data_to_save(title_names, entry_fields, result):     # list generator !!!!
        data = []
        for i in range(len(title_names)):
            data.append(title_names[i] + ': ' + entry_fields[i].text() + '\n')
        data.append(result.text() + ct.data_library["Отчет"][5])
        return data

    @staticmethod
    def create_noise_calc_data_to_save(bands, source, background, delta, correct):
        data = []
        r = range(10)

        for i in r:
            data.append(bands[i] + '|*|')

        data.append(ct.data_library["Отчет"][5])
        for j in (source, background, delta, correct):
            for i in r:
                data.append(j[i].text() + '   ')
            data.append('\n')

        return data

    def save_to_desktop(self, file, data):
        message = f"{ct.data_library["Отчет"][4]}\'{file[1:]}\'"
        file_path = get_desktop() + file
        QtWidgets.QMessageBox.information(self, " ", message)
        with open (file_path, "a", encoding="utf-8") as txt:
            txt.writelines(data)

    '''@QtCore.pyqtSlot()
    def calculating(self):
        try:
            match self.calcs_area.currentIndex():
                case 0:
                    self.air_calc.calculate()
                case 1:
                    self.work_area_calc.calculate()
                case 2:
                    self.flow_calc.calculate()
                case 3:
                    self.noise_calc.calculate()
        except TypeError:
            pass

    @QtCore.pyqtSlot()
    def clear_calculator(self):
        match self.calcs_area.currentIndex():
            case 0:
                self.clear_entry_fields(self.air_calc.entry_objects)
                self.air_calc.result_area.clear()
            case 1:
                self.clear_entry_fields(self.work_area_calc.entry_objects)
                self.work_area_calc.result_area.clear()
            case 2:
                self.clear_entry_fields(self.flow_calc.entry_objects)
                self.flow_calc.result_area.clear()
            case 3:
                self.clear_entry_fields(self.noise_calc.entry_objects)
                for result_object in self.noise_calc.result_area:
                    result_object.clear()

    @QtCore.pyqtSlot()
    def saving(self):
        match self.calcs_area.currentIndex():
            case 0:
                if self.air_calc.result_area.text() != "":
                    air_calc_data = self.create_data_to_save(ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]
                                    ["Параметры"], self.air_calc.entry_objects, self.air_calc.result_area)
                    self.save_to_desktop(ct.data_library["Отчет"][0], air_calc_data)
                else: pass
            case 1:
                if self.work_area_calc.result_area.text() != "":
                    work_area_calc_data = self.create_data_to_save(ct.data_library["Калькуляторы"]
                                          ["Пыль в воздухе раб. зоны"]["Параметры"], self.work_area_calc.entry_objects,
                                                                   self.work_area_calc.result_area)
                    self.save_to_desktop(ct.data_library["Отчет"][1], work_area_calc_data)
                else: pass
            case 2:
                if self.flow_calc.result_area.text() != "":
                    flow_calc_data = self.create_data_to_save(ct.data_library["Калькуляторы"]["Эффектив. вентиляции"]
                                     ["Параметры"], self.flow_calc.entry_objects, self.flow_calc.result_area)
                    self.save_to_desktop(ct.data_library["Отчет"][2], flow_calc_data)
                else: pass
            case 3:
                if self.noise_calc.delta_result_area[0].text() != "":
                    noise_calc_data = self.create_noise_calc_data_to_save(ct.data_library["Калькуляторы"]
                                      ["Учет влияния фонового шума"]["Параметры"], self.noise_calc.entry_objects_source,
                                      self.noise_calc.entry_objects_background, self.noise_calc.delta_result_area,
                                                                          self.noise_calc.correct_result_area)
                    self.save_to_desktop(ct.data_library["Отчет"][3], noise_calc_data)
                else: pass'''


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

        for _ in (self.calculators_area.calcs_zone, self.registers_area.options_zone):
            _.setStyleSheet("* {color: "+colors[5]+"}")

        for _ in calcs_list:
            _.setStyleSheet("QLabel {color: "+colors[6]+"} "
                            "QLineEdit, QDateEdit, QSpinBox {border-radius: 5px; background: "+colors[7]+" color: "+colors[8]+"} "
                            "QLineEdit:focus {background: "+colors[9]+"} "
                            "QDateEdit:focus {background: "+colors[9]+"} "
                            "QSpinBox:focus {background: "+colors[9]+"}")

        for _ in calcs_list[0:3]:
            _.result_area.setStyleSheet(result_area_style("9px;"))
        for _ in self.calculators_area.calcs[3].result_area:
            _.setStyleSheet(result_area_style("5px;"))

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

        main_menu.set_calculators_act = QtGui.QAction(self.data_dict_names[13], main_menu.submenu_file)
        main_menu.set_calculators_act.triggered.connect(self.calculators_show_fixed)
        main_menu.set_registers_act = QtGui.QAction(self.data_dict_names[14], main_menu.submenu_file)
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

        selector_panel.names = (self.data_dict_names[13], self.data_dict_names[14])
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
    app_calcs = ApplicationType()
    sys.exit(app.exec())
