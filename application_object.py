from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from winpath import get_desktop
import constants as ct
from calculators_objects import (AtmosphericAirDust, WorkAreaAirDust, VentilationEfficiency, NoiseLevelsWithBackground,
                                 BaseRegister, PhysicalFactorsOptions, RadiationControlOptions)


class RegisterObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])
        self.box.setSpacing(40)
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.register_names = list(ct.data_library["Журналы"].keys())
        self.base_register_area = BaseRegister()
        self.options_area = QtWidgets.QTabWidget(self)
        self.options_area.setDocumentMode(True)
        self.options_area.setCurrentIndex(0)
        self.options_area.setUsesScrollButtons(False)
        self.options_area.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.options_area.currentChanged.connect(self.clear_protocol_number_entry_field)
        self.physical_register_options = PhysicalFactorsOptions()
        self.radiation_control_register_options = RadiationControlOptions()
        self.options_area.addTab(self.physical_register_options, self.register_names[1])
        self.options_area.addTab(self.radiation_control_register_options, self.register_names[2])
        self.save = QtWidgets.QPushButton(self)
        self.save.clicked.connect(self.select_insert_command)
        self.save.setIcon(self.icon_save)
        self.save.setToolTip("Сохранить протокол")
        self.save.setToolTipDuration(3000)
        self.clear = QtWidgets.QPushButton(self)
        self.clear.clicked.connect(self.clear_registers_values)
        self.clear.setIcon(self.icon_clear)
        self.clear.setToolTip("Очистить все журналы")
        self.clear.setToolTipDuration(3000)
        self.box.addWidget(self.base_register_area, 0, 0, 5, 5, alignment=ct.data_library["Позиция левый-верхний"])
        self.box.addWidget(self.options_area, 0, 5, 5, 3, alignment=ct.data_library["Позиция левый-верхний"])

        i = 0
        for _ in (self.save, self.clear):
            _.setIconSize(ct.data_library["Размеры кнопок"])
            _.setFlat(True)
            _.setAutoDefault(True)
            self.box.addWidget(_, 5, i, alignment=ct.data_library["Позиция левый-верхний"])
            i += 1

    def save_physical_protocol(self):
        self.base_register_area.connection_with_database.open()

        '''queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
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

        self.check_read_to_database(queries_list)'''
        self.base_register_area.connection_with_database.close()

    def save_radiation_protocol(self):
        self.base_register_area.connection_with_database.open()

        '''queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
                        self.base_register_area.ready_insert_to_dates_of_research_table(),
                        self.base_register_area.ready_insert_to_objects_names_table(),
                        self.base_register_area.ready_insert_to_objects_addresses_table(),
                        self.radiation_control_register_options.ready_insert_to_gamma_radiation_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_volume_activity_table(),
                        self.radiation_control_register_options.ready_insert_to_eeva_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_flux_density_table())

        self.check_read_to_database(queries_list)'''
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
        self.base_register_area.entry_objects_others[0].clear()


class CalculatorObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setSpacing(15)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.calc_names = list(ct.data_library["Калькуляторы"].keys())
        self.calcs_area = QtWidgets.QTabWidget(self)
        self.calcs_area.setCurrentIndex(0)
        self.calcs_area.setDocumentMode(True)
        self.calcs_area.setUsesScrollButtons(False)
        self.calcs_area.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.air_calc = AtmosphericAirDust()
        self.work_area_calc = WorkAreaAirDust()
        self.flow_calc = VentilationEfficiency()
        self.noise_calc = NoiseLevelsWithBackground()
        self.calculate = QtWidgets.QPushButton(self)
        self.calculate.clicked.connect(self.calculating)
        self.calculate.setIcon(self.icon_ok)
        self.calculate.setToolTip("Вычислить")
        self.calculate.setToolTipDuration(3000)
        self.clear = QtWidgets.QPushButton(self)
        self.clear.clicked.connect(self.clear_calculator)
        self.clear.setIcon(self.icon_clear)
        self.clear.setToolTip("Очистить всё")
        self.clear.setToolTipDuration(3000)
        self.save = QtWidgets.QPushButton(self)
        self.save.clicked.connect(self.saving)
        self.save.setIcon(self.icon_save)
        self.save.setToolTip("Сохранить в файл")
        self.save.setToolTipDuration(3000)

        j = 0
        for _ in (self.air_calc, self.work_area_calc, self.flow_calc, self.noise_calc):
            self.calcs_area.addTab(_, self.calc_names[j])
            j += 1

        self.box.addWidget(self.calcs_area, 0, 0, 6, 1, alignment=ct.data_library["Позиция левый-верхний"])

        i = 0
        for _ in (self.calculate, self.clear, self.save):
            _.setIconSize(ct.data_library["Размеры кнопок"])
            _.setFlat(True)
            _.setAutoDefault(True)
            self.box.addWidget(_, i, 1, alignment=ct.data_library["Позиция нижний-центр"])
            i += 1

    @staticmethod
    def clear_entry_fields(entry_objects):
        for _ in entry_objects:
            _.clear()
            _.value = None

    @staticmethod
    def create_data_to_save(title_names, entry_fields, result):
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

    @QtCore.pyqtSlot()
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
                else: pass


