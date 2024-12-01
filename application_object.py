from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import constants
from calculators_objects import (AtmosphericAirDust, WorkAreaAirDust, VentilationEfficiency, NoiseLevelsWithBackground,
                                 BaseRegister, PhysicalFactorsOptions, RadiationControlOptions)


class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(20)
        self.submenu_file = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[0], self)
        self.submenu_view = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[1], self)
        self.submenu_help = QtWidgets.QMenu(constants.MAIN_MENU_TITLE_NAMES[2], self)

        self.addMenu(self.submenu_file)
        self.addMenu(self.submenu_view)
        self.addMenu(self.submenu_help)

        self.set_registers_act = QtGui.QAction(constants.SELECTOR_PANEL_TITLE_NAMES[1], self.submenu_file)
        self.set_calculators_act = QtGui.QAction(constants.SELECTOR_PANEL_TITLE_NAMES[0], self.submenu_file)

        self.exit_act = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[3], self.submenu_file)
        self.exit_act.triggered.connect(sys.exit)

        self.submenu_file.addAction(self.set_registers_act)
        self.submenu_file.addAction(self.set_calculators_act)
        self.submenu_file.addSeparator()
        self.submenu_file.addAction(self.exit_act)

        self.themes = self.submenu_view.addMenu(constants.MAIN_MENU_TITLE_NAMES[4])
        self.dark = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[5], self.themes)
        #dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        self.light = QtGui.QAction(constants.MAIN_MENU_TITLE_NAMES[6], self.themes)
        #light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))
        self.themes.addAction(self.dark)
        self.themes.addSeparator()
        self.themes.addAction(self.light)

        self.help_link = QtGui.QAction(constants.HELP_INFO_MESSAGE[0], self.submenu_help)
        self.help_link.triggered.connect(self.open_help_message)

        self.about = QtGui.QAction(constants.ABOUT_INFO_MESSAGE[0], self.submenu_help)
        self.about.triggered.connect(self.open_about_app_message)

        self.submenu_help.addAction(self.help_link)
        self.submenu_help.addSeparator()
        self.submenu_help.addAction(self.about)

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, constants.ABOUT_INFO_MESSAGE[0], constants.ABOUT_INFO_MESSAGE[1])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, constants.HELP_INFO_MESSAGE[0], constants.HELP_INFO_MESSAGE[1])


class SelectorPanel(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(constants.SIZE_SELECTOR_AREA)
        self.setSpacing(10)
        self.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)

        self.names = (constants.SELECTOR_PANEL_TITLE_NAMES[0], constants.SELECTOR_PANEL_TITLE_NAMES[1])

        self.model_type = QtCore.QStringListModel(self.names)
        self.setModel(self.model_type)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.setTabKeyNavigation(True)

        self.calculators_index = self.model_type.index(0, 0)
        self.registers_index = self.model_type.index(1, 0)


class CalculatorObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(900, 400)

        self.box = QtWidgets.QGridLayout(self)
        self.box.setSpacing(15)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_ALL_OBJECTS)

        self.icon_size = QtCore.QSize(40, 40)
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')       # Сделать круглые

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
        for button in (self.calculate, self.clear, self.save):
            button.setIconSize(self.icon_size)
            button.setFlat(True)
            button.setAutoDefault(True)
            self.box.addWidget(button, i, 1, alignment=constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        self.calcs_area.addTab(self.air_calc, constants.CALCULATORS_NAMES[0])
        self.calcs_area.addTab(self.work_area_calc, constants.CALCULATORS_NAMES[1])
        self.calcs_area.addTab(self.flow_calc, constants.CALCULATORS_NAMES[2])
        self.calcs_area.addTab(self.noise_calc, constants.CALCULATORS_NAMES[3])
        self.box.addWidget(self.calcs_area, 0, 0, 6, 1, alignment=constants.ALIGNMENT_TOP_LEFT)

    @staticmethod
    def clear_entry_fields(entry_objects):
        for clear in entry_objects:
            clear.clear()
            clear.value = None

    @staticmethod
    def create_data_to_save(title_names, entry_fields, result):
        data = []

        i = 0
        for string in range(len(title_names)):
            string = title_names[i] + ': ' + str(entry_fields[i].get_entry_value()) + '\n'
            data.append(string)
            i += 1

        data.append(result.text() + constants.SEPARATOR)
        return data

    @staticmethod
    def create_noise_calc_data_to_save(bands, source, background, delta, correct):
        data = []

        i = 0
        while i < 10:
            band_str = (bands[i] + '   |   ')
            data.append(band_str)
            i += 1
        data.append('\n')

        i = 0
        while i < 10:
            source_str = (str(source[i].get_entry_value()) + '      ')
            data.append(source_str)
            i += 1
        data.append('\n')

        i = 0
        while i < 10:
            background_str = (str(background[i].get_entry_value()) + '      ')
            data.append(background_str)
            i += 1
        data.append('\n')

        i = 0
        while i < 10:
            delta_str = (delta[i].text() + '      ')
            data.append(delta_str)
            i += 1
        data.append('\n')

        i = 0
        while i < 10:
            correct_str = (correct[i].text() + '      ')
            data.append(correct_str)
            i += 1
        data.append(constants.SEPARATOR)

        return data

    @staticmethod
    def save_to_desktop(file_path, data):
        with open (file_path, "a", encoding="utf-8") as txt:
            txt.writelines(data)

    def show_saving_message(self, file_name):
        message = "Данные рассчета будут сохранены\nна рабочий стол в файл " + file_name
        QtWidgets.QMessageBox.information(self, " ", message)

    def show_error_message(self):
        QtWidgets.QMessageBox.warning(self, " ", "Ошибка. Введите значения !",
                                      defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)

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
            self.show_error_message()

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
                self.show_saving_message(constants.CALCS_RESULT_FILES[0])
                air_calc_data = self.create_data_to_save(constants.ATMOSPHERIC_CALC_DUST_TITLE_NAMES,
                                self.air_calc.entry_objects, self.air_calc.result_area)
                self.save_to_desktop(constants.ATMOSPHERIC_CALC_RESULT_PATH, air_calc_data)
            case 1:
                self.show_saving_message(constants.CALCS_RESULT_FILES[1])
                work_area_calc_data = self.create_data_to_save(constants.WORK_AREA_CALC_DUST_TITLE_NAMES,
                                      self.work_area_calc.entry_objects, self.work_area_calc.result_area)
                self.save_to_desktop(constants.WORK_AREA_CALC_RESULT_PATH, work_area_calc_data)
            case 2:
                self.show_saving_message(constants.CALCS_RESULT_FILES[2])
                flow_calc_data = self.create_data_to_save(constants.VENTILATION_CALC_TITLE_NAMES,
                                 self.flow_calc.entry_objects, self.flow_calc.result_area)
                self.save_to_desktop(constants.VENTILATION_CALC_RESULT_PATH, flow_calc_data)
            case 3:
                self.show_saving_message(constants.CALCS_RESULT_FILES[3])

                noise_calc_data = self.create_noise_calc_data_to_save(constants.NOISE_CALC_BANDLINE_NAMES,
                                  self.noise_calc.entry_objects_source, self.noise_calc.entry_objects_background,
                                  self.noise_calc.delta_result_area, self.noise_calc.correct_result_area)
                self.save_to_desktop(constants.NOISE_CALC_RESULT_PATH, noise_calc_data)


class RegisterObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize()

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_ALL_OBJECTS)
        self.box.setSpacing(40)

        self.icon_size = QtCore.QSize(40, 40)
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

        i = 0
        for button in (self.save, self.clear):
            button.setIconSize(self.icon_size)
            button.setFlat(True)
            button.setAutoDefault(True)
            self.box.addWidget(button, i, 2, alignment=constants.ALIGNMENT_LEFT_CENTER)
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
        for base_entry_object in self.base_register_area.entry_objects:
            base_entry_object.clear()

        for physical_entry_object in self.physical_register_options.entry_objects:
            physical_entry_object.clear()

        for radiation_entry_object in self.radiation_control_register_options.entry_objects:
            radiation_entry_object.clear()

    @QtCore.pyqtSlot()
    def clear_protocol_number_entry_field(self):
        self.base_register_area.entry_objects[2].clear()

'''@QtCore.pyqtSlot()
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
                                      colors_list[9] + "}")'''


class LaboratorySystem(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.resize(900, 600)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setHorizontalSpacing(10)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_NULLS)

        self.registers_set = RegisterObjectsController(self)
        self.calculators_set = CalculatorObjectsController(self)
        self.registers_set.close()

        self.main_menu_area = MainMenu(self)
        self.main_menu_area.set_calculators_act.triggered.connect(self.calculators_show_fixed)
        self.main_menu_area.set_registers_act.triggered.connect(self.registers_show_fixed)

        self.selector_area = SelectorPanel(self)
        self.selector_area.clicked.connect(self.click_on_selector_panel)

        self.box.addWidget(self.main_menu_area, 0, 0, 1, 5)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.calculators_set, 1, 2, 1, 1, constants.ALIGNMENT_TOP_LEFT)
        self.box.setColumnMinimumWidth(0, 1)
        self.box.setColumnMinimumWidth(3, 40)
        self.box.setColumnMinimumWidth(5, 40)

    @QtCore.pyqtSlot()
    def calculators_show_fixed(self):
        self.registers_set.close()
        self.box.replaceWidget(self.registers_set, self.calculators_set)
        self.calculators_set.show()

    @QtCore.pyqtSlot()
    def registers_show_fixed(self):
        self.calculators_set.close()
        self.box.replaceWidget(self.calculators_set, self.registers_set)
        self.registers_set.show()

    @QtCore.pyqtSlot()
    def click_on_selector_panel(self):
        if self.selector_area.currentIndex() == self.selector_area.calculators_index:
            self.calculators_show_fixed()
        else:
            self.registers_show_fixed()


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

        self.application_area = LaboratorySystem(self)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_NULLS)
        self.box.addWidget(self.application_area, alignment=constants.ALIGNMENT_TOP_LEFT)

        self.setStyleSheet("font: 13px arial, sans-serif")

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon("images/calc_type.ico"))
    app_type = ApplicationType()
    sys.exit(app.exec())
