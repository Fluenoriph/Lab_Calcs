from PyQt6 import QtWidgets, QtGui
#from application_object import ApplicationWindow
from calculators_objects import AtmosphericAirDust, WorkAreaAirDust, VentilationEfficiency, CalculatorObjectManipulator
import sys


app = QtWidgets.QApplication(sys.argv)
#app.setWindowIcon(QtGui.QIcon("images/calc_type.ico"))
#app_window = ApplicationWindow()
#air_test = AtmosphericAirDust()
#zone_test = WorkAreaAirDust()
tab_test = CalculatorObjectManipulator()
sys.exit(app.exec())


# Рамки у фрейма сделать css стилями глобально !!!
