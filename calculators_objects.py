from PyQt6 import QtWidgets, QtCore
from application_classes import EntryValueField, ResultField
import constants
import math
import locale


class AtmosphericAirDust(QtWidgets.QWidget):
    def __init__(self, first_title=None, second_title=None, third_title=None, fourth_title=None, fifth_title=None,
                 first_entry_area=None, second_entry_area=None, third_entry_area=None, fourth_entry_area=None,
                 fifth_entry_area=None):
        super().__init__()
        self.title_names = self.set_title_names()
        self.title_objects = [first_title, second_title, third_title, fourth_title, fifth_title]
        self.entry_area_objects = [first_entry_area, second_entry_area, third_entry_area, fourth_entry_area,
                                   fifth_entry_area]

        self.create_components()
        #self.set_checking_value()

        self.show()

    def set_title_names(self):
        return constants.ATMOSPHERIC_CALC_TITLE_NAMES

    def create_components(self):
        box = QtWidgets.QGridLayout(self)
        '''box.setVerticalSpacing(30)
        box.setHorizontalSpacing(45)
        box.setContentsMargins(40, 30, 20, 20)'''

        i = 0
        for title_object in self.title_objects:
            title_object = QtWidgets.QLabel(self.title_names[i], self)
            box.addWidget(title_object, i, 0, constants.ALIGNMENT_OTHERS_COMPONENTS)
            i += 1

        j = 0
        for entry_area_object in self.entry_area_objects:
            entry_area_object = EntryValueField(self)
            entry_area_object.setFixedSize(constants.SIZE_OTHERS_ENTRY_AREAS)
            entry_area_object.setMaxLength(10)
            #entry_area_object.check_entry_value()
            box.addWidget(entry_area_object, j, 1, constants.ALIGNMENT_OTHERS_COMPONENTS)
            j += 1

    def set_checking_value(self):
        '''for check in self.entry_area_objects:
            check.check_entry_value()
        self.entry_area_objects[1].check_temperature_entry_value()'''

    '''@QtCore.pyqtSlot()
    def calculate(self):
        locale.setlocale(locale.LC_ALL, "ru")

        try:
            volume = self.entry_area_objects[0].get_entry_value() / 1000
            temperature = self.entry_area_objects[1].get_entry_value()
            pressure = self.entry_area_objects[2].get_entry_value()
            mass_before = self.entry_area_objects[3].get_entry_value() * 1000
            mass_after = self.entry_area_objects[4].get_entry_value() * 1000
        except TypeError:
            #app_classes.ClearAndLockCalc.clear(self.parameter_list)
            #app_classes.ErrorLabel(self)
        else:
            normal_volume = (volume * 273 * pressure) / ((273 + temperature) * 760)
            concentrate = (mass_after - mass_before) / normal_volume
            concentrate = round(concentrate, 2)

            if concentrate < 0.15:
                self.result_frame.result_label.setText("менее 0,15 мг/м³")
            elif concentrate > 10.0:
                self.result_frame.result_label.setText("более 10 мг/м³")
            else:
                delta = 0.110 * concentrate
                delta = round(delta, 2)
                rus_concentrate = locale.format_string("%.2f", concentrate)
                rus_delta = locale.format_string("%.2f", delta)
                result = f"{rus_concentrate} ± {rus_delta} мг/м³"

                self.result_frame.result_label.setText(result)

            #app_classes.ClearAndLockCalc.lock(self.parameter_list, self.calc_control)'''

    ''''@QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear(self.parameter_list)
        self.result_frame.result_label.clear()
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)'''


