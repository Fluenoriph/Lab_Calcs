from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants


class PhysicalFactorsTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ok_standart_title = QtWidgets.QLabel(constants.TYPE_STANDART_NAMES[0], self)
        self.no_standart_title = QtWidgets.QLabel(constants.TYPE_STANDART_NAMES[1], self)

        self.ok_standart_microclimate = QtWidgets.QSpinBox(self)
        self.ok_standart_light = QtWidgets.QSpinBox(self)
        self.ok_standart_noise = QtWidgets.QSpinBox(self)
        self.ok_standart_vibration = QtWidgets.QSpinBox(self)
        self.ok_standart_emf = QtWidgets.QSpinBox(self)
        self.ok_standart_aeroionics = QtWidgets.QSpinBox(self)
        self.ok_standart_ventilation = QtWidgets.QSpinBox(self)

        self.no_standart_microclimate = QtWidgets.QSpinBox(self)
        self.no_standart_light = QtWidgets.QSpinBox(self)
        self.no_standart_noise = QtWidgets.QSpinBox(self)
        self.no_standart_vibration = QtWidgets.QSpinBox(self)
        self.no_standart_emf = QtWidgets.QSpinBox(self)
        self.no_standart_aeroionics = QtWidgets.QSpinBox(self)
        self.no_standart_ventilation = QtWidgets.QSpinBox(self)

        self.entry_objects_ok_standart = (self.ok_standart_microclimate, self.ok_standart_light,
                                          self.ok_standart_noise, self.ok_standart_vibration, self.ok_standart_emf,
                                          self.ok_standart_aeroionics, self.ok_standart_ventilation)

        self.entry_objects_no_standart = (self.no_standart_microclimate, self.no_standart_light,
                                          self.no_standart_noise, self.no_standart_vibration, self.no_standart_emf,
                                          self.no_standart_aeroionics, self.no_standart_ventilation)

        self.entry_objects_phys_factors = self.entry_objects_ok_standart + self.entry_objects_no_standart


class BaseMagazine(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QGridLayout(self)
        self.box.setVerticalSpacing(5)
        self.box.setHorizontalSpacing(40)

        self.visual_date = QtCore.QDate(2025, 1, 1)

        self.protocol_number = QtWidgets.QLineEdit(self)
        self.first_date = QtWidgets.QDateEdit(self.visual_date, self)
        self.last_date = QtWidgets.QDateEdit(self.visual_date, self)
        self.work_type = QtWidgets.QLineEdit(self)
        self.object_name = QtWidgets.QLineEdit(self)
        self.object_address = QtWidgets.QLineEdit(self)
        self.administrator = QtWidgets.QLineEdit(self)

        self.entry_objects = (self.protocol_number, self.first_date, self.last_date, self.work_type, self.object_name,
                              self.object_address, self.administrator)

        self.button_add_to_database = QtWidgets.QPushButton('Сохранить протокол', self)

        self.create_components()

    def create_components(self):
        i = 0
        for title_object in range(len(constants.MAGAZINE_MAIN_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.MAGAZINE_MAIN_TITLE_NAMES[i], self)
            self.box.addWidget(title_object, i, 0, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 0
        for entry_object in self.entry_objects:
            self.box.addWidget(entry_object, i, 1, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        for first_objects in self.entry_objects[:4]:
            first_objects.setFixedSize(constants.SIZE_OTHERS_ENTRY_OBJECTS)

        self.entry_objects[0].setMaxLength(10)

        for objects_data in self.entry_objects[4:6]:
            objects_data.setFixedSize(200, 25)
            #objects_data.setAlignment(constants.ALIGNMENT_LEFT_CENTER)

        self.entry_objects[6].setFixedSize(100, 25)

        self.box.addWidget(self.button_add_to_database, i, 0, constants.ALIGNMENT_LEFT_CENTER)

        work_type_completer = QtWidgets.QCompleter(constants.WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(work_type_completer)

        administrator_completer = QtWidgets.QCompleter(constants.EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(administrator_completer)


class PhysicalFactorsMagazine(BaseMagazine, PhysicalFactorsTable):
    def __init__(self):
        super().__init__()
        self.create_physical_factors_area()
        self.show()

        self.button_add_to_database.clicked.connect(self.add_record_to_database)

        self.connect_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connect_db.setDatabaseName(constants.DATABASES_NAMES)  # base name in const !!!1

    def create_physical_factors_area(self):
        self.box.addWidget(self.ok_standart_title, 0, 3, constants.ALIGNMENT_LEFT_BOTTOM)
        self.box.addWidget(self.no_standart_title, 0, 4, constants.ALIGNMENT_LEFT_BOTTOM)

        i = 1
        j = 0
        for title_object in range(len(constants.PHYSICAL_FACTORS_NAMES)):
            title_object = QtWidgets.QLabel(constants.PHYSICAL_FACTORS_NAMES[j], self)
            self.box.addWidget(title_object, i, 2, constants.ALIGNMENT_LEFT_CENTER)
            i += 1
            j += 1
    # Size entry !!!!
        i = 1
        for entry_object_ok_standart in self.entry_objects_ok_standart:
            self.box.addWidget(entry_object_ok_standart, i, 3, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 1
        for entry_object_no_standart in self.entry_objects_no_standart:
            self.box.addWidget(entry_object_no_standart, i, 4, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        for entry_object in self.entry_objects_phys_factors:
            entry_object.setFixedSize(constants.SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS)
            entry_object.setRange(0, 999)

    @QtCore.pyqtSlot()
    def add_record_to_database(self):
        number = self.protocol_number.text()

        self.connect_db.open()
        query = QtSql.QSqlQuery()
        check_prepare = query.prepare("INSERT INTO protocols (number) VALUES (:number)")
        if check_prepare:
            print('Query Ok !')
        else:
            print('Query Bad !')

        query.bindValue(':number', number)
        check_exec = query.exec()
        if check_exec:
            print('Exec ok !')
        else:
            print('Exec Bad !')

        self.connect_db.close()









if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table = PhysicalFactorsMagazine()
    sys.exit(app.exec())
