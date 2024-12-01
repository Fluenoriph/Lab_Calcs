from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants
import math
import locale
from functools import partial
from decimal import Decimal, ROUND_HALF_UP

locale.setlocale(locale.LC_ALL, "ru")


class EntryValueField(QtWidgets.QLineEdit):
    ALL_VALUES_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,]+"))
    TEMPERATURE_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,\\-]+"))

    def __init__(self, parent, value=None):
        super().__init__(parent)
        self.value = value
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFrame(True)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def check_entry_value(self):
        return self.textEdited.connect(partial(self.validate_entry_text,
                                               EntryValueField.ALL_VALUES_CHECK_RE_STRING))

    def check_temperature_entry_value(self):
        return self.editingFinished.connect(partial(self.validate_entry_text,
                                                    EntryValueField.TEMPERATURE_CHECK_RE_STRING))

    @QtCore.pyqtSlot()
    def validate_entry_text(self, validator):
        self.setValidator(validator)

        if self.hasAcceptableInput():
            self.value = self.text()
            self.value = self.value.replace(",", ".")
            try:
                self.value = float(self.value)
            except ValueError:
                self.clear()
        else:
            self.clear()

    def get_entry_value(self):
        return self.value


class AbstractEntryArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        #self.box.setVerticalSpacing(5)
        #self.box.setHorizontalSpacing(40)
        self.box.setContentsMargins(constants.CONTENTS_MARGINS_ALL_OBJECTS)

    def create_title_objects(self, title_list):
        i = 0
        for title_object in range(len(title_list)):
            title_object = QtWidgets.QLabel(title_list[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def create_entry_objects(self, entry_type, entry_objects_list, row_count, column_count):
        entry_objects = []

        for _ in entry_objects_list:
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_count, column_count, constants.ALIGNMENT_LEFT_CENTER)
            row_count += 1

        return tuple(entry_objects)

    def create_result_field(self):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(constants.SIZE_RESULT_FIELD)
        result_field.setFrameShape(QtWidgets.QFrame.Shape.Box)
        result_field.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        row_count = self.box.rowCount()
        row_count += 1
        self.box.addWidget(result_field, row_count, 0, 1, 2, constants.ALIGNMENT_TOP_LEFT)

        return result_field

    @staticmethod
    def set_size_entry_objects(entry_objects_list, size):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setFixedSize(size)
            i += 1

    @staticmethod
    def set_max_length(entry_objects_list, max_len):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setMaxLength(max_len)
            i += 1

    @staticmethod
    def set_checking_value(entry_objects_list):
        for check in entry_objects_list:
            check.check_entry_value()

    @staticmethod
    def set_range_value(entry_objects_list):
        for entry_object in entry_objects_list:
            entry_object.setRange(0, 9999)


class AtmosphericAirDust(AbstractEntryArea):
    def __init__(self, volume=None, temperature=None, pressure=None, mass_before=None,
                 mass_after=None, result_string=None, ):
        super().__init__()
        # self.setFixedSize(SIZE_AIR_CALC_OBJECT)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(30)

        self.parameters = (volume, temperature, pressure, mass_before, mass_after)
        self.result_string = result_string

        self.titles = self.set_title_names()
        self.create_title_objects(self.titles)

        self.entry_objects = self.create_entry_objects(EntryValueField, self.parameters, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects, constants.SIZE_OTHERS_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=10)
        self.set_checking_value(self.entry_objects)

        self.result_area = self.create_result_field()

    @staticmethod
    def set_title_names():
        return constants.ATMOSPHERIC_CALC_DUST_TITLE_NAMES

    @staticmethod
    def set_checking_value(entry_objects_list):
        for entry_object in entry_objects_list:
            if entry_objects_list.index(entry_object) == 1:
                entry_object.check_temperature_entry_value()
            else:
                entry_object.check_entry_value()

    def calculate(self):
        volume = self.entry_objects[0].get_entry_value() / 1000
        temperature = self.entry_objects[1].get_entry_value()

        if self.entry_objects[2].get_entry_value() < 640:
            pressure = self.entry_objects[2].get_entry_value() * 7.5
        else:
            pressure = self.entry_objects[2].get_entry_value()

        mass_before = self.entry_objects[3].get_entry_value() * 1000
        mass_after = self.entry_objects[4].get_entry_value() * 1000

        normal_volume = (volume * 273 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) / normal_volume
        result = Decimal(concentrate).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

        if concentrate < 0.15:
            self.result_string = constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 10.0:
            self.result_string = constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.110 * concentrate
            result_delta = Decimal(delta).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

            self.result_string = (f"{constants.ATMOSPHERIC_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", result)} ± {locale.format_string("%0.2f", result_delta)} "
                           f"мг/м³")

        self.result_area.setText(self.result_string)


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    @staticmethod
    def set_title_names():
        return constants.WORK_AREA_CALC_DUST_TITLE_NAMES

    def calculate(self):
        volume = self.entry_objects[0].get_entry_value()
        temperature = self.entry_objects[1].get_entry_value()

        if self.entry_objects[2].get_entry_value() < 640:
            pressure = self.entry_objects[2].get_entry_value() * 7.5
        else:
            pressure = self.entry_objects[2].get_entry_value()

        mass_before = self.entry_objects[3].get_entry_value() * 1000
        mass_after = self.entry_objects[4].get_entry_value() * 1000

        normal_volume = (volume * 293 * pressure) / ((273 + temperature) * 760)
        concentrate = (mass_after - mass_before) * 1000 / normal_volume
        result = Decimal(concentrate).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

        if concentrate < 1.0:
            self.result_string = constants.WORK_AREA_CALC_DUST_RESULT_NAMES[1]

        elif concentrate > 250.0:
            self.result_string = constants.WORK_AREA_CALC_DUST_RESULT_NAMES[2]

        else:
            delta = 0.24 * concentrate
            result_delta = Decimal(delta).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

            self.result_string = (f"{constants.WORK_AREA_CALC_DUST_RESULT_NAMES[0]} "
                           f"{locale.format_string("%0.2f", result)} ± {locale.format_string("%0.2f", result_delta)} "
                           f"мг/м³")

        self.result_area.setText(self.result_string)


