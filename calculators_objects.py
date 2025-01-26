from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants as ct
import math
import locale
from functools import partial
from decimal import Decimal, ROUND_HALF_UP
locale.setlocale(locale.LC_ALL, "ru")


class InputValueField(QtWidgets.QLineEdit):
    ALL_VALUES_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,]+"))
    TEMPERATURE_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,\\-]+"))

    def __init__(self, parent, value=None):
        super().__init__(parent)
        self.value = value
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def check_entry_value(self):
        return self.textEdited.connect(partial(self.validate_entry_text,
                                               InputValueField.ALL_VALUES_CHECK_RE_STRING))

    def check_temperature_entry_value(self):
        return self.editingFinished.connect(partial(self.validate_entry_text,
                                                    InputValueField.TEMPERATURE_CHECK_RE_STRING))

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


class AbstractInputZone(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Калькуляторы"]["Отступы"])

    def create_title_objects(self, title_list, column_count):
        i = j = 1
        row_count = 0
        position = ct.data_library["Позиция левый-центр"]
        r = len(title_list)

        if column_count == 0 and r == 4:
            row_count = 1
            j = 0
        elif column_count == 0:
            j = 0
        else:
            i = 0
            position = ct.data_library["Позиция нижний-центр"]

        for n in range(r):
            self.box.addWidget(QtWidgets.QLabel(title_list[n], self), row_count, column_count, position)
            row_count += i
            column_count += j

    def create_entry_objects(self, range_value, row_count, column_count, entry_type=InputValueField,
                             position=ct.data_library["Позиция левый-центр"]):
        entry_objects = []
        i = j = 1
        if row_count == 0 or entry_type == QtWidgets.QSpinBox:
            j = 0
        elif row_count == 2 and entry_type == QtWidgets.QLineEdit:
            j = 0
        else:
            i = 0

        for _ in range(range_value):
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_count, column_count, position)
            row_count += i
            column_count += j

        return tuple(entry_objects)

    def create_result_field(self):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(ct.data_library["Калькуляторы"]["Размеры поля результатов"])
        result_field.setIndent(20)
        result_field.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        row_count = self.box.rowCount()
        self.box.setRowMinimumHeight(row_count, 30)
        row_count += 2
        self.box.addWidget(result_field, row_count, 0, 1, 2, ct.data_library["Позиция левый-верхний"])
        return result_field

    @staticmethod
    def set_size_entry_objects(entry_objects_list, size):
        for _ in entry_objects_list:
            _.setFixedSize(size)

    @staticmethod
    def set_max_length(entry_objects_list, max_len):
        for _ in entry_objects_list:
            _.setMaxLength(max_len)

    @staticmethod
    def set_checking_value(entry_objects_list):
        for _ in entry_objects_list:
            _.check_entry_value()

    @staticmethod
    def set_range_value(entry_objects_list):
        for _ in entry_objects_list:
            _.setRange(0, 9999)


class AtmosphericAirDust(AbstractInputZone):
    def __init__(self, result_string=None, ):
        super().__init__()
        self.setFixedSize(ct.data_library["Калькуляторы"]["Размеры базовые"])
        self.box.setVerticalSpacing(20)
        self.box.setHorizontalSpacing(50)
        self.box.setContentsMargins(ct.data_library["Калькуляторы"]["Отступы"])
        self.result_string = result_string
        self.titles = self.set_title_names()
        self.create_title_objects(self.titles, 0)
        self.entry_objects = self.create_entry_objects(5, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects, ct.data_library["Калькуляторы"]["Размеры поля ввода"])
        self.set_max_length(self.entry_objects, max_len=10)
        self.set_checking_value(self.entry_objects)
        self.result_area = self.create_result_field()

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
            self.result_string = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]["Результаты"][1]
        elif concentrate > 10.0:
            self.result_string = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]["Результаты"][2]
        else:
            delta = 0.110 * concentrate
            result_delta = Decimal(delta).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

            self.result_string = (f"{ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]["Результаты"][0]} "
                           f"{locale.format_string("%0.2f", result)} ± {locale.format_string("%0.2f", result_delta)} "
                           f"мг/м³")
        self.result_area.setText(self.result_string)

    @staticmethod
    def set_title_names():
        return ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]["Параметры"]

    @staticmethod
    def set_checking_value(entry_objects_list):
        for _ in entry_objects_list:
            if entry_objects_list.index(_) == 1:
                _.check_temperature_entry_value()
            else:
                _.check_entry_value()


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

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
            self.result_string = ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]["Результаты"][1]
        elif concentrate > 250.0:
            self.result_string = ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]["Результаты"][2]
        else:
            delta = 0.24 * concentrate
            result_delta = Decimal(delta).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

            self.result_string = (f"{ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]["Результаты"][0]} "
                           f"{locale.format_string("%0.2f", result)} ± {locale.format_string("%0.2f", result_delta)} "
                           f"мг/м³")
        self.result_area.setText(self.result_string)

    @staticmethod
    def set_title_names():
        return ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"]["Параметры"]


