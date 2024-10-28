from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
import constants   # Нужные !!!!


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


class AbstractEntryArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        #self.box.setVerticalSpacing(5)
        #self.box.setHorizontalSpacing(40)
        #self.box.setContentsMargins(constants.CONTENTS_MARGINS_CALC_OBJECTS)

    def create_title_objects(self, title_list):
        i = 0
        for title_object in range(len(title_list)):
            title_object = QtWidgets.QLabel(title_list[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def create_entry_objects(self, entry_objects_list):
        i = 0
        for entry_object in entry_objects_list:
            self.box.addWidget(entry_object, i, 1, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def set_size_entry_objects(self, entry_objects_list, size):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setFixedSize(size)
            i += 1

    def set_max_length(self, entry_objects_list, value):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setMaxLength(value)
            i += 1


class ResultField(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(500, 90)
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