class VentilationEfficiency(AbstractEntryArea):
    def __init__(self, room_square=None, room_height=None, flow_speed=None, diameter=None, width=None, height=None,
                 hole_square = None, result_string = None):
        super().__init__()
        # self.setFixedSize(SIZE_VENTILATION_CALC_OBJECT)
        self.box.setHorizontalSpacing(30)
        self.box.setVerticalSpacing(15)

        self.parameters = (room_square, room_height, flow_speed, diameter, width, height)
        self.hole_square = hole_square
        self.result_string = result_string

        self.create_title_objects(constants.VENTILATION_CALC_TITLE_NAMES)
        self.entry_objects = self.create_entry_objects(EntryValueField, self.parameters, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[0:3], constants.SIZE_OTHERS_ENTRY_OBJECTS)
        self.set_size_entry_objects(self.entry_objects[3:6], constants.SIZE_VENTILATION_HOLE_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=7)
        self.set_checking_value(self.entry_objects)
        self.set_hole_type()

        self.result_area = self.create_result_field()

    def set_hole_type(self):
        self.entry_objects[3].textEdited.connect(self.lock_rectangle_entry_objects)
        self.entry_objects[4].textEdited.connect(self.lock_circle_entry_object)
        self.entry_objects[5].textEdited.connect(self.lock_circle_entry_object)

    def calculate(self):
        room_square = self.entry_objects[0].get_entry_value()
        room_height = self.entry_objects[1].get_entry_value()
        flow_speed = self.entry_objects[2].get_entry_value()

        if self.entry_objects[3].get_entry_value():
            diameter = self.entry_objects[3].get_entry_value() / 100
            self.hole_square = (math.pi * pow(diameter, 2)) / 4

        else:
            width = self.entry_objects[4].get_entry_value() / 100
            height = self.entry_objects[5].get_entry_value() / 100
            self.hole_square = width * height

        room_volume = room_square * room_height
        perfomance = flow_speed * self.hole_square * 3600
        per_in_hour = perfomance / room_volume
        perfomance_result = Decimal(perfomance).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
        per_in_hour_result = Decimal(per_in_hour).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

        self.result_string = (f"{constants.VENTILATION_CALC_RESULT_NAMES[0]} {locale.format_string("%0.1f", perfomance_result)} "
                       f"м³/ч\n\n{constants.VENTILATION_CALC_RESULT_NAMES[1]} "
                       f"{locale.format_string("%0.1f", per_in_hour_result)} раз/ч")

        self.result_area.setText(self.result_string)

    @QtCore.pyqtSlot()
    def lock_rectangle_entry_objects(self):
        self.entry_objects[4].clear()
        self.entry_objects[5].clear()

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.entry_objects[3].clear()


