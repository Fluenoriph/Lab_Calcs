from PyQt6 import QtWidgets, QtCore, QtGui
import locale
from functools import partial


class StyledFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameStyle(QtWidgets.QFrame.Shape.Box | QtWidgets.QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.show()


class FrameWithName(StyledFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name

        self.label = QtWidgets.QLabel(name, self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.label, QtCore.Qt.AlignmentFlag.AlignCenter)


class ErrorMessage(QtWidgets.QMessageBox):
    TEXT = "\nВведите верное значение !"
    STYLE = "* {background-color: #ff7538; color: #181513;} QPushButton {background-color: #9cf0e7;}"

    def __init__(self, parent):
        super().__init__(parent)
        self.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setText(ErrorMessage.TEXT)
        self.setStyleSheet(ErrorMessage.STYLE)
        self.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.exec()


class EntryDB(StyledFrame):
    ALL_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,]+"))
    TEMP_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,-]+"))

    def __init__(self, parent, value=None):
        super().__init__(parent)
        self.value = value

        self.enter = QtWidgets.QLineEdit(self)
        self.enter.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.enter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.enter.setFrame(False)
        self.enter.setMaxLength(5)
        self.enter.setTextMargins(0, 10, 0, 10)
        self.enter.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.enter, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.box.setContentsMargins(0, 0, 0, 0)

    def check_all_value(self):
        return self.enter.textEdited.connect(partial(self.check_text, EntryDB.ALL_RE_STRING))

    def check_temp_value(self):
        return self.enter.editingFinished.connect(partial(self.check_text, EntryDB.TEMP_RE_STRING))

    @QtCore.pyqtSlot()
    def check_text(self, re_string):
        validator = re_string
        self.enter.setValidator(validator)

        if self.enter.hasAcceptableInput():
            self.value = self.enter.text()
            self.value = self.value.replace(",", ".")
            try:
                self.value = float(self.value)
            except ValueError:
                ErrorMessage(self)
                self.enter.clear()

            print(self.value)
        else:
            ErrorMessage(self)
            self.enter.clear()

    def get_enter_value(self):
        return self.value


class EntryValue(EntryDB):
    def __init__(self, parent, header):
        super().__init__(parent)
        self.header = header

        label = QtWidgets.QLabel(self.header, self)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.enter.setMaxLength(10)
        self.enter.setTextMargins(5, 5, 5, 5)

        self.box.insertWidget(0, label, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.box.setSpacing(12)
        self.box.setContentsMargins(5, 10, 5, 5)


class ControlFrame(StyledFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.icon_ok = QtGui.QIcon("check.ico")
        self.icon_exit = QtGui.QIcon("close.ico")
        self.icon_clear = QtGui.QIcon("basket.ico")
        self.size = QtCore.QSize(35, 35)

        self.button_ok = QtWidgets.QPushButton(self)
        self.button_ok.setIcon(self.icon_ok)
        self.button_ok.setIconSize(self.size)
        self.button_ok.setAutoDefault(True)

        self.button_clear = QtWidgets.QPushButton(self)
        self.button_clear.setIcon(self.icon_clear)
        self.button_clear.setIconSize(self.size)
        self.button_clear.setEnabled(False)
        self.button_clear.setAutoDefault(True)

        self.button_exit = QtWidgets.QPushButton(self)
        self.button_exit.setIcon(self.icon_exit)
        self.button_exit.setIconSize(self.size)
        self.button_exit.clicked.connect(quit)

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.button_ok, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        box.addWidget(self.button_clear, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        box.addWidget(self.button_exit, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)


class ResultFrame(StyledFrame):
    def __init__(self, parent):
        super().__init__(parent)
        result_line = QtWidgets.QWidget(self)

        self.result_label = QtWidgets.QLabel(result_line)
        self.result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)

        self.label_box = QtWidgets.QHBoxLayout(result_line)
        self.label_box.addWidget(self.result_label, QtCore.Qt.AlignmentFlag.AlignCenter)

        line_box = QtWidgets.QHBoxLayout(self)
        line_box.addWidget(result_line, QtCore.Qt.AlignmentFlag.AlignCenter)
        line_box.setContentsMargins(0, 0, 0, 0)
        result_line.show()


class BandLineLevels(QtWidgets.QWidget):
    def __init__(self, parent, header, result_label=None, main_result_frame=None, delta_result_frame=None,
                 phone_level_frame=None, other_level_frame=None, herz_frame=None):
        super().__init__(parent)
        self.header = header
        self.bandline_items = [herz_frame, other_level_frame, phone_level_frame, delta_result_frame, main_result_frame]
        self.result_label = result_label

        self.bandline_items[0] = FrameWithName(self, self.header)
        self.bandline_items[1] = EntryDB(self)
        self.bandline_items[2] = EntryDB(self)
        self.bandline_items[3] = ResultFrame(self)
        self.bandline_items[4] = ResultFrame(self)

        for size in self.bandline_items:
            size.setFixedSize(55, 40)

        for check in self.bandline_items[1:3]:
            check.check_all_value()

        box = QtWidgets.QVBoxLayout(self)
        box.setSpacing(5)
        box.setContentsMargins(0, 0, 0, 0)
        for add in self.bandline_items:
            box.addWidget(add, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.show()

    def correcting_with_phone(self, correct):
        locale.setlocale(locale.LC_ALL, "ru")
        value = self.bandline_items[1].get_enter_value() - correct
        value = round(value, 1)
        rus_value = locale.format_string("%.1f", value)
        return rus_value

    @QtCore.pyqtSlot()
    def calculate_result(self):
        locale.setlocale(locale.LC_ALL, "ru")

        delta = self.bandline_items[1].get_enter_value() - self.bandline_items[2].get_enter_value()

        if delta < 3:
            self.result_label = self.bandline_items[1].get_enter_value()
        elif 3.0 <= delta <= 3.4:
            self.result_label = self.correcting_with_phone(2.8)
        elif 3.5 <= delta <= 3.9:
            self.result_label = self.correcting_with_phone(2.4)
        elif 4.0 <= delta <= 4.4:
            self.result_label = self.correcting_with_phone(2.0)
        elif 4.5 <= delta <= 4.9:
            self.result_label = self.correcting_with_phone(1.8)
        elif 5.0 <= delta <= 5.9:
            self.result_label = self.correcting_with_phone(1.4)
        elif 6.0 <= delta <= 6.9:
            self.result_label = self.correcting_with_phone(1.1)
        elif 7.0 <= delta <= 7.9:
            self.result_label = self.correcting_with_phone(0.9)
        elif 8.0 <= delta <= 8.9:
            self.result_label = self.correcting_with_phone(0.7)
        elif 9.0 <= delta <= 9.9:
            self.result_label = self.correcting_with_phone(0.5)
        elif delta >= 10:
            self.result_label = "—"

        rus_delta = locale.format_string("%.1f", delta)

        self.bandline_items[3].result_label.setText(rus_delta)
        self.bandline_items[3].result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.bandline_items[4].result_label.setText(self.result_label)
        self.bandline_items[4].result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot()
    def clear_values(self):
        self.bandline_items[1].enter.clear()
        self.bandline_items[2].enter.clear()
        self.bandline_items[3].result_label.clear()
        self.bandline_items[4].result_label.clear()
