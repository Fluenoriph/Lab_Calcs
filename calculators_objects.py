from operator import index

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

    def check_value(self):
        self.textEdited.connect(partial(self.validate_text,re.compile(r"^\d+([.]|,)?\d*$")))

    def check_temper_value(self):
        self.textEdited.connect(partial(self.validate_text,re.compile(r"^(-?|\d)\d*([.]|,)?\d*$")))
        self.editingFinished.connect(self.clear_none_value)

    def get_entry_value(self):
        return float(self.value)

    @QtCore.pyqtSlot()
    def validate_text(self, validator):
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
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.sum = range(len(self.parameters))
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])
        self.entry_objects = []

    def create_input_area(self):
        [self.box.addWidget(QtWidgets.QLabel(self.parameters[_], self), _, 0, ct.data_library["Позиция левый-центр"])
         for _ in self.sum]

        [self.entry_objects.append(InputValue(self)) for _ in self.sum]
        [self.box.addWidget(self.entry_objects[_], _, 1, ct.data_library["Позиция левый-центр"]) for _ in self.sum]

    def create_result_field(self):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(ct.data_library["Размеры поля результатов"])
        result_field.setIndent(20)
        result_field.setObjectName("result_field")
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
    def check_fields(fields):
        for _ in fields:
            if _.text() == "":
                return False
        return True

    @staticmethod
    def clear_fields(fields):
        for _ in fields:
            _.clear()
            _.value = None


class AtmosphericAirDust(AbstractInputZone):
    def __init__(self, parameters = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"][0:5],
                 results = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"][5:11]):
        super().__init__(parameters = parameters)
        self.results = results
        self.set_widget_parameters()
        
        self.create_input_area()
        self.result_area = self.create_result_field()

        [_.setFixedSize(ct.data_library["Размеры поля ввода"]) for _ in self.entry_objects]
        [_.setMaxLength(10) for _ in self.entry_objects]
        [_.check_value() for _ in self.entry_objects if self.entry_objects.index(_) != 1]
        self.entry_objects[1].check_temper_value()

    def check_pressure_unit(self):
        if self.entry_objects[2].get_entry_value() < 640:
            return self.entry_objects[2].get_entry_value() * 7.5
        else:
            return self.entry_objects[2].get_entry_value()

    def calculate_concentrate(self):
        return ((((self.entry_objects[4].get_entry_value() * 1000) -
                        (self.entry_objects[3].get_entry_value() * 1000)) * 1000)
                / (((self.entry_objects[0].get_entry_value() * self.results[3] * self.check_pressure_unit())
                         / ((273 + self.entry_objects[1].get_entry_value()) * 760))))

    def calculate(self):
        if self.calculate_concentrate() < self.results[4]:
            result_string = self.results[1]
        elif self.calculate_concentrate() > self.results[5]:
            result_string = self.results[2]
        else:
            result_string = (f"{self.results[0]} {locale.format_string("%0.2f", Decimal(self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} ± "
                             f"{locale.format_string("%0.2f", Decimal(self.results[6] * self.calculate_concentrate()).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} мг/м³")

        self.result_area.setText(result_string)


class VentilationEfficiency(AbstractInputZone):
    def __init__(self):
        super().__init__(parameters = ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][0:6])
        self.set_widget_parameters()

        self.create_input_area()
        self.result_area = self.create_result_field()

        [_.setFixedSize(ct.data_library["Размеры поля ввода"]) for _ in self.entry_objects[0:3]]
        [_.setFixedSize(ct.data_library["Размеры поля ввода вент. отвер."]) for _ in self.entry_objects[3:6]]
        [_.setMaxLength(7) for _ in self.entry_objects]
        [_.check_value() for _ in self.entry_objects]

        self.entry_objects[3].textEdited.connect(self.lock_rectangle_entry_objects)
        self.entry_objects[4].textEdited.connect(self.lock_circle_entry_object)
        self.entry_objects[5].textEdited.connect(self.lock_circle_entry_object)

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
        super().__init__(parameters=ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10])
        self.setFixedSize(ct.data_library["Размеры калькулятора шум"])

        [self.box.addWidget(
            QtWidgets.QLabel(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][10:15][_], self),
            _, 0, ct.data_library["Позиция левый-центр"]) for _ in range(5)]

        [self.box.addWidget(QtWidgets.QLabel(self.parameters[_], self), 0, self.box.columnCount(),
                            ct.data_library["Позиция нижний-центр"]) for _ in self.sum]

        self.entry_objects_source = []
        self.entry_objects_background = []

        for i in (self.entry_objects_source, self.entry_objects_background):
            [i.append(InputValue(self)) for _ in self.sum]

        self.delta_result_area = []
        self.correct_result_area = []

        for i in (self.delta_result_area, self.correct_result_area):
            [i.append(QtWidgets.QLabel(self)) for _ in self.sum]

        [self.entry_objects.append(_) for _ in (self.entry_objects_source, self.entry_objects_background,
                                                self.delta_result_area, self.correct_result_area)]

        f = lambda x: x + 1
        for i, j in enumerate(self.entry_objects):
            [_.setFixedSize(ct.data_library["Размеры полей шум"]) for _ in j]
            [self.box.addWidget(j[_], f(i), f(_), ct.data_library["Позиция центр"]) for _ in self.sum]

            if i == 0 or i == 1:
                [_.setMaxLength(5) for _ in j]
                [_.check_value() for _ in j]
            else:
                [_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) for _ in j]
                [_.setObjectName("result_field_noise") for _ in j]

    # test !!!
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
        super().__init__(parameters=ct.data_library["Журналы"]["Основной регистратор"][0:8])
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)

        #self.create_title_objects(ct.data_library["Журналы"]["Основной регистратор"][0:8])
        #self.entry_objects = self.create_entry_objects(self.MAIN_REG_TYPE)

        #self.set_size_fields(self.entry_objects[0:4], ct.data_library["Размеры поля ввода инфо. протокола"])
        #self.set_size_fields(self.entry_objects[4:8], ct.data_library["Размеры поля ввода инфо. объекта"])

        #[_.setDate(ct.data_library["Текущий период"]) for _ in self.entry_objects[1:3]]
        #self.entry_objects[3].addItems(ct.data_library["Журналы"]["Основной регистратор"][8:14])
        #self.entry_objects[7].setCompleter(QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"][14:18], self))


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
        super().__init__(parameters)
        self.parameters = parameters
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)


        '''self.entry_objects_ok_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects_no_standart = self.create_entry_objects(self.FACTORS_TYPE)
        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        #self.set_size_fields(self.entry_objects, ct.data_library["Размеры поля ввода факторов"])
        #self.set_range_value(self.entry_objects)'''

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
