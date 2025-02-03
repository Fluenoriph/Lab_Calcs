from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants as ct
import math
import locale
import re
import itertools
from functools import partial
from decimal import Decimal, ROUND_HALF_UP
locale.setlocale(locale.LC_ALL, "ru")


class InputValue(QtWidgets.QLineEdit):
    def __init__(self, value=None):
        super().__init__()
        self.value = value
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def check_entry_value(self, value_type=True):
        if value_type:
            self.textEdited.connect(partial(self.validate_entry_text,re.compile(r"^\d+([.]|,)?\d*$")))
        else:
            self.textEdited.connect(partial(self.validate_entry_text,re.compile(r"^(-?|\d)\d*([.]|,)?\d*$")))
            self.editingFinished.connect(self.clear_none_value)

    def get_entry_value(self):
        return float(self.value)

    @QtCore.pyqtSlot()
    def validate_entry_text(self, validator):
        if validator.findall(self.text()):
            if self.text().find(",") != -1:
                self.value = self.text().replace(",", ".")
            else:
                self.value = self.text()
        else:
            self.clear()

    @QtCore.pyqtSlot()
    def clear_none_value(self):
        for _ in ("-", ".", ","):
            if self.text() == _:
                self.clear()


class AbstractInputZone(QtWidgets.QWidget):
    AIR_TYPE = 1
    NOISE_TYPE = 2
    MAIN_REG_TYPE = 3
    FACTORS_TYPE = 4

    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

    def create_title_objects(self, title_list, positioning_flag=True):
        if positioning_flag:
            row_start = column_i = column_start = 0
            row_i = 1
            position = ct.data_library["Позиция левый-центр"]
        else:
            row_i = row_start = 0
            column_i = column_start = 1
            position = ct.data_library["Позиция нижний-центр"]

        for _ in title_list:
            self.box.addWidget(QtWidgets.QLabel(_, self), row_start, column_start, position)
            row_start += row_i
            column_start += column_i

    def create_entry_objects(self, positioning_flag=AIR_TYPE):
        entry_objects = []

        match positioning_flag:
            case 1:
                row_start = 0
                column_start = 1
                range_value = self.box.rowCount()
                entry_type = InputValue
            case 3:
                for _ in range(4):
                    if _ == 0:
                        field = QtWidgets.QLineEdit(self)
                    elif _ == 3:
                        field = QtWidgets.QComboBox(self)
                        field.setEditable(False)
                    else:
                        field = QtWidgets.QDateEdit(self)
                    entry_objects.append(field)
                    self.box.addWidget(field, _, 1, ct.data_library["Позиция левый-центр"])

                row_start = 4
                column_start = 1
                range_value = self.box.rowCount() - 4
                entry_type = QtWidgets.QLineEdit
            case 4:
                row_start = 1
                column_start = self.box.columnCount()
                range_value = self.box.rowCount() - 1
                entry_type = QtWidgets.QSpinBox
            case _:
                return

        for _ in range(range_value):
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_start, column_start, ct.data_library["Позиция левый-центр"])
            row_start += 1

        return entry_objects

    def create_result_field(self):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(ct.data_library["Размеры поля результатов"])
        result_field.setIndent(20)
        result_field.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.box.setRowMinimumHeight(self.box.rowCount(), 30)
        self.box.addWidget(result_field, self.box.rowCount(), 0, 1, 2, ct.data_library["Позиция левый-верхний"])

        return result_field

    def set_widget_parameters(self):
        self.setFixedSize(ct.data_library["Размеры калькулятора базовые"])
        self.box.setVerticalSpacing(20)
        self.box.setHorizontalSpacing(50)           # Abstract ???

    @staticmethod
    def set_size_fields(fields_list, size):
        [_.setFixedSize(size) for _ in fields_list]

    @staticmethod
    def set_max_length(entry_objects, max_len):
        [_.setMaxLength(max_len) for _ in entry_objects]

    @staticmethod
    def set_checking_value(entry_objects, calc_type=True):
        if calc_type:
            [_.check_entry_value() for _ in entry_objects]
        else:
            for _ in entry_objects:
                if entry_objects.index(_) != 1:
                    _.check_entry_value()
                else:
                    _.check_entry_value(False)

    @staticmethod
    def set_range_value(entry_objects):
       [_.setRange(0, 9999) for _ in entry_objects]

    @staticmethod
    def check_fields(fields):
        for _ in fields:
            if _.text() == "":
                return False
        return True

    @staticmethod
    def clear_fields(fields):
        for _ in fields:
            if type(_) == QtWidgets.QLabel:
                _.clear()
            else:
                _.clear()
                _.value = None