class WorkAreaAirDust(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return constants.WORK_AREA_CALC_TITLE_NAMES

    '''@QtCore.pyqtSlot()
    def calculate_result(self):
        locale.setlocale(locale.LC_ALL, "ru")

        try:
            volume = self.parameter_list[1].get_enter_value()
            temp = self.parameter_list[0].get_enter_value()
            pressure = self.parameter_list[2].get_enter_value()
            mass_before = self.parameter_list[3].get_enter_value() * 1000
            mass_after = self.parameter_list[4].get_enter_value() * 1000
        except TypeError:
            app_classes.ClearAndLockCalc.clear(self.parameter_list)
            app_classes.ErrorLabel(self)
        else:
            normal_volume = (volume * 293 * pressure) / ((273 + temp) * 760)
            concentrate = (mass_after - mass_before) * 1000 / normal_volume
            concentrate = round(concentrate, 2)

            if concentrate < 1.0:
                self.result_frame.result_label.setText("менее 1,0 мг/м³")
            elif concentrate > 250.0:
                self.result_frame.result_label.setText("более 250 мг/м³")
            else:
                delta = 0.24 * concentrate
                delta = round(delta, 2)
                rus_concentrate = locale.format_string("%.2f", concentrate)
                rus_delta = locale.format_string("%.2f", delta)
                result = f"{rus_concentrate} ± {rus_delta} мг/м³"

                self.result_frame.result_label.setText(result)

            app_classes.ClearAndLockCalc.lock(self.parameter_list, self.calc_control)'''


class CalcFlow(QtWidgets.QWidget):
    def __init__(self, parent, s_frame=None, h_frame=None, speed_frame=None, diameter_frame=None, width_frame=None,
                 height_frame=None, hole_type_frame=None, type_hole=None, type_quad=None, s_hole=None):
        super().__init__(parent)
        self.parameter_list = [s_frame, h_frame, speed_frame, diameter_frame, width_frame, height_frame]
        self.hole_type_frame = hole_type_frame
        self.type_hole = type_hole
        self.type_quad = type_quad
        self.s_hole = s_hole
        self.parameter_frame_size = QtCore.QSize(250, 90)
        self.result_frame_size = QtCore.QSize(120, 40)

        self.parameter_list[0] = app_classes.EntryValue(self, "Площадь помещения, м²")
        self.parameter_list[1] = app_classes.EntryValue(self, "Высота помещения, м")
        self.parameter_list[2] = app_classes.EntryValue(self, "Скорость движения воздуха\nв вентиляционном "
                                                              "отверстии, м/с")

        for size_i in self.parameter_list[0:3]:
            size_i.setFixedSize(self.parameter_frame_size)

        self.create_hole_type_frame()
        self.parameter_list[3] = app_classes.EntryValue(self, "Диаметр, см")
        self.parameter_list[4] = app_classes.EntryValue(self, "Ширина, см")
        self.parameter_list[5] = app_classes.EntryValue(self, "Высота, см")

        for size_j in self.parameter_list[3:6]:
            size_j.setFixedSize(150, 70)

        for check in self.parameter_list:
            check.check_all_value()

        self.perfomance_name = QtWidgets.QLabel("Производительность вентиляции", self)
        self.perfomance_frame = app_classes.ResultFrame(self)
        self.perfomance_frame.setFixedSize(self.result_frame_size)

        self.per_in_hour_name = QtWidgets.QLabel("Кратность воздухообмена", self)
        self.per_in_hour_frame = app_classes.ResultFrame(self)
        self.per_in_hour_frame.setFixedSize(self.result_frame_size)

        self.calc_control = app_classes.ControlFrame(self)
        self.calc_control.button_ok.clicked.connect(self.calculate_result)
        self.calc_control.button_clear.clicked.connect(self.clear_frames)

        self.setup_frame_position()

    def create_hole_type_frame(self):
        self.hole_type_frame = QtWidgets.QWidget(self)
        self.hole_type_frame.setFixedSize(self.parameter_frame_size)

        label = QtWidgets.QLabel("Тип вентиляционного отверстия", self.hole_type_frame)

        self.type_hole = QtWidgets.QRadioButton("Окружность", self.hole_type_frame)
        self.type_hole.clicked.connect(self.lock_quad_frames)
        self.type_quad = QtWidgets.QRadioButton("Прямоугольник", self.hole_type_frame)
        self.type_quad.clicked.connect(self.lock_diameter_frame)

        box = QtWidgets.QGridLayout(self.hole_type_frame)
        box.addWidget(label, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        box.addWidget(self.type_hole, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        box.addWidget(self.type_quad, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    def lock_quad_frames(self):
        self.type_hole.toggle()
        self.parameter_list[4].setEnabled(False)
        self.parameter_list[5].setEnabled(False)
        self.parameter_list[3].setEnabled(True)

    def lock_diameter_frame(self):
        self.type_quad.toggle()
        self.parameter_list[3].setEnabled(False)
        self.parameter_list[4].setEnabled(True)
        self.parameter_list[5].setEnabled(True)

    def setup_frame_position(self):
        calc_box = QtWidgets.QGridLayout(self)
        calc_box.setHorizontalSpacing(40)
        calc_box.setVerticalSpacing(15)
        calc_box.setContentsMargins(40, 30, 30, 30)
        calc_box.setColumnMinimumWidth(2, 20)
        calc_box.setRowMinimumHeight(5, 20)

        calc_box.addWidget(self.parameter_list[0], 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[1], 2, 0, 2, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[2], 4, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.hole_type_frame, 0, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[3], 2, 1, QtCore.Qt.AlignmentFlag.AlignTop |
                           QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[4], 3, 1, QtCore.Qt.AlignmentFlag.AlignTop |
                           QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[5], 4, 1, QtCore.Qt.AlignmentFlag.AlignTop |
                           QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.perfomance_name, 6, 0)
        calc_box.addWidget(self.perfomance_frame, 6, 1)
        calc_box.addWidget(self.per_in_hour_name, 7, 0)
        calc_box.addWidget(self.per_in_hour_frame, 7, 1)
        calc_box.addWidget(self.calc_control, 2, 3, 3, 1)

    @QtCore.pyqtSlot()
    def calculate_result(self):
        locale.setlocale(locale.LC_ALL, "ru")

        s = self.parameter_list[0].get_enter_value()
        h = self.parameter_list[1].get_enter_value()
        speed = self.parameter_list[2].get_enter_value()
        try:
            if self.type_hole.isChecked():
                diameter = self.parameter_list[3].get_enter_value() / 100
                self.s_hole = (math.pi * pow(diameter, 2)) / 4
            if self.type_quad.isChecked():
                width = self.parameter_list[4].get_enter_value() / 100
                height = self.parameter_list[5].get_enter_value() / 100
                self.s_hole = width * height

            volume_room = s * h
            perfomance = speed * self.s_hole * 3600
        except TypeError:
            app_classes.ClearAndLockCalc.clear(self.parameter_list)
            app_classes.ErrorLabel(self)
        else:
            per_in_hour = perfomance / volume_room
            perfomance = round(perfomance, 1)
            per_in_hour = round(per_in_hour, 1)
            rus_perfomance = locale.format_string("%.1f", perfomance)
            rus_per_in_hour = locale.format_string("%.1f", per_in_hour)
            perfomance_result = f"{rus_perfomance} м³/ч"
            per_in_hour_result = f"{rus_per_in_hour} раз/ч"

            self.perfomance_frame.result_label.setText(perfomance_result)
            self.per_in_hour_frame.result_label.setText(per_in_hour_result)

            app_classes.ClearAndLockCalc.lock(self.parameter_list, self.calc_control)

    @QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear(self.parameter_list)
        self.perfomance_frame.result_label.clear()
        self.per_in_hour_frame.result_label.clear()
        self.lock_quad_frames()
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)


class CalcNoise(QtWidgets.QWidget):
    def __init__(self, parent, band_31=None, band_63=None, band_125=None, band_250=None, band_500=None, band_1k=None,
                 band_2k=None, band_4k=None, band_8k=None, band_l_as=None, unit_name_frame=None, other_name_frame=None,
                 phone_name_frame=None, delta_name_frame=None, main_result_name_frame=None):
        super().__init__(parent)
        self.band_list = [band_31, band_63, band_125, band_250, band_500, band_1k, band_2k, band_4k, band_8k, band_l_as]
        self.side_frame_list = [unit_name_frame, other_name_frame, phone_name_frame, delta_name_frame,
                                main_result_name_frame]

        self.side_frame_list[0] = QtWidgets.QLabel("дБ  \\  Гц", self)
        self.side_frame_list[1] = QtWidgets.QLabel("Общий уровень", self)
        self.side_frame_list[2] = QtWidgets.QLabel("Фоновый уровень", self)
        self.side_frame_list[3] = QtWidgets.QLabel("Разность с фоном", self)
        self.side_frame_list[4] = QtWidgets.QLabel("С поправкой на фон", self)

        for size in self.side_frame_list:
            size.setFixedHeight(40)

        self.side_frame_list[0].setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        for align in self.side_frame_list[1:]:
            align.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.band_list[0] = app_classes.BandLineLevels(self, "31.5")
        self.band_list[1] = app_classes.BandLineLevels(self, "63")
        self.band_list[2] = app_classes.BandLineLevels(self, "125")
        self.band_list[3] = app_classes.BandLineLevels(self, "250")
        self.band_list[4] = app_classes.BandLineLevels(self, "500")
        self.band_list[5] = app_classes.BandLineLevels(self, "1K")
        self.band_list[6] = app_classes.BandLineLevels(self, "2K")
        self.band_list[7] = app_classes.BandLineLevels(self, "4K")
        self.band_list[8] = app_classes.BandLineLevels(self, "8K")
        self.band_list[9] = app_classes.BandLineLevels(self, "L(AS)")

        self.calc_control = app_classes.ControlFrame(self)
        self.calc_control.button_ok.clicked.connect(self.calculate_band_lines)
        self.calc_control.button_clear.clicked.connect(self.clear_frames)

        self.setup_frame_position()

    def setup_frame_position(self):
        title_left = QtWidgets.QWidget(self)
        title_box = QtWidgets.QVBoxLayout(title_left)
        title_box.setSpacing(7)
        for label in self.side_frame_list:
            title_box.addWidget(label)

        calc_box = QtWidgets.QGridLayout(self)
        calc_box.setContentsMargins(30, 40, 30, 30)
        calc_box.setColumnMinimumWidth(11, 30)
        calc_box.setSpacing(0)

        calc_box.addWidget(title_left, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[0], 0, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[1], 0, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[2], 0, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[3], 0, 4, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[4], 0, 5, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[5], 0, 6, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[6], 0, 7, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[7], 0, 8, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[8], 0, 9, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.band_list[9], 0, 10, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.calc_control, 0, 12, QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot()
    def calculate_band_lines(self):
        try:
            for band in self.band_list:
                band.calculate_result()
        except TypeError:
            app_classes.ClearAndLockCalc.clear_bandline(self.band_list)
            app_classes.ErrorLabel(self)
        else:
            app_classes.ClearAndLockCalc.lock(self.band_list, self.calc_control)

    @QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear_bandline(self.band_list)
        app_classes.ClearAndLockCalc.activate(self.band_list, self.calc_control)


class ObjectsManupulator(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(AtmosphericAirDust(), "Air")
        self.addTab(WorkAreaAirDust(), "Zone")
        self.setCurrentIndex(0)
        self.setDocumentMode(True)

        self.show()

















