import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial


class EntryValueField(QtWidgets.QLineEdit):
    ALL_VALUES_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,]+"))
    TEMPERATURE_CHECK_RE_STRING = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9\\.,-]+"))

    def __init__(self, parent):
        super().__init__(parent)
        self.value = None
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFrame(True)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def check_entry_value(self):
        return self.textEdited.connect(partial(self.validate_entry_text,
                                               EntryValueField.ALL_VALUES_CHECK_RE_STRING))

    def check_temperature_entry_value(self):            # signal ??
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


class ResultField(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(500, 90)
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.setWordWrap(True)













'''class ClearAndLockCalc:

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
        self.close()'''

