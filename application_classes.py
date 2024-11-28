from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
from constants import (CONTENTS_MARGINS_ALL_OBJECTS, ALIGNMENT_LEFT_CENTER, TYPE_STANDART_NAMES, ALIGNMENT_TOP_LEFT)


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


class AbstractEntryArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        #self.box.setVerticalSpacing(5)
        #self.box.setHorizontalSpacing(40)
        self.box.setContentsMargins(CONTENTS_MARGINS_ALL_OBJECTS)

    def create_title_objects(self, title_list):
        i = 0
        for title_object in range(len(title_list)):
            title_object = QtWidgets.QLabel(title_list[i], self)
            self.box.addWidget(title_object, i, 0, ALIGNMENT_LEFT_CENTER)
            i += 1

    def create_entry_objects(self, entry_objects_list, row_count, column_count):
        for entry_object in entry_objects_list:
            self.box.addWidget(entry_object, row_count, column_count, ALIGNMENT_LEFT_CENTER)
            entry_object.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
            row_count += 1

    def create_result_field(self, row_count):
        result_field = QtWidgets.QLabel(self)
        result_field.setFixedSize(500, 90)
        result_field.setFrameShape(QtWidgets.QFrame.Shape.Box)
        result_field.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
                                     QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.box.addWidget(result_field, row_count, 0, 1, 2, ALIGNMENT_TOP_LEFT)
        return result_field

    def set_size_entry_objects(self, entry_objects_list, size):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setFixedSize(size)
            i += 1

    def set_max_length(self, entry_objects_list, max_len):
        i = 0
        for entry_object in entry_objects_list:
            entry_object.setMaxLength(max_len)
            i += 1

    def set_checking_value(self, entry_objects_list):
        for check in entry_objects_list:
            check.check_entry_value()

    def set_range_value(self, entry_objects_list):
        for entry_object in entry_objects_list:
            entry_object.setRange(0, 9999)

    def create_ok_standart_title(self):
        return QtWidgets.QLabel(TYPE_STANDART_NAMES[0], self)

    def create_no_standart_title(self):
        return QtWidgets.QLabel(TYPE_STANDART_NAMES[1], self)
