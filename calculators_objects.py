from PyQt6 import QtWidgets, QtCore

from constants import (SIZE_AIR_CALC_OBJECT, SIZE_OTHERS_ENTRY_OBJECTS, SIZE_VENTILATION_CALC_OBJECT,
                       SIZE_VENTILATION_HOLE_ENTRY_OBJECTS, SIZE_NOISE_CALC_OBJECT, SIZE_NOISE_CALC_ENTRY_OBJECTS,
                       ATMOSPHERIC_CALC_DUST_TITLE_NAMES, ATMOSPHERIC_CALC_DUST_RESULT_NAMES,
                       WORK_AREA_CALC_DUST_TITLE_NAMES, WORK_AREA_CALC_DUST_RESULT_NAMES, VENTILATION_CALC_TITLE_NAMES,
                       VENTILATION_CALC_RESULT_NAMES, NOISE_CALC_RESULT_NAMES, NOISE_CALC_BANDLINE_NAMES,
                       ALIGNMENT_CENTER_CENTER)

from application_classes import EntryValueField, AbstractEntryArea
import math
import locale


class AtmosphericAirDust(AbstractEntryArea):
    def __init__(self, result=None):
        super().__init__()
        self.setFixedSize(SIZE_AIR_CALC_OBJECT)

        self.title_names = self.set_title_names()

        self.volume = EntryValueField(self)
        self.temperature = EntryValueField(self)
        self.pressure = EntryValueField(self)
        self.mass_before = EntryValueField(self)
        self.mass_after = EntryValueField(self)

        self.entry_objects = (self.volume, self.temperature, self.pressure, self.mass_before, self.mass_after)

        self.result = result

        self.create_title_objects(self.title_names)
        self.create_entry_objects(self.entry_objects, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects, SIZE_OTHERS_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=10)
        self.set_checking_value(self.entry_objects)

    def set_title_names(self):
        return ATMOSPHERIC_CALC_DUST_TITLE_NAMES

    def set_checking_value(self, entry_objects_list):
        entry_objects_list[0].check_entry_value()
        entry_objects_list[1].check_temperature_entry_value()
        entry_objects_list[2].check_entry_value()
        entry_objects_list[3].check_entry_value()
        entry_objects_list[4].check_entry_value()

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value() / 1000
        temperature = self.temperature.get_entry_value()

        if self.pressure.get_entry_value() < 640:
            pressure = self.pressure.get_entry_value() * 7.5
        else:
            pressure = self.pressure.get_entry_value()

        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 273 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) / normal_volume
        #concentrate = round(concentrate, 2)

        if concentrate < 0.15:
            self.result = ATMOSPHERIC_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 10.0:
            self.result = ATMOSPHERIC_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.110 * concentrate
            #delta = round(delta, 2)

            self.result = (f"{ATMOSPHERIC_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", concentrate)} ± {locale.format_string("%0.2f", delta)} "
                           f"мг/м³")

    def get_result_text(self):
        return self.result


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return WORK_AREA_CALC_DUST_TITLE_NAMES

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        volume = self.volume.get_entry_value()
        temperature = self.temperature.get_entry_value()

        if self.pressure.get_entry_value() < 640:
            pressure = self.pressure.get_entry_value() * 7.5
        else:
            pressure = self.pressure.get_entry_value()

        mass_before = self.mass_before.get_entry_value() * 1000
        mass_after = self.mass_after.get_entry_value() * 1000

        normal_volume = (volume * 293 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) * 1000 / normal_volume
        #concentrate = round(concentrate, 2)

        if concentrate < 1.0:
            self.result = WORK_AREA_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 250.0:
            self.result = WORK_AREA_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.24 * concentrate
            #delta = round(delta, 2)

            self.result = (f"{WORK_AREA_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", concentrate)} ± {locale.format_string("%0.2f", delta)} "
                           f"мг/м³")


