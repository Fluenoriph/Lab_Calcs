from dataclasses import fields
from operator import index

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants as ct
import math
import locale
import re
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
        return [self.clear() for _ in ("-", ".", ",") if self.text() == _]


class AbstractBaseCalc(QtWidgets.QWidget):

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.entry_objects = []
        self.sum = range(len(self.parameters))

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])
        self.setFixedSize(ct.data_library["Размеры калькулятора базовые"])
        self.box.setVerticalSpacing(20)
        self.box.setHorizontalSpacing(50)

        [self.box.addWidget(QtWidgets.QLabel(self.parameters[_], self), _, 0, ct.data_library["Позиция левый-центр"])
         for _ in self.sum]

        [self.entry_objects.append(InputValue(self)) for _ in self.sum]
        [self.box.addWidget(self.entry_objects[_], _, 1, ct.data_library["Позиция левый-центр"]) for _ in self.sum]

        self.result_area = QtWidgets.QLabel(self)
        self.result_area.setFixedSize(ct.data_library["Размеры поля результатов"])
        self.result_area.setIndent(20)
        self.result_area.setObjectName("result_field")
        self.result_area.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.box.setRowMinimumHeight(self.box.rowCount(), 30)
        self.box.addWidget(self.result_area, self.box.rowCount(), 0, 1, 2, ct.data_library["Позиция левый-верхний"])

    @staticmethod
    def reset_value(x):
        x.value = None


class AtmosphericAirDust(AbstractBaseCalc):
    def __init__(self, parameters = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"][0:5],
                 results = ct.data_library["Калькуляторы"]["Пыль в атмосф. воздухе"][5:12]):
        super().__init__(parameters = parameters)
        self.results = results

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


class VentilationEfficiency(AbstractBaseCalc):
    def __init__(self):
        super().__init__(ct.data_library["Калькуляторы"]["Эффектив. вентиляции"][0:6])
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
        [_.clear() for _ in self.entry_objects[4:6]]
        [self.reset_value(_) for _ in self.entry_objects[4:6]]

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.entry_objects[3].clear()
        self.entry_objects[3].value = None


class NoiseLevelsWithBackground(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(ct.data_library["Размеры калькулятора шум"])
        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])
        self.sum = range(10)

        self.octave_table = []
        self.entry_objects_source = []
        self.entry_objects_background = []
        self.delta_result_area = []
        self.correct_result_area = []

        [self.box.addWidget(
            QtWidgets.QLabel(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][10:15][_], self),
            _, 0, ct.data_library["Позиция левый-центр"]) for _ in range(5)]

        [self.box.addWidget(QtWidgets.QLabel(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10][_], self),
                            0, self.box.columnCount(), ct.data_library["Позиция нижний-центр"]) for _ in self.sum]

        for i, j in enumerate((self.entry_objects_source, self.entry_objects_background,
                               self.delta_result_area, self.correct_result_area)):
            if i == 0 or i == 1:
                [j.append(InputValue(self)) for _ in self.sum]
                [_.setMaxLength(5) for _ in j]
                [_.check_value() for _ in j]
            else:
                [j.append(QtWidgets.QLabel(self)) for _ in self.sum]
                [_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) for _ in j]
                [_.setObjectName("result_field_noise") for _ in j]

            [_.setFixedSize(ct.data_library["Размеры полей шум"]) for _ in j]
            [self.box.addWidget(j[_], ct.f_upper(i), ct.f_upper(_), ct.data_library["Позиция центр"]) for _ in self.sum]
            self.octave_table.append(j)

    # test !!!
    def calculate(self):
        for _ in range(10):
            if self.entry_objects_source[_].text() != "" and self.entry_objects_background[_].text() != "":
                result = self.correcting_with_background(self.entry_objects_source[_].get_entry_value(),
                                                         self.entry_objects_background[_].get_entry_value())

                self.delta_result_area[_].setText(locale.format_string("%0.1f", result[0]))
                self.correct_result_area[_].setText(locale.format_string("%0.1f", result[1]))
            else:
                return

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


class AbstractRegister(QtWidgets.QWidget):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.entry_objects = []
        self.sum = range(len(self.parameters))
        self.connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connect.setDatabaseName('registers_data.db')

        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)

        [self.box.addWidget(QtWidgets.QLabel(self.parameters[_], self), _, 0, ct.data_library["Позиция левый-центр"])
         for _ in self.sum]

        if not self.connect.open():
            self.error_message(self, 2)

    @staticmethod
    def error_message(parent, x):
        return QtWidgets.QMessageBox.critical(parent, " ", ct.data_library["Журналы"]["Критические сообщения"][x])


class MainRegister(AbstractRegister):
    def __init__(self, parameters = ct.data_library["Журналы"]["Основной регистратор"][0:8]):
        super().__init__(parameters)
        self.entry_objects.append(QtWidgets.QLineEdit(self))
        [self.entry_objects.append(QtWidgets.QDateEdit(self)) for _ in range(2)]

        self.entry_objects.append(QtWidgets.QComboBox(self))
        [self.entry_objects.append(QtWidgets.QLineEdit(self)) for _ in range(4)]

        [_.setFixedSize(ct.data_library["Размеры поля ввода инфо. протокола"]) for _ in self.entry_objects[0:4]]
        [_.setFixedSize(ct.data_library["Размеры поля ввода инфо. объекта"]) for _ in self.entry_objects[4:8]]

        [self.box.addWidget(self.entry_objects[_], _, 1, ct.data_library["Позиция левый-центр"]) for _ in self.sum]

        [_.setDate(ct.data_library["Текущий период"]) for _ in self.entry_objects[1:3]]
        [self.entry_objects[3].addItem(ct.data_library["Журналы"]["Основной регистратор"][8:14][_], ct.f_upper(_)) for _
         in range(6)]
        self.entry_objects[7].setCompleter(QtWidgets.QCompleter(ct.data_library["Журналы"]["Основной регистратор"][14:18], self))


class FactorsRegister(AbstractRegister):
    def __init__(self, parameters = ct.data_library["Журналы"]["Физические факторы"]):
        super().__init__(parameters = parameters)
        self.ok_standart_entries = []
        self.no_standart_entries = []

        for i in (self.ok_standart_entries, self.no_standart_entries):
            [i.append(QtWidgets.QSpinBox(self)) for _ in self.sum]
            self.entry_objects.append(i)

        [self.entry_objects.append(_) for _ in (self.ok_standart_entries, self.no_standart_entries)]
        [j.setFixedSize(ct.data_library["Размеры поля ввода факторов"]) for i in self.entry_objects for j in i]
        [j.setRange(0, 9999) for i in self.entry_objects for j in i]

        for i in range(2):
            [self.box.addWidget(self.entry_objects[i][_], _, ct.f_upper(i), ct.data_library["Позиция левый-центр"]) for _ in self.sum]

        x = self.box.rowCount()
        for i, j in enumerate(("соотв.", "не соотв.")):
            self.box.addWidget(QtWidgets.QLabel(j, self), x, ct.f_upper(i), ct.data_library["Позиция левый-верхний"])