class VentilationEfficiency(AbstractInputZone):
    def __init__(self, hole_square = None, result_string = None):
        super().__init__()
        self.setFixedSize(ct.data_library["Калькуляторы"]["Размеры базовые"])
        self.box.setVerticalSpacing(20)
        self.box.setHorizontalSpacing(50)
        self.box.setContentsMargins(ct.data_library["Калькуляторы"]["Отступы"])
        self.hole_square = hole_square
        self.result_string = result_string
        self.create_title_objects(ct.data_library["Калькуляторы"]["Эффектив. вентиляции"]["Параметры"], 0)
        self.entry_objects = self.create_entry_objects(6, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[0:3], ct.data_library["Калькуляторы"]["Размеры поля ввода"])
        self.set_size_entry_objects(self.entry_objects[3:6], ct.data_library["Калькуляторы"]["Эффектив. вентиляции"]
        ["Размеры поля ввода параметров отверстия"])
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

        self.result_string = (f"{ct.data_library["Калькуляторы"]["Эффектив. вентиляции"]["Результаты"][0]} "
                              f"{locale.format_string("%0.1f", perfomance_result)} "
                       f"м³/ч\n\n{ct.data_library["Калькуляторы"]["Эффектив. вентиляции"]["Результаты"][1]} "
                       f"{locale.format_string("%0.1f", per_in_hour_result)} раз/ч")
        self.result_area.setText(self.result_string)

    @QtCore.pyqtSlot()
    def lock_rectangle_entry_objects(self):
        self.entry_objects[4].clear()
        self.entry_objects[5].clear()

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.entry_objects[3].clear()


