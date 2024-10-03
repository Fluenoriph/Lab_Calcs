from PyQt6 import QtWidgets, QtCore
from application_classes import EntryValueField, ResultField
import constants
import math
import locale


class AtmosphericAirDust(QtWidgets.QWidget):  # константы указаны не в классе ?
    def __init__(self):
        super().__init__()
        self.setFixedSize(constants.SIZE_AIR_CALC_OBJECT)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(40)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_CALC_OBJECTS)

        self.title_names = self.set_title_names()

        self.volume = EntryValueField(self)
        self.temperature = EntryValueField(self)
        self.pressure = EntryValueField(self)
        self.mass_before = EntryValueField(self)
        self.mass_after = EntryValueField(self)

        self.entry_objects = (self.volume, self.temperature, self.pressure, self.mass_before, self.mass_after)

        self.create_components()

        self.set_checking_value()

        self.but = QtWidgets.QPushButton(self)
        self.box.addWidget(self.but)
        self.but.clicked.connect(self.calculate)

        self.show()

    def set_title_names(self):
        return constants.ATMOSPHERIC_CALC_DUST_TITLE_NAMES

    def create_components(self):
        i = 0
        for title_object in range(len(self.title_names)):
            title_object = QtWidgets.QLabel(self.title_names[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 0
        for entry_object in self.entry_objects:
            entry_object.setFixedSize(constants.SIZE_OTHERS_ENTRY_OBJECTS)
            entry_object.setMaxLength(10)
            self.box.addWidget(entry_object, i, 1, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def set_checking_value(self):
        self.volume.check_entry_value()
        self.temperature.check_temperature_entry_value()
        self.pressure.check_entry_value()
        self.mass_before.check_entry_value()
        self.mass_after.check_entry_value()

    @QtCore.pyqtSlot()
    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value() / 1000
        temperature = self.temperature.get_entry_value()
        pressure = self.pressure.get_entry_value()
        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 273 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) / normal_volume
        concentrate = round(concentrate, 2)

        if concentrate < 0.15:
            print("low")  #self.fixed(constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[1])
        elif concentrate > 10.0:
            print("down")  #self.fixed(constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[2])
        else:
            delta = 0.110 * concentrate
            delta = round(delta, 2)
            rus_concentrate = locale.format_string("%.2f", concentrate)
            rus_delta = locale.format_string("%.2f", delta)
            result = f"{rus_concentrate} ± {rus_delta} мг/м³"

            print(result)

    ''''@QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear(self.parameter_list)
        self.result_frame.result_label.clear()
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)'''


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return constants.WORK_AREA_CALC_DUST_TITLE_NAMES

    @QtCore.pyqtSlot()
    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value()
        temperature = self.temperature.get_entry_value()
        pressure = self.pressure.get_entry_value()
        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 293 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) * 1000 / normal_volume
        concentrate = round(concentrate, 2)

        if concentrate < 1.0:
            print("low")  #self.result_frame.result_label.setText("менее 1,0 мг/м³")
        elif concentrate > 250.0:
            print("down")  #self.result_frame.result_label.setText("более 250 мг/м³")
        else:
            delta = 0.24 * concentrate
            delta = round(delta, 2)
            rus_concentrate = locale.format_string("%.2f", concentrate)
            rus_delta = locale.format_string("%.2f", delta)
            result = f"{rus_concentrate} ± {rus_delta} мг/м³"

            print(result)


class VentilationEfficiency(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(constants.SIZE_VENTILATION_CALC_OBJECT)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(40)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_CALC_OBJECTS)

        self.room_square = EntryValueField(self)
        self.room_height = EntryValueField(self)
        self.flow_speed = EntryValueField(self)
        self.diameter = EntryValueField(self)
        self.width = EntryValueField(self)
        self.height = EntryValueField(self)

        self.entry_objects = (self.room_square, self.room_height, self.flow_speed, self.diameter, self.width,
                              self.height)

        self.create_components()
        self.set_checking_value()

        self.show()

    def create_components(self):
        i = 0
        for title_object in range(len(constants.VENTILATION_CALC_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.VENTILATION_CALC_TITLE_NAMES[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 0
        for main_entry_object in self.entry_objects[0:3]:
            main_entry_object.setFixedSize(constants.SIZE_OTHERS_ENTRY_OBJECTS)
            self.box.addWidget(main_entry_object, i, 1, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        for holy_type_entry_object in self.entry_objects[3:6]:
            holy_type_entry_object.setFixedSize(constants.SIZE_HOLE_ENTRY_OBJECTS)
            self.box.addWidget(holy_type_entry_object, i, 1, constants.ALIGNMENT_CENTER_CENTER)
            i += 1

    def set_checking_value(self):
        for check in self.entry_objects:
            check.setMaxLength(7)
            check.check_entry_value()

    '''def lock_quad_frames(self):
        self.type_hole.toggle()
        self.parameter_list[4].setEnabled(False)
        self.parameter_list[5].setEnabled(False)
        self.parameter_list[3].setEnabled(True)

    def lock_diameter_frame(self):
        self.type_quad.toggle()
        self.parameter_list[3].setEnabled(False)
        self.parameter_list[4].setEnabled(True)
        self.parameter_list[5].setEnabled(True)'''

    @QtCore.pyqtSlot()
    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        room_square = self.room_square.get_entry_value()
        h = self.parameter_list[1].get_enter_value()
        speed = self.parameter_list[2].get_enter_value()
        try:
            if self.type_hole.isChecked():
                diameter = self.parameter_list[3].get_enter_value() / 100
                self.s_hole = (math.pi * pow(diameter, 2)) / 4
            if self.type_quad.isChecked():
                width = self.parameter_list[4].get_enter_value() / 100
                height = self.parameter_list[5].get_enter_value() / 100
                self.s_hole = width * height

            volume_room = s * h
            perfomance = speed * self.s_hole * 3600
        except TypeError:
            app_classes.ClearAndLockCalc.clear(self.parameter_list)
            app_classes.ErrorLabel(self)
        else:
            per_in_hour = perfomance / volume_room
            perfomance = round(perfomance, 1)
            per_in_hour = round(per_in_hour, 1)
            rus_perfomance = locale.format_string("%.1f", perfomance)
            rus_per_in_hour = locale.format_string("%.1f", per_in_hour)
            perfomance_result = f"{rus_perfomance} м³/ч"
            per_in_hour_result = f"{rus_per_in_hour} раз/ч"

            self.perfomance_frame.result_label.setText(perfomance_result)
            self.per_in_hour_frame.result_label.setText(per_in_hour_result)



    '''@QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear(self.parameter_list)
        self.perfomance_frame.result_label.clear()
        self.per_in_hour_frame.result_label.clear()
        self.lock_quad_frames()
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)'''


class NoiseLevelsWithBackground(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(constants.SIZE_NOISE_CALC_OBJECT)
        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(5)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_CALC_OBJECTS)

        self.band_31_source = EntryValueField(self)
        self.band_63_source = EntryValueField(self)
        self.band_125_source = EntryValueField(self)
        self.band_250_source = EntryValueField(self)
        self.band_500_source = EntryValueField(self)
        self.band_1k_source = EntryValueField(self)
        self.band_2k_source = EntryValueField(self)
        self.band_4k_source = EntryValueField(self)
        self.band_8k_source = EntryValueField(self)
        self.band_l_as_source = EntryValueField(self)

        self.band_31_background = EntryValueField(self)
        self.band_63_background = EntryValueField(self)
        self.band_125_background = EntryValueField(self)
        self.band_250_background = EntryValueField(self)
        self.band_500_background = EntryValueField(self)
        self.band_1k_background = EntryValueField(self)
        self.band_2k_background = EntryValueField(self)
        self.band_4k_background = EntryValueField(self)
        self.band_8k_background = EntryValueField(self)
        self.band_l_as_background = EntryValueField(self)

        self.entry_objects_source = (self.band_31_source, self.band_63_source, self.band_125_source,
                                     self.band_250_source, self.band_500_source, self.band_1k_source,
                                     self.band_2k_source, self.band_4k_source, self.band_8k_source,
                                     self.band_l_as_source)

        self.entry_objects_background = (self.band_31_background, self.band_63_background, self.band_125_background,
                                         self.band_250_background, self.band_500_background, self.band_1k_background,
                                         self.band_2k_background, self.band_4k_background, self.band_8k_background,
                                         self.band_l_as_background)

        self.create_and_check_components()

        self.show()

    def create_and_check_components(self):
        title_source = QtWidgets.QLabel(constants.NOISE_CALC_RESULT_NAMES[0], self)
        self.box.addWidget(title_source, 1, 0, constants.ALIGNMENT_LEFT_CENTER)

        title_background = QtWidgets.QLabel(constants.NOISE_CALC_RESULT_NAMES[1], self)
        self.box.addWidget(title_background, 2, 0, constants.ALIGNMENT_LEFT_CENTER)

        i = 0
        j = 1
        for title_object in range(len(constants.NOISE_CALC_BANDLINE_NAMES)):
            title_object = QtWidgets.QLabel(constants.NOISE_CALC_BANDLINE_NAMES[i], self)
            self.box.addWidget(title_object, 0, j, constants.ALIGNMENT_CENTER_CENTER)
            i += 1
            j += 1

        i = 0
        j = 1
        for entry_object_source in self.entry_objects_source:
            entry_object_source.setFixedSize(constants.SIZE_NOISE_CALC_ENTRY_OBJECTS)
            entry_object_source.setMaxLength(5)
            entry_object_source.check_entry_value()
            self.box.addWidget(entry_object_source, 1, j, constants.ALIGNMENT_CENTER_CENTER)
            i += 1
            j += 1

        i = 0
        j = 1
        for entry_object_background in self.entry_objects_background:
            entry_object_background.setFixedSize(constants.SIZE_NOISE_CALC_ENTRY_OBJECTS)
            entry_object_background.setMaxLength(5)
            entry_object_background.check_entry_value()
            self.box.addWidget(entry_object_background, 2, j, constants.ALIGNMENT_CENTER_CENTER)
            i += 1
            j += 1


class CalculatorObjectManipulator(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize(900, 700)

        self.tab_selector = QtWidgets.QTabWidget(self)
        self.tab_selector.addTab(AtmosphericAirDust(), "Air")
        self.tab_selector.addTab(WorkAreaAirDust(), "Zone")
        self.tab_selector.addTab(VentilationEfficiency(), "Vent")
        self.tab_selector.addTab(NoiseLevelsWithBackground(), "Noise")
        self.tab_selector.setCurrentIndex(0)
        self.tab_selector.setDocumentMode(True)

        self.result_area = ResultField(self)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.tab_selector)
        self.box.addWidget(self.result_area)

        self.show()

    def set_air_result_text(self, value):
        self.result_area.result_text.setText(constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[0] + value)
