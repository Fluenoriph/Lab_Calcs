from PyQt6 import QtWidgets, QtGui
from main_window_objects import ApplicationWindow
import sys


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("calc_type.ico"))
app_window = ApplicationWindow()
sys.exit(app.exec())



# Класс для блокировки кнопок и очищения      ControlFrame ???

# Повтор значений ?
