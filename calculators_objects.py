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
    NOISE_TYPE = "Horisontal"
    MAIN_REG_TYPE = "Any entry types"
    FACTORS_TYPE = "SpinBox Type"

    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

    def create_title_objects(self, title_list, positioning_flag="Basic"):
        row_start = column_i = column_start = 0
        row_i = 1
        position = ct.data_library["Позиция левый-центр"]

        if positioning_flag == "Horisontal":
            row_i = 0
            column_i = column_start = 1
            position = ct.data_library["Позиция нижний-центр"]

        for n in range(len(title_list)):
            self.box.addWidget(QtWidgets.QLabel(title_list[n], self), row_start, column_start, position)
            row_start += row_i
            column_start += column_i

    def create_entry_objects(self, positioning_flag="Basic"):
        entry_objects = []

        row_i = column_start = 1
        row_start = 0
        range_value = self.box.rowCount()
        entry_type = InputValueField
        position = ct.data_library["Позиция левый-центр"]

        match positioning_flag:
            case "Any entry types":
                entry_type = QtWidgets.QLineEdit
                number = entry_type
                first_date = last_date = QtWidgets.QDateEdit

                s = (number, first_date, last_date)
                for i, j in enumerate(s):
                    entry_objects.append(j)
                    self.box.addWidget(j(self), i, 1, position)
                row_start = 3
                range_value -= 3

            case "SpinBox Type":
                entry_type = QtWidgets.QSpinBox
                row_start = 1
                column_start = self.box.columnCount()
                range_value -= 1

        for _ in range(range_value):
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_start, column_start, position)
            row_start += row_i

        return tuple(entry_objects)

    def create_result_field(self):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(ct.data_library["Размеры поля результатов"])
        result_field.setIndent(20)
        result_field.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        row_count = self.box.rowCount()
        self.box.setRowMinimumHeight(row_count, 30)

        row_count += 2
        self.box.addWidget(result_field, row_count, 0, 1, 2, ct.data_library["Позиция левый-верхний"])

        return result_field

    def set_widget_parameters(self):
        self.setFixedSize(ct.data_library["Размеры калькулятора базовые"])
        self.box.setVerticalSpacing(20)
        self.box.setHorizontalSpacing(50)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

    @staticmethod
    def set_size_fields(fields_list, size):
        for _ in fields_list:
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
    def __init__(self, parameters = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]):
        super().__init__()
        self.parameters = parameters
        self.set_widget_parameters()

        self.create_title_objects(self.parameters[0:5])

        self.entry_objects = self.create_entry_objects()
        self.set_size_fields(self.entry_objects, ct.data_library["Размеры поля ввода"])
        self.set_max_length(self.entry_objects, max_len=10)
        self.set_checking_value(self.entry_objects)

        self.result_area = self.create_result_field()

    def check_pressure_unit(self):
        if self.entry_objects[2].get_entry_value() < 640:
            return self.entry_objects[2].get_entry_value() * 7.5
        else:
            return self.entry_objects[2].get_entry_value()

    def calculate_concentrate(self):
        normal_volume = ((self.entry_objects[0].get_entry_value() * self.parameters[8] * self.check_pressure_unit())
                         / ((273 + self.entry_objects[1].get_entry_value()) * 760))

        return (((self.entry_objects[4].get_entry_value() * 1000) -
                        (self.entry_objects[3].get_entry_value() * 1000)) * 1000) / normal_volume

    def calculate(self):
        if self.calculate_concentrate() < self.parameters[9]:
            result_string = self.parameters[6]
        elif self.calculate_concentrate() > self.parameters[10]:
            result_string = self.parameters[7]
        else:
            result_string = (f"{self.parameters[5]} {locale.format_string("%0.2f", Decimal(self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} ± "
                             f"{locale.format_string("%0.2f", Decimal(self.parameters[11] * self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} мг/м³")

        self.result_area.setText(result_string)

    @staticmethod
    def set_checking_value(entry_objects_list):
        for _ in entry_objects_list:
            if entry_objects_list.index(_) == 1:
                _.check_temperature_entry_value()
            else:
                _.check_entry_value()


class VentilationEfficiency(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.set_widget_parameters()

        self.create_title_objects(ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][0:6])

        self.entry_objects = self.create_entry_objects()
        self.set_size_fields(self.entry_objects[0:3], ct.data_library["Размеры поля ввода"])
        self.set_size_fields(self.entry_objects[3:6], ct.data_library["Размеры поля ввода вент. отвер."])
        self.set_max_length(self.entry_objects, max_len=7)
        self.set_checking_value(self.entry_objects)
        self.set_hole_type()

        self.result_area = self.create_result_field()

    def set_hole_type(self):
        self.entry_objects[3].textEdited.connect(self.lock_rectangle_entry_objects)
        self.entry_objects[4].textEdited.connect(self.lock_circle_entry_object)
        self.entry_objects[5].textEdited.connect(self.lock_circle_entry_object)

    def calculate_hole_square(self):
        if self.entry_objects[3].get_entry_value():
            return (math.pi * pow(self.entry_objects[3].get_entry_value() / 100, 2)) / 4
        else:
            return (self.entry_objects[4].get_entry_value() / 100) * (self.entry_objects[5].get_entry_value() / 100)

    def calculate(self):
        perfomance = self.entry_objects[2].get_entry_value() * self.calculate_hole_square() * 3600
        per_in_hour = perfomance / (self.entry_objects[0].get_entry_value() * self.entry_objects[1].get_entry_value())

        self.result_area.setText(f"{ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][6]} "
                              f"{locale.format_string("%0.1f", Decimal(perfomance).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} "
                       f"м³/ч\n\n{ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][7]} "
                       f"{locale.format_string("%0.1f", Decimal(per_in_hour).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} раз/ч")

    @QtCore.pyqtSlot()
    def lock_rectangle_entry_objects(self):
        for _ in self.entry_objects[4:6]:
            _.clear()
            _.value = None

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.entry_objects[3].clear()
        self.entry_objects[3].value = None