class NoiseLevelsWithBackground(AbstractInputZone):
    def __init__(self, delta_result = None, correct_result = None):
        super().__init__()
        self.setFixedSize(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Размеры"])
        self.box.setContentsMargins(ct.data_library["Калькуляторы"]["Отступы"])
        self.delta_result = delta_result
        self.correct_result = correct_result
        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Параметры"], 1)
        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Результаты"], 0)
        self.entry_objects_source = self.create_entry_objects(10, 1, 1,
                                                              InputValueField, ct.data_library["Позиция центр"])
        self.entry_objects_background = self.create_entry_objects(10, 2, 1,
                                                                  InputValueField, ct.data_library["Позиция центр"])
        self.entry_objects = self.entry_objects_source + self.entry_objects_background
        self.set_size_entry_objects(self.entry_objects, ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]
        ["Размеры поля ввода"])
        self.set_max_length(self.entry_objects, max_len=5)
        self.set_checking_value(self.entry_objects)
        self.result_area = self.create_result_field()
        self.set_result_field_properties(self.result_area)
        self.delta_result_area = self.result_area[0:10]
        self.correct_result_area = self.result_area[10:20]

    def create_result_field(self):
        result_objects = []
        i = j = 1
        r = range(10)

        for _ in r:
            object_delta = QtWidgets.QLabel(self)
            result_objects.append(object_delta)
            self.box.addWidget(object_delta, 3, i, ct.data_library["Позиция центр"])
            i += 1
        for _ in r:
            object_correct = QtWidgets.QLabel(self)
            result_objects.append(object_correct)
            self.box.addWidget(object_correct, 4, j, ct.data_library["Позиция центр"])
            j += 1

        return tuple(result_objects)

    def set_result_field_style(self, style):
        for _ in self.result_area:
            _.setStyleSheet(style)

    def calculate(self):
        for i in range(10):
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

    @staticmethod
    def set_result_field_properties(result_objects):
        for _ in result_objects:
            _.setFixedSize(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Размеры поля ввода"])
            _.setAlignment(ct.data_library["Позиция центр"])


class BaseRegister(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)
        self.visual_date = QtCore.QDate(2025, 1, 1)
        self.create_title_objects(ct.data_library["Журналы"]["Основной регистратор"]["Параметры"], 0)
        self.entry_objects_dates = self.create_entry_objects(2, 0, 1,
                                                             QtWidgets.QDateEdit)
        self.entry_objects_others = self.create_entry_objects(5, 2, 1,
                                                              QtWidgets.QLineEdit)
        self.set_size_entry_objects(self.entry_objects_dates, ct.data_library["Журналы"]["Основной регистратор"]
        ["Размеры поля ввода инфо. протокола"])
        self.set_size_entry_objects(self.entry_objects_others[0:2], ct.data_library["Журналы"]["Основной регистратор"]
        ["Размеры поля ввода инфо. протокола"])
        self.set_size_entry_objects(self.entry_objects_others[2:4], ct.data_library["Журналы"]["Основной регистратор"]
        ["Размеры поля ввода инфо. объекта"])
        self.entry_objects_others[4].setFixedSize(120, 30)
        self.entry_objects_others[0].setMaxLength(10)
        self.work_type_completer = QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"]["Тип"], self)
        self.entry_objects_others[1].setCompleter(self.work_type_completer)
        self.administrator_completer = QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"]["Сотрудники"], self)
        self.entry_objects_others[4].setCompleter(self.administrator_completer)
        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        #self.connection_with_database.setDatabaseName()

    '''def ready_insert_to_protocol_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':number', self.entry_objects[2].text())
        query.bindValue(':protocol_date', self.entry_objects_dates[1].text())
        query.bindValue(':work_type', self.entry_objects[3].text())
        query.bindValue(':employee', self.entry_objects[6].text())
        return query

    def ready_insert_to_dates_of_research_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':current_date', self.entry_objects_dates[0].text())
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
        return query'''


class PhysicalFactorsOptions(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)
        self.create_title_objects(ct.data_library["Журналы"]["Физические факторы"]["Параметры"], 0)
        self.entry_objects_ok_standart = self.create_entry_objects(7, 1, 1,
                                                                   QtWidgets.QSpinBox)
        self.entry_objects_no_standart = self.create_entry_objects(7, 1, 2,
                                                                   QtWidgets.QSpinBox)
        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, ct.data_library["Журналы"]["Размеры поля ввода факторов"])
        self.set_range_value(self.entry_objects)

    '''def ready_insert_to_microclimate_table(self):
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
        return query'''


class RadiationControlOptions(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.box.setHorizontalSpacing(20)
        self.box.setVerticalSpacing(5)
        self.create_title_objects(ct.data_library["Журналы"]["Радиационные факторы"]["Параметры"], 0)
        self.entry_objects_ok_standart = self.create_entry_objects(4, 1, 1,
                                                                   QtWidgets.QSpinBox)
        self.entry_objects_no_standart = self.create_entry_objects(4, 1, 2,
                                                                   QtWidgets.QSpinBox)
        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, ct.data_library["Журналы"]["Размеры поля ввода факторов"])
        self.set_range_value(self.entry_objects)

    '''def ready_insert_to_gamma_radiation_table(self):
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
        return query'''
