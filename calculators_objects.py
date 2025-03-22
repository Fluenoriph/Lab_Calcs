from PyQt6 import QtWidgets, QtCore, QtGui
import constants as ct
import math
import locale
from functools import partial
from decimal import Decimal, ROUND_HALF_UP
locale.setlocale(locale.LC_ALL, "ru")


class InputValue(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.value = None
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def check_value(self):
        self.textEdited.connect(partial(self.validate_text, QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("\\d+([.]|,)?\\d*"), self)))

    def check_temper_value(self):
        self.textEdited.connect(partial(self.validate_text, QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("-?\\d*([.]|,)?\\d*"), self)))
        self.editingFinished.connect(self.clear_none_value)

    def get_entry_value(self):
        return float(self.value)

    @QtCore.pyqtSlot()
    def validate_text(self, validator):
        self.setValidator(validator)
        if self.hasAcceptableInput():
            if self.text().find(",") != -1:
                self.value = self.text().replace(",", ".")
            else:
                self.value = self.text()
        else:
            self.clear()

    @QtCore.pyqtSlot()
    def clear_none_value(self):
        return [self.clear() for _ in ("-", ".", ",", "-.", "-,") if self.text() == _]


class AbstractBaseCalc(QtWidgets.QWidget):
    def __init__(self, parameters, results):
        super().__init__()
        self.parameters = parameters
        self.results = results
        self.entry_objects = []

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

        for _ in self.parameters:
            i = self.box.rowCount()
            self.box.addWidget(QtWidgets.QLabel(_, self), i, 0, ct.data_library["Позиция левый-центр"])
            j = InputValue(self)
            self.box.addWidget(j, i, 1, ct.data_library["Позиция левый-центр"])
            self.entry_objects.append(j)

        self.result_area = QtWidgets.QLabel(self)
        self.result_area.setFixedSize(ct.data_library["Размеры поля результатов"])
        self.result_area.setIndent(20)
        self.result_area.setObjectName("result_field")
        self.result_area.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.box.setRowMinimumHeight(self.box.rowCount(), 50)
        self.box.addWidget(self.result_area, self.box.rowCount(), 0, 1, 3, ct.data_library["Позиция левый-верхний"])

    @staticmethod
    def reset_value(x):
        x.value = None


class AtmosphericAirDust(AbstractBaseCalc):
    def __init__(self, parameters = ct.data_library["Калькуляторы"]["Пыль в атмосферном воздухе"]["Параметры"],
                 results = ct.data_library["Калькуляторы"]["Пыль в атмосферном воздухе"]["Результаты"]):

        super().__init__(parameters = parameters, results = results)
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

        return self.result_area.setText(result_string)


class VentilationEfficiency(AbstractBaseCalc):
    def __init__(self):
        super().__init__(ct.data_library["Калькуляторы"]["Эффективность вентиляции"]["Параметры"],
                         ct.data_library["Калькуляторы"]["Эффективность вентиляции"]["Результаты"])

        [_.setFixedSize(ct.data_library["Размеры поля ввода"]) for _ in self.entry_objects[:3]]
        [_.setFixedSize(ct.data_library["Размеры поля ввода вент. отвер."]) for _ in self.entry_objects[3:]]
        [_.setMaxLength(7) for _ in self.entry_objects]
        [_.check_value() for _ in self.entry_objects]

        self.entry_objects[3].textEdited.connect(self.lock_rectangle_entry_objects)
        self.entry_objects[4].textEdited.connect(self.lock_circle_entry_object)
        self.entry_objects[5].textEdited.connect(self.lock_circle_entry_object)

    def check_hole_data(self):
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

        return self.result_area.setText(f"{self.results[0]} "
                              f"{locale.format_string("%0.1f", Decimal(perfomance).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} "
                       f"м³/ч\n\n{self.results[1]} "
                       f"{locale.format_string("%0.1f", Decimal(per_in_hour).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))} раз/ч")

    @QtCore.pyqtSlot()
    def lock_rectangle_entry_objects(self):
        [_.clear() for _ in self.entry_objects[4:]]
        [self.reset_value(_) for _ in self.entry_objects[4:]]

    @QtCore.pyqtSlot()
    def lock_circle_entry_object(self):
        self.entry_objects[3].clear()
        self.entry_objects[3].value = None


class NoiseLevelsWithBackground(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.sum = range(10)
        self.octave_table = []
        self.entry_objects_source = []
        self.entry_objects_background = []
        self.delta_result_area = []
        self.correct_result_area = []

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы калькулятора"])

        [self.box.addWidget(QtWidgets.QLabel(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Октавные полосы"][_], self),
                            0, _ + 1, ct.data_library["Позиция нижний-центр"]) for _ in self.sum]

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

            self.box.addWidget(QtWidgets.QLabel(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Результаты"][i], self),
            i + 1, 0, ct.data_library["Позиция левый-центр"])

            [_.setFixedSize(ct.data_library["Размеры полей шум"]) for _ in j]
            [self.box.addWidget(j[_], i + 1, _ + 1, ct.data_library["Позиция центр"]) for _ in self.sum]
            self.octave_table.append(j)

    def calculate(self):
        for _ in self.sum:
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
            for _ in ct.data_library["Калькуляторы"]["Учет влияния фонового шума"]["Поправки"]:
                if _[0] <= delta <= _[1]:
                    return delta, source - _[2]

class Factors(QtWidgets.QWidget):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.r = range(len(self.parameters))
        self.entry_objects = []
        self.ok_standart_entries = []
        self.no_standart_entries = []

        self.box = QtWidgets.QGridLayout(self)

        for i, j in enumerate(("соотв.", "не соотв.")):
            self.box.addWidget(QtWidgets.QLabel(j, self), 0, i + 1, ct.data_library["Позиция левый-центр"])
        [self.box.addWidget(QtWidgets.QLabel(self.parameters[_], self), _ + 1, 0, ct.data_library["Позиция левый-центр"]) for _ in self.r]

        for i, j in enumerate((self.ok_standart_entries, self.no_standart_entries)):
            [j.append(QtWidgets.QSpinBox(self)) for _ in self.r]
            [_.setFixedSize(ct.data_library["Размеры поля ввода факторов"]) for _ in j]
            [_.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons) for _ in j]
            [_.setRange(0, 9999) for _ in j]
            [self.box.addWidget(j[_], _ + 1, i + 1, ct.data_library["Позиция левый-центр"]) for _ in self.r]
            self.entry_objects.append(j)

    def validate_values(self):
        if (not [i for i, j in enumerate(self.entry_objects[0]) if j.value()] or
            [i for i, j in enumerate(self.entry_objects[0]) if j.value() < self.entry_objects[1][i].value()]):
            return False
        else:
            return True