class NoiseLevelsWithBackground(AbstractEntryArea):
    def __init__(self, octave_band_31_5=None, octave_band_63=None, octave_band_125=None, octave_band_250=None,
                 octave_band_500=None, octave_band_1k=None, octave_band_2k=None, octave_band_4k=None,
                 octave_band_8k=None, octave_band_l_as=None, delta_result = None, correct_result = None):
        super().__init__()
        # self.setFixedSize(SIZE_NOISE_CALC_OBJECT)
        self.box.setHorizontalSpacing(1)
        self.box.setContentsMargins(5, 50, 5, 0)

        self.parameters = (octave_band_31_5, octave_band_63, octave_band_125, octave_band_250, octave_band_500,
                           octave_band_1k, octave_band_2k, octave_band_4k, octave_band_8k, octave_band_l_as)

        self.delta_result = delta_result
        self.correct_result = correct_result

        self.titles = constants.NOISE_CALC_BANDLINE_NAMES + constants.NOISE_CALC_RESULT_NAMES
        self.create_title_objects(self.titles)

        self.entry_objects_source = self.create_entry_objects(EntryValueField, self.parameters, row_count=1, column_count=1)
        self.entry_objects_background = self.create_entry_objects(EntryValueField, self.parameters, row_count=2, column_count=1)

        self.entry_objects = self.entry_objects_source + self.entry_objects_background
        self.set_size_entry_objects(self.entry_objects, constants.SIZE_NOISE_CALC_ENTRY_OBJECTS)
        self.set_max_length(self.entry_objects, max_len=5)
        self.set_checking_value(self.entry_objects)

        self.result_area = self.create_result_field()
        self.set_result_field_properties(self.result_area)
        self.delta_result_area = self.result_area[0:10]
        self.correct_result_area = self.result_area[10:20]

    def create_title_objects(self, title_objects):
        i = 0
        j = 1
        for _ in title_objects[0:10]:
            title_band = QtWidgets.QLabel(title_objects[i], self)
            self.box.addWidget(title_band, 0, j, constants.ALIGNMENT_CENTER_CENTER)
            i += 1
            j += 1

        j = 1
        for _ in title_objects[10:14]:
            title_of_level = QtWidgets.QLabel(title_objects[i], self)
            self.box.addWidget(title_of_level, j, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1
            j += 1

    def create_entry_objects(self, entry_type, entry_objects_list, row_count, column_count):
        entry_objects = []

        for _ in entry_objects_list:
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_count, column_count, constants.ALIGNMENT_CENTER_CENTER)
            column_count += 1
        return tuple(entry_objects)

    def create_result_field(self):
        result_objects = []
        j = range(1, 11)

        i = 1
        for _ in j:
            object_delta = QtWidgets.QLabel(self)
            result_objects.append(object_delta)
            self.box.addWidget(object_delta, 3, i, constants.ALIGNMENT_CENTER_CENTER)
            i += 1

        i = 1
        for _ in j:
            object_correct = QtWidgets.QLabel(self)
            result_objects.append(object_correct)
            self.box.addWidget(object_correct, 4, i, constants.ALIGNMENT_CENTER_CENTER)
            i += 1

        return tuple(result_objects)

    @staticmethod
    def set_result_field_properties(result_objects):
        for result_object in result_objects:
            result_object.setFixedSize(constants.SIZE_NOISE_CALC_ENTRY_OBJECTS)
            result_object.setAlignment(constants.ALIGNMENT_CENTER_CENTER)
            result_object.setFrameShape(QtWidgets.QFrame.Shape.Box)    # ???

    def calculate(self):
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

            self.delta_result_area[i].setText(locale.format_string("%0.1f", self.delta_result))
            self.correct_result_area[i].setText(locale.format_string("%0.1f", self.correct_result))
            i += 1


