from PyQt6 import QtWidgets, QtGui
from application_object import ApplicationType
import sys


app = QtWidgets.QApplication(sys.argv)
#app.setWindowIcon(QtGui.QIcon("images/calc_type.ico"))
#app_window = ApplicationWindow()
#air_test = AtmosphericAirDust()
#zone_test = WorkAreaAirDust()
#tab_test = CalculatorObjectManipulator()
app_type = ApplicationType()
sys.exit(app.exec())
