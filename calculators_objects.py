from turtle import speed

from PyQt6 import QtWidgets, QtCore
from application_classes import EntryValueField, ResultField
import constants
import math
import locale


class AtmosphericAirDust(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.entry_objects = self.set_area_objects()
        #self.result_area =

        self.create_components()
        #self.set_checking_value()

        self.show()

    def set_title_names(self):
        return constants.ATMOSPHERIC_CALC_DUST_TITLE_NAMES

    def set_area_objects(self, volume=None, temperature=None, pressure=None, mass_before=None, mass_after=None):
        return [volume, temperature, pressure, mass_before, mass_after]

    #def set_result_area(self):

    def create_components(self):
        box = QtWidgets.QGridLayout(self)
        '''box.setVerticalSpacing(30)
        box.setHorizontalSpacing(45)
        box.setContentsMargins(40, 30, 20, 20)'''
        title_names = self.set_title_names()
        title_objects = self.set_area_objects()

        i = 0
        for title_object in title_objects:
            title_object = QtWidgets.QLabel(title_names[i], self)

            box.addWidget(title_object, 0, i, constants.ALIGNMENT_OTHERS_COMPONENTS)
            i += 1

        j = 0
        for entry_object in self.entry_objects:
            entry_object = EntryValueField(self)

            entry_object.setFixedSize(constants.SIZE_OTHERS_ENTRY_OBJECTS)
            entry_object.setMaxLength(10)
            #entry_area_object.check_entry_value()
            box.addWidget(entry_object, 1, j, constants.ALIGNMENT_OTHERS_COMPONENTS)
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
                self.result_frame.result_label.setText()
            elif concentrate > 10.0:
                self.result_frame.result_label.setText()
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
        return constants.WORK_AREA_CALC_DUST_TITLE_NAMES

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


class VentilationEfficiency(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return constants.VENTILATION_CALC_TITLE_NAMES

    def set_area_objects(self, square=None, height=None, diameter_circle=None, width_quad=None, height_quad=None):
        return [square, height, speed, diameter_circle, width_quad, height_quad]

    '''def lock_quad_frames(self):
        self.type_hole.toggle()
        self.parameter_list[4].setEnabled(False)
        self.parameter_list[5].setEnabled(False)
        self.parameter_list[3].setEnabled(True)

    def lock_diameter_frame(self):
        self.type_quad.toggle()
        self.parameter_list[3].setEnabled(False)
        self.parameter_list[4].setEnabled(True)
        self.parameter_list[5].setEnabled(True)'''

    '''@QtCore.pyqtSlot()
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
        app_classes.ClearAndLockCalc.activate(self.parameter_list, self.calc_control)'''


class NoiseLevelsWithBackground(AtmosphericAirDust):
    def __init__(self):
        super().__init__()

    def set_title_names(self):
        return constants.NOISE_CALC_BANDLINE_NAMES

    def set_area_objects(self, band_31=None, band_63=None, band_125=None, band_250=None, band_500=None, band_1k=None,
                         band_2k=None, band_4k=None, band_8k=None, band_l_as=None):
        return [band_31, band_63, band_125, band_250, band_500, band_1k, band_2k, band_4k, band_8k, band_l_as]


class CalculatorObjectManipulator(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(AtmosphericAirDust(), "Air")
        self.addTab(WorkAreaAirDust(), "Zone")
        self.addTab(VentilationEfficiency(), "Vent")
        self.addTab(NoiseLevelsWithBackground(), "Noise")
        self.setCurrentIndex(0)
        self.setDocumentMode(True)

        self.show()