class VentilationEfficiency(AbstractEntryArea):
    def __init__(self, hole_square = None, result = None):
        super().__init__()
        self.setFixedSize(SIZE_VENTILATION_CALC_OBJECT)
        self.box.setHorizontalSpacing(20)

        self.room_square = EntryValueField(self)
        self.room_height = EntryValueField(self)
        self.flow_speed = EntryValueField(self)
        self.diameter = EntryValueField(self)
        self.width = EntryValueField(self)
        self.height = EntryValueField(self)

        self.entry_objects = (self.room_square, self.room_height, self.flow_speed, self.diameter, self.width,
                              self.height)

        self.hole_square = hole_square
        self.result = result

        self.create_title_objects(VENTILATION_CALC_TITLE_NAMES)
        self.create_entry_objects(self.entry_objects, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[0:3], SIZE_OTHERS_ENTRY_OBJECTS)
        self.set_size_entry_objects(self.entry_objects[3:6], SIZE_VENTILATION_HOLE_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=7)
        self.set_checking_value(self.entry_objects)
        self.set_hole_type()

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

        self.result = (f"{VENTILATION_CALC_RESULT_NAMES[0]} {locale.format_string("%0.1f", perfomance)} "
                       f"м³/ч\n\n {VENTILATION_CALC_RESULT_NAMES[1]} "
                       f"{locale.format_string("%0.1f", per_in_hour)} раз/ч")

    def get_result_text(self):
        return self.result


class NoiseLevelsWithBackground(AbstractEntryArea):
    def __init__(self, delta_result = None, correct_result = None):
        super().__init__()
        self.setFixedSize(SIZE_NOISE_CALC_OBJECT)
        self.box.setHorizontalSpacing(5)

        self.title_source = QtWidgets.QLabel(NOISE_CALC_RESULT_NAMES[0], self)
        self.title_background = QtWidgets.QLabel(NOISE_CALC_RESULT_NAMES[1], self)

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

        self.entry_objects_source_with_title = (self.title_source, self.band_31_source, self.band_63_source,
                                                self.band_125_source, self.band_250_source, self.band_500_source,
                                                self.band_1k_source, self.band_2k_source, self.band_4k_source,
                                                self.band_8k_source, self.band_l_as_source)

        self.entry_objects_background_with_title = (self.title_background, self.band_31_background,
                                                    self.band_63_background, self.band_125_background,
                                                    self.band_250_background, self.band_500_background,
                                                    self.band_1k_background, self.band_2k_background,
                                                    self.band_4k_background, self.band_8k_background,
                                                    self.band_l_as_background)

        self.entry_objects_source = self.entry_objects_source_with_title[1:]
        self.entry_objects_background = self.entry_objects_background_with_title[1:]
        self.entry_objects = self.entry_objects_source + self.entry_objects_background

        self.delta_result = delta_result
        self.correct_result = correct_result
        self.delta_result_massive = []
        self.correct_result_massive = []

        self.create_title_objects(NOISE_CALC_BANDLINE_NAMES)
        self.create_entry_objects(self.entry_objects_source_with_title, row_count=1, column_count=0)
        self.create_entry_objects(self.entry_objects_background_with_title, row_count=2, column_count=0)
        self.set_size_entry_objects(self.entry_objects, SIZE_NOISE_CALC_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=5)
        self.set_checking_value(self.entry_objects)

    def create_title_objects(self, title_objects):
        i = 0
        j = 1
        for title_object in range(len(title_objects)):
            title_object = QtWidgets.QLabel(title_objects[i], self)
            self.box.addWidget(title_object, 0, j)
            i += 1
            j += 1

    def create_entry_objects(self, entry_objects_list, row_count, column_count):
        for entry_object in entry_objects_list:
            self.box.addWidget(entry_object, row_count, column_count, ALIGNMENT_CENTER_CENTER)
            column_count += 1

    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        i = 1
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
        return (f"{NOISE_CALC_RESULT_NAMES[2]} {"|".join(self.delta_result_massive)}\n\n"
                f"{NOISE_CALC_RESULT_NAMES[3]} {"|".join(self.correct_result_massive)}")