class NoiseLevelsWithBackground(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.setFixedSize(ct.data_library["Размеры калькулятора шум"])

        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10], self.NOISE_TYPE)
        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][10:15])

        self.row_start = 1
        self.entry_objects_source = self.create_fields(InputValueField)
        self.row_start += 1
        self.entry_objects_background = self.create_fields(InputValueField)
        self.entry_objects = self.entry_objects_source + self.entry_objects_background
        self.set_size_fields(self.entry_objects, ct.data_library["Размеры полей шум"])
        self.set_checking_value(self.entry_objects)
        self.set_max_length(self.entry_objects, max_len=5)

        self.row_start += 1
        self.delta_result_area = self.create_fields(QtWidgets.QLabel)
        self.row_start += 1
        self.correct_result_area = self.create_fields(QtWidgets.QLabel)
        self.result_area = self.delta_result_area + self.correct_result_area
        self.set_size_fields(self.result_area, ct.data_library["Размеры полей шум"])

        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

    def create_fields(self, field_type):
        result_objects = []

        for i in range(1, 11):
            field = field_type(self)
            result_objects.append(field)
            self.box.addWidget(field, self.row_start, i, ct.data_library["Позиция центр"])

        return tuple(result_objects)

    def calculate(self):
        for i in range(10):
            delta = (self.entry_objects_source[i].get_entry_value() -
                                 self.entry_objects_background[i].get_entry_value())

            self.delta_result_area[i].setText(locale.format_string("%0.1f", delta))
            self.correct_result_area[i].setText(locale.format_string("%0.1f", self.correcting_result(delta,
                                                                    self.entry_objects_source[i].get_entry_value())))

    @staticmethod
    def correcting_result(delta_level, source_level):
        if delta_level < 3.0:
            return source_level
        elif 3.0 <= delta_level <= 3.4:
            return source_level - 2.8
        elif 3.5 <= delta_level <= 3.9:
            return source_level - 2.4
        elif 4.0 <= delta_level <= 4.4:
            return source_level - 2.0
        elif 4.5 <= delta_level <= 4.9:
            return source_level - 1.8
        elif 5.0 <= delta_level <= 5.9:
            return source_level - 1.4
        elif 6.0 <= delta_level <= 6.9:
            return source_level - 1.1
        elif 7.0 <= delta_level <= 7.9:
            return source_level - 0.9
        elif 8.0 <= delta_level <= 8.9:
            return source_level - 0.7
        elif 9.0 <= delta_level <= 9.9:
            return source_level - 0.5
        else:
            return source_level * 0


class BaseRegister(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.visual_date = QtCore.QDate(2025, 1, 1)

        self.create_title_objects(ct.data_library["Журналы"]["Основной регистратор"][0:11])
        self.create_entry_objects(self.MAIN_REG_TYPE)

        '''self.set_size_entry_objects(self.entry_objects_dates, ct.data_library["Размеры поля ввода инфо. протокола"])
        self.set_size_entry_objects(self.entry_objects_others[0:2], ct.data_library["Размеры поля ввода инфо. протокола"])
        self.set_size_entry_objects(self.entry_objects_others[2:4], ct.data_library["Размеры поля ввода инфо. объекта"])

        self.entry_objects_others[4].setFixedSize(120, 30)
        self.entry_objects_others[0].setMaxLength(10)
        self.work_type_completer = QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"]["Тип"], self)
        self.entry_objects_others[1].setCompleter(self.work_type_completer)
        self.administrator_completer = QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"]["Сотрудники"], self)
        self.entry_objects_others[4].setCompleter(self.administrator_completer)
        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        #self.connection_with_database.setDatabaseName()'''

        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)

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


class FactorsRegister(AbstractInputZone):
    def __init__(self, parameters = ct.data_library["Журналы"]["Физические факторы"]):
        super().__init__()
        self.parameters = parameters
        self.create_title_objects(self.parameters)
        self.entry_objects_ok_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects_no_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_fields(self.entry_objects, ct.data_library["Размеры поля ввода факторов"])
        self.set_range_value(self.entry_objects)

        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)

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
        return query

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
        return query'''
