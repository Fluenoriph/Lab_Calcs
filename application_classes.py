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
                self.value = float(self.value)  # ok button activate factor
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
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
