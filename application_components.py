from PyQt6 import QtWidgets, QtCore, QtGui
import sys

from constants import (MAIN_MENU_TITLE_NAMES, SELECTOR_PANEL_TITLE_NAMES, HELP_INFO_MESSAGE, ABOUT_INFO_MESSAGE,
                       SIZE_SELECTOR_AREA, CALCULATORS_NAMES, ALIGNMENT_TOP_LEFT, CONTENTS_MARGINS_ALL_OBJECTS,
                       REGISTERS_NAMES)

from application_classes import ResultField
import calculators_objects
import registers_objects


class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.submenu_file = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[0], self)
        self.submenu_edit = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[1], self)
        self.submenu_view = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[2], self)
        self.submenu_help = QtWidgets.QMenu(MAIN_MENU_TITLE_NAMES[3], self)

        self.addMenu(self.submenu_file)
        self.addMenu(self.submenu_edit)
        self.addMenu(self.submenu_view)
        self.addMenu(self.submenu_help)

        self.set_calculators_act = QtGui.QAction(SELECTOR_PANEL_TITLE_NAMES[0], self.submenu_file)
        # signals !!
        self.set_magazines_act = QtGui.QAction(SELECTOR_PANEL_TITLE_NAMES[1], self.submenu_file)

        self.exit_act = QtGui.QAction(MAIN_MENU_TITLE_NAMES[4], self.submenu_file)
        self.exit_act.triggered.connect(sys.exit)

        self.submenu_file.addAction(self.set_calculators_act)
        self.submenu_file.addAction(self.set_magazines_act)
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
        self.names = (SELECTOR_PANEL_TITLE_NAMES[0], SELECTOR_PANEL_TITLE_NAMES[1])

        self.model_type = QtCore.QStringListModel(self.names)

        self.setModel(self.model_type)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSpacing(10)
        self.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        self.setTabKeyNavigation(True)
        self.setFixedSize(SIZE_SELECTOR_AREA)

        self.calculators_index = self.model_type.index(0, 0)

        '''self.select_list.activated.connect(self.click_air_calc)
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
            self.noise_calc.show()'''


class CalculatorObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(900, 400)
        self.tab_area = QtWidgets.QTabWidget(self)
        self.tab_area.setCurrentIndex(0)
        self.tab_area.setDocumentMode(True)
        self.tab_area.currentChanged.connect(self.clear_result_area)

        self.result_area = ResultField(self)

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
        self.box.addWidget(self.result_area, alignment=ALIGNMENT_TOP_LEFT)

    @QtCore.pyqtSlot()
    def select_calculate_object(self):
        try:
            match self.tab_area.currentIndex():
                case 0:
                    self.air_calc.calculate()
                    self.result_area.setText(self.air_calc.get_result_text())
                case 1:
                    self.work_area_calc.calculate()
                    self.result_area.setText(self.work_area_calc.get_result_text())
                case 2:
                    self.flow_calc.calculate()
                    self.result_area.setText(self.flow_calc.get_result_text())
                case 3:
                    self.noise_calc.calculate()
                    self.result_area.setText(self.noise_calc.get_result_text())
        except TypeError:
            self.show_error_message()

    def clear_entry_fields(self, entry_objects):
        for clear in entry_objects:
            clear.clear()
            clear.value = None
        self.result_area.clear()

    @QtCore.pyqtSlot()
    def select_clear_object(self):
        match self.tab_area.currentIndex():
            case 0:
                self.clear_entry_fields(self.air_calc.entry_objects)
            case 1:
                self.clear_entry_fields(self.work_area_calc.entry_objects)
            case 2:
                self.clear_entry_fields(self.flow_calc.entry_objects)
            case 3:
                self.clear_entry_fields(self.noise_calc.entry_objects)

    @QtCore.pyqtSlot()
    def clear_result_area(self):
        if self.result_area.text():
            self.result_area.clear()

    def show_error_message(self):
        QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите значения !",
                                      defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)


class RegisterObjectsController(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize()
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(CONTENTS_MARGINS_ALL_OBJECTS)

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
     #  Проверка сохранения пустых значений !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        for entry_object in self.base_register_area.entry_objects:
            entry_object.clear()

        for entry_object in self.physical_register_options.entry_objects:
            entry_object.clear()

        for entry_object in self.radiation_control_register_options.entry_objects:
            entry_object.clear()


class MainControlField(QtWidgets.QWidget):  # methods ??
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(80, 300)
        self.icon_size = QtCore.QSize(35, 35)

        self.icon_change_style = QtGui.QIcon('images/style.ico')
        self.icon_ok = QtGui.QIcon('images/ok.ico')
        self.icon_clear = QtGui.QIcon('images/clear.ico')
        self.icon_save = QtGui.QIcon('images/save.ico')
        self.icon_copy = QtGui.QIcon('images/copy.ico')
        self.icon_exit = QtGui.QIcon('images/exit.ico')

        self.button_change_style = QtWidgets.QPushButton(self)
        self.button_change_style.setIcon(self.icon_change_style)
        self.button_change_style.setIconSize(self.icon_size)

        self.button_ok = QtWidgets.QPushButton(self)
        self.button_ok.setIcon(self.icon_ok)
        self.button_ok.setIconSize(self.icon_size)
        self.button_ok.setAutoDefault(True)

        self.button_clear = QtWidgets.QPushButton(self)
        self.button_clear.setIcon(self.icon_clear)
        self.button_clear.setIconSize(self.icon_size)
        #self.button_clear.setEnabled(False)
        self.button_clear.setAutoDefault(True)

        self.button_save = QtWidgets.QPushButton(self)
        self.button_save.setIcon(self.icon_save)
        self.button_save.setIconSize(self.icon_size)
        self.button_save.setAutoDefault(True)

        self.button_copy = QtWidgets.QPushButton(self)
        self.button_copy.setIcon(self.icon_copy)
        self.button_copy.setIconSize(self.icon_size)

        self.button_exit = QtWidgets.QPushButton(self)
        self.button_exit.setIcon(self.icon_exit)
        self.button_exit.setIconSize(self.icon_size)
        self.button_exit.clicked.connect(sys.exit)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(15)
        self.box.addWidget(self.button_change_style)
        self.box.addWidget(self.button_ok)
        self.box.addWidget(self.button_clear)
        self.box.addWidget(self.button_save)
        self.box.addWidget(self.button_copy)
        self.box.addWidget(self.button_exit)


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
