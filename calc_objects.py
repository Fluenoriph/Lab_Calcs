from PyQt6 import QtWidgets, QtCore
import app_classes
import math
import locale


class CalcAir(QtWidgets.QWidget):

    def __init__(self, parent, temp_frame=None, volume_frame=None, press_frame=None, mass_before_frame=None,
                 mass_after_frame=None):
        super().__init__(parent)
        self.parameter_list = [temp_frame, volume_frame, press_frame, mass_before_frame, mass_after_frame]
        self.headers_list = self.setup_header_names()
        
        self.parameter_list[1] = app_classes.EntryValue(self, self.headers_list[0])
        self.parameter_list[0] = app_classes.EntryValue(self, self.headers_list[1])
        self.parameter_list[0].check_temp_value()
        self.parameter_list[2] = app_classes.EntryValue(self, self.headers_list[2])
        self.parameter_list[3] = app_classes.EntryValue(self, self.headers_list[3])
        self.parameter_list[4] = app_classes.EntryValue(self, self.headers_list[4])

        for size in self.parameter_list:
            size.setFixedSize(240, 90)

        for check in self.parameter_list[1:]:
            check.check_all_value()

        self.result_name = QtWidgets.QLabel("Концентрация взвешенных веществ (пыли)", self)
        self.result_frame = app_classes.ResultFrame(self)
        self.result_frame.setFixedSize(120, 40)

        self.calc_control = app_classes.ControlFrame(self)
        self.calc_control.button_ok.clicked.connect(self.calculate_result)
        self.calc_control.button_clear.clicked.connect(self.clear_frames)

        self.setup_frames_position()

    def setup_header_names(self):
        names_list = ("Объем взятого на анализ\nатмосферного воздуха, л",
                      "Температура воздуха,\nпрошедшего через ротаметр, ℃",
                      "Атмосферное давление\nв месте отбора, мм.рт.ст.",
                      "Среднее значение массы\nфильтра до отбора пробы, г",
                      "Среднее значение массы\nфильтра после отбора пробы, г")
        return names_list

    def setup_frames_position(self):
        calc_box = QtWidgets.QGridLayout(self)
        calc_box.setVerticalSpacing(30)
        calc_box.setHorizontalSpacing(45)
        calc_box.setContentsMargins(40, 30, 20, 20)
        calc_box.setRowMinimumHeight(4, 30)

        calc_box.addWidget(self.parameter_list[1], 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[0], 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[2], 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[3], 2, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.parameter_list[4], 2, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        calc_box.addWidget(self.calc_control, 1, 2, 2, 1)
        calc_box.addWidget(self.result_name, 5, 0)
        calc_box.addWidget(self.result_frame, 5, 1)

    @QtCore.pyqtSlot()
    def calculate_result(self):
        locale.setlocale(locale.LC_ALL, "ru")

        try:
            volume = self.parameter_list[1].get_enter_value() / 1000
            temp = self.parameter_list[0].get_enter_value()
            pressure = self.parameter_list[2].get_enter_value()
            mass_before = self.parameter_list[3].get_enter_value() * 1000
            mass_after = self.parameter_list[4].get_enter_value() * 1000
        except TypeError:
            app_classes.ClearAndLockCalc.clear(self.parameter_list)
            app_classes.ErrorLabel(self)
        else:
            normal_volume = (volume * 273 * pressure) / ((273 + temp) * 760)
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

            app_classes.ClearAndLockCalc.lock(self.parameter_list, self.calc_control)

    @QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear(self.parameter_list)
        self.result_frame.result_label.clear()
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)


class CalcZone(CalcAir):
    def __init__(self, parent):
        super().__init__(parent)

    def setup_header_names(self):
        names_list = ("Объем воздуха,\nотобранный для анализа, л",
                      "Температура воздуха\nв месте отбора пробы, ℃",
                      "Барометрическое давление\nв месте отбора пробы, мм.рт.ст.",
                      "Масса фильтра\nдо отбора пробы, г",
                      "Масса фильтра (с пылью)\nпосле отбора пробы, г")
        return names_list

    @QtCore.pyqtSlot()
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

            app_classes.ClearAndLockCalc.lock(self.parameter_list, self.calc_control)


class CalcFlow(QtWidgets.QWidget):
    def __init__(self, parent, s_frame=None, h_frame=None, speed_frame=None, diameter_frame=None, width_frame=None,
                 height_frame=None, hole_type_frame=None, type_hole=None, type_quad=None, s_hole=None):
        super().__init__(parent)
        self.parameter_list = [s_frame, h_frame, speed_frame, diameter_frame, width_frame, height_frame]
        self.hole_type_frame = hole_type_frame
        self.type_hole = type_hole
        self.type_quad = type_quad
        self.s_hole = s_hole
        self.parameter_size = QtCore.QSize(250, 90)
        self.result_size = QtCore.QSize(120, 40)

        self.parameter_list[0] = app_classes.EntryValue(self, "Площадь помещения, м²")
        self.parameter_list[1] = app_classes.EntryValue(self, "Высота помещения, м")
        self.parameter_list[2] = app_classes.EntryValue(self, "Скорость движения воздуха\nв вентиляционном "
                                                              "отверстии, м/с")

        for size_i in self.parameter_list[0:3]:
            size_i.setFixedSize(self.parameter_size)

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
        self.perfomance_frame.setFixedSize(self.result_size)

        self.per_in_hour_name = QtWidgets.QLabel("Кратность воздухообмена", self)
        self.per_in_hour_frame = app_classes.ResultFrame(self)
        self.per_in_hour_frame.setFixedSize(self.result_size)

        self.calc_control = app_classes.ControlFrame(self)
        self.calc_control.button_ok.clicked.connect(self.calculate_result)
        self.calc_control.button_clear.clicked.connect(self.clear_frames)

        self.setup_frame_position()

    def create_hole_type_frame(self):
        self.hole_type_frame = QtWidgets.QWidget(self)
        self.hole_type_frame.setFixedSize(self.parameter_size)

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

        self.control_frame = app_classes.ControlFrame(self)
        self.control_frame.button_ok.clicked.connect(self.calculate_band_lines)
        self.control_frame.button_clear.clicked.connect(self.clear_frames)

        self.setup_frame_position()

    def setup_frame_position(self):
        title_side = QtWidgets.QWidget(self)
        title_box = QtWidgets.QVBoxLayout(title_side)
        title_box.setSpacing(7)
        for add in self.side_frame_list:
            title_box.addWidget(add)

        calc_box = QtWidgets.QGridLayout(self)
        calc_box.setContentsMargins(30, 40, 30, 30)
        calc_box.setColumnMinimumWidth(11, 30)
        calc_box.setSpacing(0)

        calc_box.addWidget(title_side, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
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
        calc_box.addWidget(self.control_frame, 0, 12, QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot()
    def calculate_band_lines(self):
        try:
            for band in self.band_list:
                band.calculate_result()
        except TypeError:
            app_classes.ClearAndLockCalc.clear_bandline(self.band_list)
            app_classes.ErrorLabel(self)
        else:
            app_classes.ClearAndLockCalc.lock(self.band_list, self.control_frame)

    @QtCore.pyqtSlot()
    def clear_frames(self):
        app_classes.ClearAndLockCalc.clear_bandline(self.band_list)
        app_classes.ClearAndLockCalc.activate(self.band_list, self.control_frame)