class ApplicationType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькуляторы")
        self.resize(1015, 550)
        self.move(self.width() * -2, 0)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()

        self.box = QtWidgets.QGridLayout(self)
        self.box.setHorizontalSpacing(5)
        self.box.setVerticalSpacing(15)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.data_dict_names = list(ct.data_library.keys())
        self.menu_area = self.create_main_menu()
        self.selector_area = self.create_selector_panel()
        self.registers = RegisterObjectsController(self)
        self.calculators = CalculatorObjectsController(self)
        self.registers.close()
        self.box.addWidget(self.menu_area, 0, 0, 1, 4)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, ct.data_library["Позиция левый-верхний"])
        self.box.addWidget(self.calculators, 1, 2, 1, 1, ct.data_library["Позиция левый-верхний"])
        self.box.setColumnMinimumWidth(0, 1)

        self.set_style(list(ct.data_library["Светлая тема"].values()))
        self.show()

    def set_style(self, style_list):
        calcs_list = (self.calculators.air_calc, self.calculators.work_area_calc, self.calculators.flow_calc,
                           self.calculators.noise_calc, self.registers.base_register_area,
                           self.registers.physical_register_options, self.registers.radiation_control_register_options)

        self.setStyleSheet(style_list[0])
        self.selector_area.setStyleSheet(style_list[1])
        self.calculators.calcs_area.setStyleSheet(style_list[2])
        self.registers.options_area.setStyleSheet(style_list[2])

        for _ in calcs_list:
            _.setStyleSheet(style_list[3])
        for _ in calcs_list[0:3]:
            _.result_area.setStyleSheet(style_list[4])
        self.calculators.noise_calc.set_result_field_style(style_list[4])

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
        selector_panel.setTabKeyNavigation(True)
        selector_panel.calculators_index = selector_panel.model_type.index(0, 0)
        selector_panel.registers_index = selector_panel.model_type.index(1, 0)
        selector_panel.clicked.connect(self.click_on_selector_panel)
        return selector_panel

    @QtCore.pyqtSlot()
    def change_app_style(self):
        match self.menu_area.change_style.isChecked():
            case True:
                self.set_style(list(ct.data_library["Темная тема"].values()))
            case False:
                self.set_style(list(ct.data_library["Светлая тема"].values()))

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, self.data_dict_names[2], ct.data_library["О программе"])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, self.data_dict_names[1], ct.data_library["Справка"])

    @QtCore.pyqtSlot()
    def calculators_show_fixed(self):
        self.registers.close()
        self.box.replaceWidget(self.registers, self.calculators)
        self.calculators.show()

    @QtCore.pyqtSlot()
    def registers_show_fixed(self):
        self.calculators.close()
        self.box.replaceWidget(self.calculators, self.registers)
        self.registers.show()

    @QtCore.pyqtSlot()
    def click_on_selector_panel(self):
        match self.selector_area.currentIndex():
            case self.selector_area.calculators_index:
                self.calculators_show_fixed()
            case self.selector_area.registers_index:
                self.registers_show_fixed()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("images/calc_logo.ico"))
    app_calcs = ApplicationType()
    sys.exit(app.exec())
