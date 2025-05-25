from PyQt6 import QtWidgets, QtCore
import sys


class Application(QtWidgets.QMainWindow):
    SIZE = QtCore.QSize(1000, 600)

    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QHBoxLayout(self)

        self.panel = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        self.panel.setHandleWidth(5)

        self.panel.addWidget(QtWidgets.QLabel("Item"))
        self.panel.addWidget(QtWidgets.QLabel("Item 2"))
        self.box.addWidget(self.panel)


        self.show()












if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #app.setWindowIcon(QtGui.QIcon("icons/calc_logo.ico"))
    app_calcs = Application()
    sys.exit(app.exec())