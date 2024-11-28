from PyQt6 import QtWidgets, QtCore, QtGui
import sys

from constants import (MAIN_MENU_TITLE_NAMES, SELECTOR_PANEL_TITLE_NAMES, HELP_INFO_MESSAGE, ABOUT_INFO_MESSAGE,
                       SIZE_SELECTOR_AREA, CALCULATORS_NAMES, ALIGNMENT_TOP_LEFT, CONTENTS_MARGINS_ALL_OBJECTS,
                       REGISTERS_NAMES, ALIGNMENT_TOP_RIGHT, CONTENTS_MARGINS_NULLS, CALCS_RESULT_FILES,
                       ATMOSPHERIC_CALC_RESULT_PATH, WORK_AREA_CALC_RESULT_PATH, VENTILATION_CALC_RESULT_PATH,
                       NOISE_CALC_RESULT_PATH, ATMOSPHERIC_CALC_DUST_TITLE_NAMES, WORK_AREA_CALC_DUST_TITLE_NAMES,
                       VENTILATION_CALC_TITLE_NAMES, NOISE_CALC_BANDLINE_NAMES)

import calculators_objects
import registers_objects


class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(20)
        self.submenu_file = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[0], self)
        self.submenu_edit = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[1], self)
        self.submenu_view = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[2], self)
        self.submenu_help = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[3], self)

        self.addMenu(self.submenu_file)
        self.addMenu(self.submenu_edit)
        self.addMenu(self.submenu_view)
        self.addMenu(self.submenu_help)

        self.set_registers_act = QtGui.QAction(SELECTOR_PANEL_TITLE_NAMES[0], self.submenu_file)
        self.set_calculators_act = QtGui.QAction(SELECTOR_PANEL_TITLE_NAMES[1], self.submenu_file)

        self.exit_act = QtGui.QAction(MAIN_MENU_TITLE_NAMES[4], self.submenu_file)
        self.exit_act.triggered.connect(sys.exit)

        self.submenu_file.addAction(self.set_registers_act)
        self.submenu_file.addAction(self.set_calculators_act)
        self.submenu_file.addSeparator()
        self.submenu_file.addAction(self.exit_act)

        self.themes = self.submenu_view.addMenu(MAIN_MENU_TITLE_NAMES[5])
        self.dark = QtGui.QAction(MAIN_MENU_TITLE_NAMES[6], self.themes)
        #dark_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.DARK_COLORS))
        self.light = QtGui.QAction(MAIN_MENU_TITLE_NAMES[7], self.themes)
        #light_style.triggered.connect(partial(self.set_app_style, ApplicationWindow.LIGHT_COLORS))
        self.themes.addAction(self.dark)
        self.themes.addSeparator()
        self.themes.addAction(self.light)

        self.help_link = QtGui.QAction(HELP_INFO_MESSAGE[0], self.submenu_help)
        self.help_link.triggered.connect(self.open_help_message)

        self.about = QtGui.QAction(ABOUT_INFO_MESSAGE[0], self.submenu_help)
        self.about.triggered.connect(self.open_about_app_message)

        self.submenu_help.addAction(self.help_link)
        self.submenu_help.addSeparator()
        self.submenu_help.addAction(self.about)

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, ABOUT_INFO_MESSAGE[0], ABOUT_INFO_MESSAGE[1])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, HELP_INFO_MESSAGE[0], HELP_INFO_MESSAGE[1])


class SelectorPanel(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(SIZE_SELECTOR_AREA)
        self.setSpacing(10)
        self.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)

        self.names = (SELECTOR_PANEL_TITLE_NAMES[0], SELECTOR_PANEL_TITLE_NAMES[1])

        self.model_type = QtCore.QStringListModel(self.names)
        self.setModel(self.model_type)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.setTabKeyNavigation(True)

        self.registers_index = self.model_type.index(0, 0)
        self.calculators_index = self.model_type.index(1, 0)


