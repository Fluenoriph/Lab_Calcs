from PyQt6 import QtWidgets, QtCore
import constants
from application_classes import EntryValueField
import math
import locale


class AtmosphericAirDust(QtWidgets.QWidget):
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

        self.result = None

        self.create_components()
        self.set_checking_value()

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

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value() / 1000
        temperature = self.temperature.get_entry_value()
        pressure = self.pressure.get_entry_value()
        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 273 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) / normal_volume
        #concentrate = round(concentrate, 2)

        if concentrate < 0.15:
            self.result = constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 10.0:
            self.result = constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.110 * concentrate
            #delta = round(delta, 2)

            self.result = (f"{constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", concentrate)} ± {locale.format_string("%0.2f", delta)} "
                           f"мг/м³")

    def get_result_text(self):
        return self.result


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return constants.WORK_AREA_CALC_DUST_TITLE_NAMES

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value()
        temperature = self.temperature.get_entry_value()
        pressure = self.pressure.get_entry_value()
        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 293 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) * 1000 / normal_volume
        #concentrate = round(concentrate, 2)

        if concentrate < 1.0:
            self.result = constants.WORK_AREA_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 250.0:
            self.result = constants.WORK_AREA_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.24 * concentrate
            #delta = round(delta, 2)

            self.result = (f"{constants.WORK_AREA_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", concentrate)} ± {locale.format_string("%0.2f", delta)} "
                           f"мг/м³")


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

        self.hole_square = None
        self.result = None

        self.create_components()
        self.set_checking_value()
        self.set_hole_type()

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

    @QtCore.pyqtSlot()
    def lock_rectangle_entry_objects(self):
        self.width.clear()
        self.height.clear()

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.diameter.clear()

    def set_hole_type(self):
        self.diameter.textEdited.connect(self.lock_rectangle_entry_objects)
        self.width.textEdited.connect(self.lock_circle_entry_object)
        self.height.textEdited.connect(self.lock_circle_entry_object)

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        room_square = self.room_square.get_entry_value()
        room_height = self.room_height.get_entry_value()
        flow_speed = self.flow_speed.get_entry_value()

        if self.diameter.get_entry_value():
            diameter = self.diameter.get_entry_value() / 100
            self.hole_square = (math.pi * pow(diameter, 2)) / 4

        else:
            width = self.width.get_entry_value() / 100
            height = self.height.get_entry_value() / 100
            self.hole_square = width * height

        room_volume = room_square * room_height
        perfomance = flow_speed * self.hole_square * 3600
        per_in_hour = perfomance / room_volume
        #perfomance = round(perfomance, 1)
        #per_in_hour = round(per_in_hour, 1)

        self.result = (f"{constants.VENTILATION_CALC_RESULT_NAMES[0]} {locale.format_string("%0.1f", perfomance)} "
                       f"м³/ч\n\n {constants.VENTILATION_CALC_RESULT_NAMES[1]} "
                       f"{locale.format_string("%0.1f", per_in_hour)} раз/ч")

    def get_result_text(self):
        return self.result


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

        self.entry_objects = self.entry_objects_source + self.entry_objects_background

        self.delta_result = None
        self.correct_result = None
        self.delta_result_massive = []
        self.correct_result_massive = []

        self.create_and_check_components()

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

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        i = 0
        while i < 10:
            self.delta_result = (self.entry_objects_source[i].get_entry_value() -
                                 self.entry_objects_background[i].get_entry_value())

            if self.delta_result < 3.0:
                self.correct_result = self.entry_objects_source[i].get_entry_value()
            elif 3.0 <= self.delta_result <= 3.4:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 2.8
            elif 3.5 <= self.delta_result <= 3.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 2.4
            elif 4.0 <= self.delta_result <= 4.4:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 2.0
            elif 4.5 <= self.delta_result <= 4.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 1.8
            elif 5.0 <= self.delta_result <= 5.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 1.4
            elif 6.0 <= self.delta_result <= 6.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 1.1
            elif 7.0 <= self.delta_result <= 7.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 0.9
            elif 8.0 <= self.delta_result <= 8.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 0.7
            elif 9.0 <= self.delta_result <= 9.9:
                self.correct_result = self.entry_objects_source[i].get_entry_value() - 0.5
            elif self.delta_result >= 10.0:
                self.correct_result = self.entry_objects_source[i].get_entry_value() * 0

            self.delta_result_massive.append(locale.format_string("%0.1f", self.delta_result))
            self.correct_result_massive.append(locale.format_string("%0.1f", self.correct_result))
            i += 1

    def get_result_text(self):
        return (f"{constants.NOISE_CALC_RESULT_NAMES[2]} {"|".join(self.delta_result_massive)}\n\n"
                f"{constants.NOISE_CALC_RESULT_NAMES[3]} {"|".join(self.correct_result_massive)}")
