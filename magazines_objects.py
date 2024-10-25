from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants


'''class PhysicalFactorsTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.setFixedSize()'''







class PhysicalFactorsMagazine(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedSize()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(40)

        self.protocol_number = QtWidgets.QLineEdit(self)
        self.first_date = QtWidgets.QDateEdit(self)
        self.last_date = QtWidgets.QDateEdit(self)
        self.work_type = QtWidgets.QLineEdit(self)
        self.object_name = QtWidgets.QLineEdit(self)
        self.object_address = QtWidgets.QLineEdit(self)
        self.administrator = QtWidgets.QLineEdit(self)

        self.entry_objects = (self.protocol_number, self.first_date, self.last_date, self.work_type, self.object_name,
                              self.object_address, self.administrator)

        self.connect_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connect_db.setDatabaseName('physical_data.db')
        self.connect_db.open()
        print(self.connect_db.tables())
        self.connect_db.close()



        self.create_main_components()
        self.show()

    def create_main_components(self):
        i = 0
        for title_object in range(len(constants.MAGAZINE_MAIN_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.MAGAZINE_MAIN_TITLE_NAMES[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 0
        for entry_object in self.entry_objects:
            self.box.addWidget(entry_object, i, 1, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        work_type_completer = QtWidgets.QCompleter(constants.WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(work_type_completer)
        administrator_completer = QtWidgets.QCompleter(constants.EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(administrator_completer)

    #def create_area_of_factors(self):

































if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table = PhysicalFactorsMagazine()
    sys.exit(app.exec())
