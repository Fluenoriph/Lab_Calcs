from PyQt6 import QtWidgets, QtCore


class Application(QtWidgets.QMainWindow):
    SIZE = QtCore.QSize(1000, 600)

    def __init__(self):
        super().__init__()
        