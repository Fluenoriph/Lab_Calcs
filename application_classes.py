import sys
from PyQt6 import QtWidgets, QtCore, QtGui
import locale
from functools import partial


class EntryValueField(QtWidgets.QLineEdit):
    ALL_VALUES_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,]+"))
    TEMPERATURE_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,-]+"))

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
    def validate_entry_text(self, re_string):
        validator = re_string   # one var ?
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


class ResultField(QtWidgets.QFrame):     #Frame ????
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)


class MainControlField(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #self.setFixedSize()
        self.icon_size = QtCore.QSize(35, 35)

        self.icon_change_style = QtGui.QIcon("images/style.ico")
        self.icon_ok = QtGui.QIcon("images/ok.ico")
        self.icon_clear = QtGui.QIcon("images/clear.ico")
        self.icon_copy = QtGui.QIcon("images/copy.ico")
        self.icon_exit = QtGui.QIcon("images/exit.ico")

        self.button_change_style = QtWidgets.QPushButton(self)
        self.button_change_style.setIcon(self.icon_change_style)
        self.button_change_style.setIconSize(self.icon_size)

        self.button_ok = QtWidgets.QPushButton(self)
        self.button_ok.setIcon(self.icon_ok)
        self.button_ok.setIconSize(self.icon_size)
        self.button_ok.setAutoDefault(True)

        self.button_clear = QtWidgets.QPushButton(self)
        self.button_clear.setIcon(self.icon_clear)
        self.button_clear.setIconSize(self.icon_size)
        #self.button_clear.setEnabled(False)
        self.button_clear.setAutoDefault(True)

        self.button_copy = QtWidgets.QPushButton(self)
        self.button_copy.setIcon(self.icon_copy)
        self.button_copy.setIconSize(self.icon_size)

        self.button_exit = QtWidgets.QPushButton(self)
        self.button_exit.setIcon(self.icon_exit)
        self.button_exit.setIconSize(self.icon_size)
        self.button_exit.clicked.connect(sys.exit)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(20)
        self.box.addWidget(self.button_change_style)
        self.box.addWidget(self.button_ok)
        self.box.addWidget(self.button_clear)
        self.box.addWidget(self.button_copy)
        self.box.addWidget(self.button_exit)

#class ChangeStyle:


class BandLineLevels(QtWidgets.QWidget):
    BOX_SPACE = 7
    SIZE = QtCore.QSize(55, 40)

    def __init__(self, parent, header, herz_frame=None, other_level_frame=None, phone_level_frame=None,
                 delta_result_frame=None, main_result_frame=None, result_label=None):
        super().__init__(parent)
        self.header = header
        self.bandline_items = [herz_frame, other_level_frame, phone_level_frame, delta_result_frame, main_result_frame]
        self.result_label = result_label

        self.bandline_items[0] = QtWidgets.QLabel(self.header, self)
        self.bandline_items[1] = EntryDB(self)
        self.bandline_items[2] = EntryDB(self)
        self.bandline_items[3] = ResultFrame(self)
        self.bandline_items[4] = ResultFrame(self)

        for size in self.bandline_items[3:5]:
            size.setFixedSize(BandLineLevels.SIZE)

        for check in self.bandline_items[1:3]:
            check.check_all_value()

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(BandLineLevels.BOX_SPACE)
        for add in self.bandline_items:
            self.box.addWidget(add, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot()
    def calculate_result(self):
        locale.setlocale(locale.LC_ALL, "ru")

        delta = self.bandline_items[1].get_enter_value() - self.bandline_items[2].get_enter_value()

        if delta < 3:
            self.result_label = str(self.bandline_items[1].get_enter_value())
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

    def correcting_with_phone(self, correct):
        locale.setlocale(locale.LC_ALL, "ru")

        value = self.bandline_items[1].get_enter_value() - correct
        value = round(value, 1)

        rus_value = locale.format_string("%.1f", value)
        return rus_value

    @QtCore.pyqtSlot()
    def clear_values(self):
        self.bandline_items[1].enter.clear()
        self.bandline_items[2].enter.clear()
        self.bandline_items[3].result_label.clear()
        self.bandline_items[4].result_label.clear()


'''
class ClearAndLockCalc:

    @staticmethod
    def lock(frames_list, control_frame):
        for lock in frames_list:
            lock.setEnabled(False)
        control_frame.button_ok.setEnabled(False)
        control_frame.button_clear.setEnabled(True)

    @staticmethod
    def clear(frames_list):
        for clear in frames_list:
            clear.enter.clear()

    @staticmethod
    def activate(frames_list, control_frame):
        for activate in frames_list:
            activate.setEnabled(True)
        control_frame.button_ok.setEnabled(True)
        control_frame.button_clear.setEnabled(False)

    @staticmethod
    def clear_bandline(band_list):
        for line in band_list:
            line.clear_values()


class ErrorLabel(QtWidgets.QLabel):
    TEXT = "ВВЕДИТЕ ЗНАЧЕНИЯ !"
    COLOR = "color: #ff0033;"
    POSITION = QtCore.QRect(10, 5, 160, 25)

    def __init__(self, parent):
        super().__init__(parent)
        self.setText(ErrorLabel.TEXT)
        self.setStyleSheet(ErrorLabel.COLOR)
        self.setGeometry(ErrorLabel.POSITION)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.show()

        self.timer = QtCore.QTimer(self)
        self.timer.start(3000)
        self.timer.timeout.connect(self.clear_error_label)

    def clear_error_label(self):
        self.close()
        '''
