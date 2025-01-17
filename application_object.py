from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from winpath import get_desktop
from functools import partial
import constants
from calculators_objects import (AtmosphericAirDust, WorkAreaAirDust, VentilationEfficiency, NoiseLevelsWithBackground,
                                 BaseRegister, PhysicalFactorsOptions, RadiationControlOptions)


class RegisterObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize()

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_ALL_OBJECTS)
        self.box.setSpacing(40)
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.base_register_area = BaseRegister()
        self.options_area = QtWidgets.QTabWidget(self)
        self.options_area.setDocumentMode(True)
        self.options_area.setCurrentIndex(0)
        self.options_area.setUsesScrollButtons(False)
        self.options_area.currentChanged.connect(self.clear_protocol_number_entry_field)
        self.physical_register_options = PhysicalFactorsOptions()
        self.radiation_control_register_options = RadiationControlOptions()
        self.options_area.addTab(self.physical_register_options, constants.REGISTERS_NAMES[0])
        self.options_area.addTab(self.radiation_control_register_options, constants.REGISTERS_NAMES[1])
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

        i = 0            # кнопки внизу !!
        for _ in (self.save, self.clear):
            _.setIconSize(constants.SIZE_ICON)
            _.setFlat(True)
            _.setAutoDefault(True)
            self.box.addWidget(_, i, 2, alignment=constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        self.box.addWidget(self.base_register_area, 0, 0, 5, 1, alignment=constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.options_area, 0, 1, 5, 1, alignment=constants.ALIGNMENT_TOP_LEFT)

    def save_physical_protocol(self):
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
        self.base_register_area.entry_objects_others[0].clear()


class CalculatorObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(900, 400)

        self.box = QtWidgets.QGridLayout(self)
        self.box.setSpacing(15)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_ALL_OBJECTS)
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.calcs_area = QtWidgets.QTabWidget(self)
        self.calcs_area.setCurrentIndex(0)
        self.calcs_area.setDocumentMode(True)
        self.calcs_area.setUsesScrollButtons(False)
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

        i = 1
        for _ in (self.calculate, self.clear, self.save):
            _.setIconSize(constants.SIZE_ICON)
            _.setFlat(True)
            _.setAutoDefault(True)
            self.box.addWidget(_, i, 1, alignment=constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        self.calcs_area.addTab(self.air_calc, constants.CALCULATORS_NAMES[0])
        self.calcs_area.addTab(self.work_area_calc, constants.CALCULATORS_NAMES[1])
        self.calcs_area.addTab(self.flow_calc, constants.CALCULATORS_NAMES[2])
        self.calcs_area.addTab(self.noise_calc, constants.CALCULATORS_NAMES[3])
        self.box.addWidget(self.calcs_area, 0, 0, 6, 1, alignment=constants.ALIGNMENT_TOP_LEFT)

    @staticmethod
    def clear_entry_fields(entry_objects):
        for _ in entry_objects:
            _.clear()
            _.value = None

    @staticmethod
    def create_data_to_save(title_names, entry_fields, result):
        data = []
        for i in range(len(title_names)):
            data.append(title_names[i] + ': ' + str(entry_fields[i].get_entry_value()) + '\n')

        data.append(result.text() + constants.SEPARATOR)
        return data

    @staticmethod
    def create_noise_calc_data_to_save(bands, source, background, delta, correct):     # переделать запись в файл !!!!!!!
        data = []
        for i in range(10):
            band_str = (bands[i] + '   |   ')
            data.append(band_str)
            data.append('\n')
            source_str = (str(source[i].get_entry_value()) + '      ')
            data.append(source_str)
            data.append('\n')
            background_str = (str(background[i].get_entry_value()) + '      ')
            data.append(background_str)
            data.append('\n')
            delta_str = (delta[i].text() + '      ')
            data.append(delta_str)
            data.append('\n')
            correct_str = (correct[i].text() + '      ')
            data.append(correct_str)
            data.append(constants.SEPARATOR)
        return data

    @staticmethod
    def save_to_desktop(file, data):
        file_path = get_desktop() + file
        with open (file_path, "a", encoding="utf-8") as txt:
            txt.writelines(data)

    def show_saving_message(self, file_name):
        message = 'in dict' + file_name
        QtWidgets.QMessageBox.information(self, " ", message)

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
                    self.show_saving_message(constants.CALCS_RESULT_FILES[0])
                    air_calc_data = self.create_data_to_save(constants.ATMOSPHERIC_CALC_DUST_TITLE_NAMES,
                                    self.air_calc.entry_objects, self.air_calc.result_area)
                    self.save_to_desktop(constants.ATMOSPHERIC_CALC_RESULT_PATH, air_calc_data)
                else: pass
            case 1:
                if self.work_area_calc.result_area.text() != "":
                    self.show_saving_message(constants.CALCS_RESULT_FILES[1])
                    work_area_calc_data = self.create_data_to_save(constants.WORK_AREA_CALC_DUST_TITLE_NAMES,
                                          self.work_area_calc.entry_objects, self.work_area_calc.result_area)
                    self.save_to_desktop(constants.WORK_AREA_CALC_RESULT_PATH, work_area_calc_data)
                else: pass
            case 2:
                if self.flow_calc.result_area.text() != "":
                    self.show_saving_message(constants.CALCS_RESULT_FILES[2])
                    flow_calc_data = self.create_data_to_save(constants.VENTILATION_CALC_TITLE_NAMES,
                                     self.flow_calc.entry_objects, self.flow_calc.result_area)
                    self.save_to_desktop(constants.VENTILATION_CALC_RESULT_PATH, flow_calc_data)
                else: pass
            case 3:
                if self.noise_calc.delta_result_area[0].text() != "":
                    self.show_saving_message(constants.CALCS_RESULT_FILES[3])
                    noise_calc_data = self.create_noise_calc_data_to_save(constants.NOISE_CALC_BANDLINE_NAMES,
                                      self.noise_calc.entry_objects_source, self.noise_calc.entry_objects_background,
                                      self.noise_calc.delta_result_area, self.noise_calc.correct_result_area)
                    self.save_to_desktop(constants.NOISE_CALC_RESULT_PATH, noise_calc_data)
                else: pass


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

        self.box = QtWidgets.QGridLayout(self)
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(15)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_NULLS)

        self.menu_area = self.create_main_menu()
        self.selector_area = self.create_selector_panel()
        self.registers = RegisterObjectsController(self)
        self.calculators = CalculatorObjectsController(self)
        self.registers.close()

        self.box.addWidget(self.menu_area, 0, 0, 1, 6)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.calculators, 1, 2, 1, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.setColumnMinimumWidth(0, 1)
        self.box.setColumnMinimumWidth(3, 40)
        self.box.setColumnMinimumWidth(5, 40)

        self.calcs_list = (self.calculators.air_calc, self.calculators.work_area_calc, self.calculators.flow_calc,
                           self.calculators.noise_calc)

        self.set_app_style(constants.TYPE_LIGHT_STYLE)
        self.show()

    def set_app_style(self, style_list):
        self.setStyleSheet(style_list[0])
        self.selector_area.setStyleSheet(style_list[1])
        self.calculators.calcs_area.setStyleSheet(style_list[2])

        for _ in self.calcs_list:
            _.setStyleSheet(style_list[3])
            if self.calcs_list.index(_) == 3:
                _.set_result_field_style(style_list[4])
            else:
                _.result_area.setStyleSheet(style_list[4])

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        main_menu.setFixedHeight(20)
        main_menu.submenu_file = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[0], main_menu)
        main_menu.submenu_view = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[1], main_menu)
        main_menu.submenu_help = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[2], main_menu)

        main_menu.addMenu(main_menu.submenu_file)
        main_menu.addMenu(main_menu.submenu_view)
        main_menu.addMenu(main_menu.submenu_help)

        main_menu.set_calculators_act = QtGui.QAction(constants.SELECTOR_PANEL_TITLE_NAMES[0], main_menu.submenu_file)
        main_menu.set_calculators_act.triggered.connect(self.calculators_show_fixed)

        main_menu.set_registers_act = QtGui.QAction(constants.SELECTOR_PANEL_TITLE_NAMES[1], main_menu.submenu_file)
        main_menu.set_registers_act.triggered.connect(self.registers_show_fixed)

        main_menu.exit_act = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[3], main_menu.submenu_file)
        main_menu.exit_act.triggered.connect(sys.exit)

        main_menu.submenu_file.addAction(main_menu.set_registers_act)
        main_menu.submenu_file.addAction(main_menu.set_calculators_act)
        main_menu.submenu_file.addSeparator()
        main_menu.submenu_file.addAction(main_menu.exit_act)

        main_menu.themes = main_menu.submenu_view.addMenu(constants.MAIN_MENU_TITLE_NAMES[4])
        main_menu.dark = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[5], main_menu.themes)
        # dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        main_menu.light = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[6], main_menu.themes)
        # light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))
        main_menu.themes.addAction(main_menu.dark)
        main_menu.themes.addSeparator()
        main_menu.themes.addAction(main_menu.light)

        main_menu.help_link = QtGui.QAction(constants.HELP_INFO_MESSAGE[0], main_menu.submenu_help)
        main_menu.help_link.triggered.connect(self.open_help_message)

        main_menu.about = QtGui.QAction(constants.ABOUT_INFO_MESSAGE[0], main_menu.submenu_help)
        main_menu.about.triggered.connect(self.open_about_app_message)

        main_menu.submenu_help.addAction(main_menu.help_link)
        main_menu.submenu_help.addSeparator()
        main_menu.submenu_help.addAction(main_menu.about)

        return main_menu

    def create_selector_panel(self):
        selector_panel = QtWidgets.QListView(self)
        selector_panel.setFixedSize(constants.SIZE_SELECTOR_AREA)
        selector_panel.setSpacing(10)
        selector_panel.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        selector_panel.names = (constants.SELECTOR_PANEL_TITLE_NAMES[0], constants.SELECTOR_PANEL_TITLE_NAMES[1])
        selector_panel.model_type = QtCore.QStringListModel(selector_panel.names)
        selector_panel.setModel(selector_panel.model_type)
        selector_panel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        selector_panel.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        selector_panel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        selector_panel.setTabKeyNavigation(True)
        selector_panel.calculators_index = selector_panel.model_type.index(0, 0)
        selector_panel.registers_index = selector_panel.model_type.index(1, 0)
        selector_panel.clicked.connect(self.click_on_selector_panel)
        return selector_panel

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, constants.ABOUT_INFO_MESSAGE[0], constants.ABOUT_INFO_MESSAGE[1])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, constants.HELP_INFO_MESSAGE[0], constants.HELP_INFO_MESSAGE[1])

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
        if self.selector_area.currentIndex() == self.selector_area.calculators_index:
            self.calculators_show_fixed()
        else:
            self.registers_show_fixed()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon("images/calc_type.ico"))
    print(constants.main_interface["Справка"])
    app_type = ApplicationType()
    sys.exit(app.exec())