class AtmosphericAirDust(AbstractInputZone):
    def __init__(self, parameters = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"]):
        super().__init__()
        self.parameters = parameters
        self.set_widget_parameters()

        self.titles = self.parameters[0:5]
        self.create_title_objects(self.titles)

        self.entry_objects = self.create_entry_objects()
        self.set_size_fields(self.entry_objects, ct.data_library["Размеры поля ввода"])
        self.set_max_length(self.entry_objects, max_len=10)
        self.set_checking_value(self.entry_objects, False)

        self.result_area = self.create_result_field()

    def check_pressure_unit(self):
        if self.entry_objects[2].get_entry_value() < 640:
            return self.entry_objects[2].get_entry_value() * 7.5
        else:
            return self.entry_objects[2].get_entry_value()

    def calculate_concentrate(self):
        return ((((self.entry_objects[4].get_entry_value() * 1000) -
                        (self.entry_objects[3].get_entry_value() * 1000)) * 1000)
                / (((self.entry_objects[0].get_entry_value() * self.parameters[8] * self.check_pressure_unit())
                         / ((273 + self.entry_objects[1].get_entry_value()) * 760))))

    def calculate(self):
        if self.calculate_concentrate() < self.parameters[9]:
            result_string = self.parameters[6]
        elif self.calculate_concentrate() > self.parameters[10]:
            result_string = self.parameters[7]
        else:
            result_string = (f"{self.parameters[5]} {locale.format_string("%0.2f", Decimal(self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} ± "
                             f"{locale.format_string("%0.2f", Decimal(self.parameters[11] * self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} мг/м³")

        self.result_area.setText(result_string)


class VentilationEfficiency(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.set_widget_parameters()

        self.titles = ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][0:6]
        self.create_title_objects(self.titles)

        self.entry_objects = self.create_entry_objects()
        self.set_size_fields(self.entry_objects[0:3], ct.data_library["Размеры поля ввода"])
        self.set_size_fields(self.entry_objects[3:6], ct.data_library["Размеры поля ввода вент. отвер."])
        self.set_max_length(self.entry_objects, max_len=7)
        self.set_checking_value(self.entry_objects)

        self.entry_objects[3].textEdited.connect(self.lock_rectangle_entry_objects)
        self.entry_objects[4].textEdited.connect(self.lock_circle_entry_object)
        self.entry_objects[5].textEdited.connect(self.lock_circle_entry_object)

        self.result_area = self.create_result_field()

    def set_hole_checks(self):
        if self.entry_objects[3].text() != "" and self.entry_objects[4].text() == "" and self.entry_objects[5].text() == "":
            return True
        elif self.entry_objects[3].text() == "" and self.entry_objects[4].text() != "" and self.entry_objects[5].text() != "":
            return True
        else:
            return False

    def calculate_hole_square(self):
        if self.entry_objects[3].text() != "":
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

        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10], False)
        self.create_title_objects(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][10:15])

        self.row_start = 1
        self.entry_objects_source = self.create_fields(InputValue)
        self.row_start += 1
        self.entry_objects_background = self.create_fields(InputValue)
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

    def create_fields(self, field_type):
        result_objects = []

        for _ in range(1, 11):
            field = field_type(self)
            if field_type == QtWidgets.QLabel:
                field.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            result_objects.append(field)
            self.box.addWidget(field, self.row_start, _, ct.data_library["Позиция центр"])

        return result_objects
    # check method !!!!
    def calculate(self):
        for _ in range(10):
            if self.entry_objects_source[_].text() != "" and self.entry_objects_background[_].text() != "":
                result = self.correcting_with_background(self.entry_objects_source[_].get_entry_value(),
                                                         self.entry_objects_background[_].get_entry_value())

                self.delta_result_area[_].setText(locale.format_string("%0.1f", result[0]))
                self.correct_result_area[_].setText(locale.format_string("%0.1f", result[1]))
            else:
                pass

    @staticmethod
    def correcting_with_background(source, back):
        delta = source - back

        if delta < 3.0:
            return delta, source
        elif delta > 10.0:
            return delta, source * 0
        else:
            for _ in ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][15:24]:
                if _[0] <= delta <= _[1]:
                    return delta, source - _[2]


class MainRegister(AbstractInputZone):
    def __init__(self):
        super().__init__()
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)

        self.create_title_objects(ct.data_library["Журналы"]["Основной регистратор"][0:8])
        self.entry_objects = self.create_entry_objects(self.MAIN_REG_TYPE)

        self.set_size_fields(self.entry_objects[0:4], ct.data_library["Размеры поля ввода инфо. протокола"])
        self.set_size_fields(self.entry_objects[4:8], ct.data_library["Размеры поля ввода инфо. объекта"])

        [_.setDate(ct.data_library["Текущий период"]) for _ in self.entry_objects[1:3]]
        self.entry_objects[3].addItems(ct.data_library["Журналы"]["Основной регистратор"][8:14])
        self.entry_objects[7].setCompleter(QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"][14:18], self))


        #self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
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


class FactorsRegister(AbstractInputZone):
    def __init__(self, parameters = ct.data_library["Журналы"]["Физические факторы"]):
        super().__init__()
        self.parameters = parameters
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)

        self.create_title_objects(self.parameters)
        self.entry_objects_ok_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects_no_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_fields(self.entry_objects, ct.data_library["Размеры поля ввода факторов"])
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