class BaseRegister(AbstractEntryArea):
    def __init__(self, date_of_research=None, protocol_date=None, protocol_number=None, work_type=None,
                 object_name=None, object_address=None, administrator=None):
        super().__init__()
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)
        self.visual_date = QtCore.QDate(2025, 1, 1)

        self.parameters = (date_of_research, protocol_date, protocol_number, work_type, object_name, object_address,
                           administrator)

        self.create_title_objects(constants.BASE_REGISTER_TITLE_NAMES)

        self.entry_objects = self.create_entry_objects(QtWidgets.QLineEdit, self.parameters, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[:4], constants.SIZE_BASE_REGISTER_PROTOCOL_INFO)
        self.set_size_entry_objects(self.entry_objects[4:6], constants.SIZE_BASE_REGISTER_OBJECT_DATA)
        self.entry_objects[6].setFixedSize(120, 30)
        self.entry_objects[2].setMaxLength(10)

        self.work_type_completer = QtWidgets.QCompleter(constants.WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(self.work_type_completer)
        self.administrator_completer = QtWidgets.QCompleter(constants.EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(self.administrator_completer)

        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connection_with_database.setDatabaseName(constants.DATABASE_NAME)

    def create_entry_objects(self, entry_type, entry_objects_list, row_count, column_count):
        entry_objects = []

        for _ in entry_objects_list[0:2]:
            date_object = QtWidgets.QDateEdit(self.visual_date, self)
            entry_objects.append(date_object)
            self.box.addWidget(date_object, row_count, column_count, constants.ALIGNMENT_LEFT_CENTER)
            row_count += 1

        for _ in entry_objects_list[2:7]:
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_count, column_count, constants.ALIGNMENT_LEFT_CENTER)
            row_count += 1

        return tuple(entry_objects)

    def ready_insert_to_protocol_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':number', self.entry_objects[2].text())
        query.bindValue(':protocol_date', self.entry_objects[1].text())
        query.bindValue(':work_type', self.entry_objects[3].text())
        query.bindValue(':employee', self.entry_objects[6].text())
        return query

    def ready_insert_to_dates_of_research_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':current_date', self.entry_objects[0].text())
        return query

    def ready_insert_to_objects_names_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':name', self.entry_objects[4].text())
        return query

    def ready_insert_to_objects_addresses_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':address', self.entry_objects[5].text())
        return query


class PhysicalFactorsOptions(AbstractEntryArea):
    def __init__(self, microclimate=None, light=None, noise=None, vibration=None, emf=None, aeroionics=None,
                 ventilation=None):
        super().__init__()
        #self.setFixedSize(300, 400)
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)

        self.parameters = (microclimate, light, noise, vibration, emf, aeroionics, ventilation)

        self.create_title_objects(constants.PHYSICAL_FACTORS_TITLE_NAMES)
        self.entry_objects_ok_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=1)
        self.entry_objects_no_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=2)

        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, constants.SIZE_OPTIONS_AREA_ENTRY_OBJECTS)
        self.set_range_value(self.entry_objects)

    def ready_insert_to_microclimate_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[0].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[0].text())
        return query

    def ready_insert_to_light_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[1].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[1].text())
        return query

    def ready_insert_to_noise_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[2].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[2].text())
        return query

    def ready_insert_to_vibration_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[3].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[3].text())
        return query

    def ready_insert_to_emf_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[4])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[4].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[4].text())
        return query

    def ready_insert_to_aeroionics_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[5])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[5].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[5].text())
        return query

    def ready_insert_to_ventilation_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.PHYSICAL_REGISTER_COMMANDS_INSERT[6])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[6].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[6].text())
        return query


class RadiationControlOptions(AbstractEntryArea):
    def __init__(self, gamma_radiation=None, radon_volume_activity=None,
                 radon_equivalent_equilibrium_volumetric_activity=None, radon_flux_density=None):
        super().__init__()
        self.box.setHorizontalSpacing(20)
        self.box.setVerticalSpacing(5)

        self.parameters = (gamma_radiation, radon_volume_activity, radon_equivalent_equilibrium_volumetric_activity,
                           radon_flux_density)

        self.create_title_objects(constants.RADIATION_CONTROL_TITLE_NAMES)

        self.entry_objects_ok_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=1)
        self.entry_objects_no_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=2)

        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, constants.SIZE_OPTIONS_AREA_ENTRY_OBJECTS)
        self.set_range_value(self.entry_objects)

    def ready_insert_to_gamma_radiation_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.RADIATION_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[0].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[0].text())
        return query

    def ready_insert_to_radon_volume_activity_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.RADIATION_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[1].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[1].text())
        return query

    def ready_insert_to_eeva_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.RADIATION_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[2].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[2].text())
        return query

    def ready_insert_to_radon_flux_density_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.RADIATION_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':ok_standart', self.entry_objects_ok_standart[3].text())
        query.bindValue(':no_standart', self.entry_objects_no_standart[3].text())
        return query