class MainControlField(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(80, 300)
        self.icon_size = QtCore.QSize(35, 35)

        self.icon_change_style = QtGui.QIcon('images/style.ico')     #  Круглые углы !!!
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.icon_exit = QtGui.QIcon('images/exit.ico')

        self.button_change_style = QtWidgets.QPushButton(self)
        self.button_change_style.setIcon(self.icon_change_style)

        self.button_ok = QtWidgets.QPushButton(self)
        self.button_ok.setIcon(self.icon_ok)
        self.button_ok.setEnabled(False)

        self.button_clear = QtWidgets.QPushButton(self)
        self.button_clear.setIcon(self.icon_clear)

        self.button_save = QtWidgets.QPushButton(self)
        self.button_save.setIcon(self.icon_save)

        self.button_exit = QtWidgets.QPushButton(self)
        self.button_exit.setIcon(self.icon_exit)
        self.button_exit.clicked.connect(sys.exit)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(5)
        self.box.setContentsMargins(CONTENTS_MARGINS_NULLS)

        for button in (self.button_change_style, self.button_ok, self.button_clear, self.button_save, self.button_exit):
            button.setIconSize(self.icon_size)
            button.setFlat(True)
            button.setAutoDefault(True)
            self.box.addWidget(button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)


class CalculatorObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(900, 400)
        self.tab_area = QtWidgets.QTabWidget(self)
        self.tab_area.setCurrentIndex(0)
        self.tab_area.setDocumentMode(True)
        #self.tab_area.currentChanged.connect(self.clear_result_area)

        self.air_calc = calculators_objects.AtmosphericAirDust()
        self.work_area_calc = calculators_objects.WorkAreaAirDust()
        self.flow_calc = calculators_objects.VentilationEfficiency()
        self.noise_calc = calculators_objects.NoiseLevelsWithBackground()

        self.tab_area.addTab(self.air_calc, CALCULATORS_NAMES[0])
        self.tab_area.addTab(self.work_area_calc, CALCULATORS_NAMES[1])
        self.tab_area.addTab(self.flow_calc, CALCULATORS_NAMES[2])
        self.tab_area.addTab(self.noise_calc, CALCULATORS_NAMES[3])

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.tab_area, alignment=ALIGNMENT_TOP_LEFT)

    def clear_entry_fields(self, entry_objects):
        for clear in entry_objects:
            clear.clear()
            clear.value = None
        #self.result_area.clear()

    def create_data_to_save(self, title_names, entry_fields, result_string):
        data = ["\n----------------------------------------------------------------------\n"]

        i = 0
        for string in range(len(title_names)):
            string = title_names[i] + ': ' + str(entry_fields[i].get_entry_value()) + '\n'
            data.append(string)
            i += 1
        data.append(result_string)

        return data

    def save_to_desktop(self, file_path, data):
        with open (file_path, "a", encoding="utf-8") as txt:
            txt.writelines(data)

    def show_saving_message(self, file_name):
        message = "Данные рассчета будут сохранены\nна рабочий стол в файл " + file_name
        QtWidgets.QMessageBox.information(self, "Сохранение", message)

    def show_error_message(self):
        QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите значения !",
                                      defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)

    @QtCore.pyqtSlot()
    def calculating(self):
        try:
            match self.tab_area.currentIndex():
                case 0:
                    self.air_calc.calculate()
                    #self.result_area.setText(self.air_calc.get_result())
                case 1:
                    self.work_area_calc.calculate()
                    #self.result_area.setText(self.work_area_calc.get_result())
                case 2:
                    self.flow_calc.calculate()
                    #self.result_area.setText(self.flow_calc.get_result())
                case 3:
                    self.noise_calc.calculate()
                    #self.result_area.setText(self.noise_calc.get_result())
        except TypeError:
            self.show_error_message()

    @QtCore.pyqtSlot()
    def clear_calculator(self):
        match self.tab_area.currentIndex():
            case 0:
                self.clear_entry_fields(self.air_calc.entry_objects)
            case 1:
                self.clear_entry_fields(self.work_area_calc.entry_objects)
            case 2:
                self.clear_entry_fields(self.flow_calc.entry_objects)
            case 3:
                self.clear_entry_fields(self.noise_calc.entry_objects)

    '''@QtCore.pyqtSlot()
    def clear_result_area(self):
        if self.result_area.text():
            self.result_area.clear()'''

    @QtCore.pyqtSlot()
    def saving(self):
        match self.tab_area.currentIndex():
            case 0:
                self.show_saving_message(CALCS_RESULT_FILES[0])

                air_calc_data = self.create_data_to_save(ATMOSPHERIC_CALC_DUST_TITLE_NAMES, self.air_calc.entry_objects,
                                self.air_calc.get_result())
                self.save_to_desktop(ATMOSPHERIC_CALC_RESULT_PATH, air_calc_data)
            case 1:
                self.show_saving_message(CALCS_RESULT_FILES[1])

                work_area_calc_data = self.create_data_to_save(WORK_AREA_CALC_DUST_TITLE_NAMES,
                                      self.work_area_calc.entry_objects, self.work_area_calc.get_result())
                self.save_to_desktop(WORK_AREA_CALC_RESULT_PATH, work_area_calc_data)
            case 2:
                self.show_saving_message(CALCS_RESULT_FILES[2])

                flow_calc_data = self.create_data_to_save(VENTILATION_CALC_TITLE_NAMES, self.flow_calc.entry_objects,
                                 self.flow_calc.get_result())
                self.save_to_desktop(VENTILATION_CALC_RESULT_PATH, flow_calc_data)
            case 3:
                self.show_saving_message(CALCS_RESULT_FILES[3])

                self.clear_entry_fields(self.noise_calc.entry_objects) # !!!!!!!!!!!


class RegisterObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize()
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(CONTENTS_MARGINS_ALL_OBJECTS)
        self.box.setSpacing(40)

        self.base_register_area = registers_objects.BaseRegister()
        self.options_area = QtWidgets.QTabWidget(self)
        self.options_area.setDocumentMode(True)
        self.options_area.setCurrentIndex(0)
        self.options_area.currentChanged.connect(self.clear_protocol_number_entry_field)

        self.physical_register_options = registers_objects.PhysicalFactorsOptions()
        self.radiation_control_register_options = registers_objects.RadiationControlOptions()

        self.options_area.addTab(self.physical_register_options, REGISTERS_NAMES[0])
        self.options_area.addTab(self.radiation_control_register_options, REGISTERS_NAMES[1])

        self.box.addWidget(self.base_register_area, alignment=ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.options_area, alignment=ALIGNMENT_TOP_LEFT)

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

        for query in queries_list:
            check = query.exec()
            if check:
                print('Ok!')
            else:
                print('Bad!')

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

        for query in queries_list:
            check = query.exec()
            if check:
                print('Ok!')
            else:
                print('Bad!')

        self.base_register_area.connection_with_database.close()

    @QtCore.pyqtSlot()
    def select_insert_command(self):
        match self.options_area.currentIndex():
            case 0:
                self.save_physical_protocol()
            case 1:
                self.save_radiation_protocol()

    @QtCore.pyqtSlot()
    def clear_protocol_number_entry_field(self):
        self.base_register_area.protocol_number.clear()

    @QtCore.pyqtSlot()
    def clear_registers_values(self):
        for base_entry_object in self.base_register_area.entry_objects:
            base_entry_object.clear()

        for physical_entry_object in self.physical_register_options.entry_objects:
            physical_entry_object.clear()

        for radiation_entry_object in self.radiation_control_register_options.entry_objects:
            radiation_entry_object.clear()


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
        self.box.setContentsMargins(CONTENTS_MARGINS_NULLS)

        self.registers_set = RegisterObjectsController(self)
        self.calculators_set = CalculatorObjectsController(self)
        self.calculators_set.close()

        self.main_menu_area = MainMenu(self)
        self.main_menu_area.set_calculators_act.triggered.connect(self.calculators_set_menu_slot)
        self.main_menu_area.set_registers_act.triggered.connect(self.registers_set_menu_slot)

        self.selector_area = SelectorPanel(self)
        self.selector_area.clicked.connect(self.click_on_string)
        self.selector_area.clicked.connect(self.set_a_control_buttons_activity)

        self.control_area = MainControlField(self)
        #self.control_area.button_save.clicked.connect(self.registers_set.select_insert_command)
        self.control_area.button_save.clicked.connect(self.calculators_set.saving)
        self.control_area.button_clear.clicked.connect(self.registers_set.clear_registers_values)

        self.box.addWidget(self.main_menu_area, 0, 0, 1, 5)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.registers_set, 1, 2, 1, 1, ALIGNMENT_TOP_LEFT)
        self.box.addWidget(self.control_area, 1, 4, 1, 1, ALIGNMENT_TOP_RIGHT)
        self.box.setColumnMinimumWidth(0, 1)
        self.box.setColumnMinimumWidth(3, 40)
        self.box.setColumnMinimumWidth(5, 40)

    def calculators_set_show_fixed(self):
        self.registers_set.close()
        self.box.replaceWidget(self.registers_set, self.calculators_set)
        self.calculators_set.show()

    def registers_set_show_fixed(self):
        self.calculators_set.close()
        self.box.replaceWidget(self.calculators_set, self.registers_set)
        self.registers_set.show()

    def calculators_set_control_buttons_fixed(self):
        self.control_area.button_clear.disconnect()
        self.control_area.button_save.setEnabled(True)     # !!!!!!
        self.control_area.button_ok.setEnabled(True)
        self.control_area.button_ok.clicked.connect(self.calculators_set.calculating)
        self.control_area.button_clear.clicked.connect(self.calculators_set.clear_calculator)

    def registers_set_control_buttons_fixed(self):
        self.control_area.button_clear.disconnect()
        self.control_area.button_ok.setEnabled(False)
        self.control_area.button_save.setEnabled(True)
        self.control_area.button_clear.clicked.connect(self.registers_set.clear_registers_values)

    @QtCore.pyqtSlot()
    def set_a_control_buttons_activity(self):
        if self.selector_area.currentIndex() == self.selector_area.calculators_index:
            self.calculators_set_control_buttons_fixed()
        else:
            self.registers_set_control_buttons_fixed()

    @QtCore.pyqtSlot()
    def click_on_string(self):          # New name !!
        if self.selector_area.currentIndex() == self.selector_area.calculators_index:
            self.calculators_set_show_fixed()
        else:
            self.registers_set_show_fixed()

    @QtCore.pyqtSlot()
    def calculators_set_menu_slot(self):
        self.calculators_set_control_buttons_fixed()
        self.calculators_set_show_fixed()

    @QtCore.pyqtSlot()
    def registers_set_menu_slot(self):
        self.registers_set_control_buttons_fixed()
        self.registers_set_show_fixed()


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
        self.box.setContentsMargins(CONTENTS_MARGINS_NULLS)
        self.box.addWidget(self.application_area, alignment=ALIGNMENT_TOP_LEFT)

        self.setStyleSheet("font: 13px arial, sans-serif")

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon("images/calc_type.ico"))
    app_type = ApplicationType()
    sys.exit(app.exec())
