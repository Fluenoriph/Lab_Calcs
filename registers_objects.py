from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants


class BaseRegister(QtWidgets.QWidget):
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

        self.ok_standart_title = QtWidgets.QLabel(constants.TYPE_STANDART_NAMES[0], self)
        self.no_standart_title = QtWidgets.QLabel(constants.TYPE_STANDART_NAMES[1], self)

        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')

        self.button_add_to_database = QtWidgets.QPushButton('Сохранить протокол', self)

        self.create_base_area()

    def create_base_area(self):
        i = 0
        for title_object in range(len(constants.BASE_REGISTER_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.BASE_REGISTER_TITLE_NAMES[i], self)
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


class PhysicalFactorsOptions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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

        self.entry_objects_phys_factors = (self.ok_standart_microclimate, self.ok_standart_light,
                                           self.ok_standart_noise, self.ok_standart_vibration, self.ok_standart_emf,
                                           self.ok_standart_aeroionics, self.ok_standart_ventilation,
                                           self.no_standart_microclimate, self.no_standart_light,
                                           self.no_standart_noise, self.no_standart_vibration, self.no_standart_emf,
                                           self.no_standart_aeroionics, self.no_standart_ventilation)

        for entry_object in self.entry_objects_phys_factors:
            entry_object.setFixedSize(constants.SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS)
            entry_object.setRange(0, 999)


class PhysicalFactorsRegister(BaseRegister, PhysicalFactorsOptions):
    def __init__(self):
        super().__init__()
        self.create_physical_factors_area()
        self.show()
        self.button_add_to_database.clicked.connect(self.add_record_to_database)     # Put in high level !!!

        self.connection_with_database.setDatabaseName(constants.DATABASES_NAMES)

    def create_physical_factors_area(self):
        self.box.addWidget(self.ok_standart_title, 0, 3, constants.ALIGNMENT_LEFT_BOTTOM)
        self.box.addWidget(self.no_standart_title, 0, 4, constants.ALIGNMENT_LEFT_BOTTOM)

        i = 1
        j = 0
        for title_object in range(len(constants.PHYSICAL_FACTORS_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.PHYSICAL_FACTORS_TITLE_NAMES[j], self)
            self.box.addWidget(title_object, i, 2, constants.ALIGNMENT_LEFT_CENTER)
            i += 1
            j += 1

        i = 1
        for entry_object_ok_standart in self.entry_objects_phys_factors[0:7]:
            self.box.addWidget(entry_object_ok_standart, i, 3, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 1
        for entry_object_no_standart in self.entry_objects_phys_factors[7:14]:
            self.box.addWidget(entry_object_no_standart, i, 4, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def ready_queries_to_database(self):
        self.query_to_protocols = QtSql.QSqlQuery()
        self.query_to_protocols.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[0])
        self.query_to_protocols.bindValue(':number', self.protocol_number.text())
        self.query_to_protocols.bindValue(':type', self.work_type.text())
        self.query_to_protocols.bindValue(':employee', self.administrator.text())

        self.query_to_first_date = QtSql.QSqlQuery()
        self.query_to_first_date.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[1])
        self.query_to_first_date.bindValue(':date', self.first_date.text())

        self.query_to_last_date = QtSql.QSqlQuery()
        self.query_to_last_date.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[2])
        self.query_to_last_date.bindValue(':date', self.last_date.text())

        self.query_to_object_name = QtSql.QSqlQuery()
        self.query_to_object_name.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[3])
        self.query_to_object_name.bindValue(':name', self.object_name.text())

        self.query_to_object_address = QtSql.QSqlQuery()
        self.query_to_object_address.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[4])
        self.query_to_object_address.bindValue(':address', self.object_address.text())

        self.query_to_microclimate = QtSql.QSqlQuery()
        self.query_to_microclimate.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[5])
        self.query_to_microclimate.bindValue(':ok_norm', self.ok_standart_microclimate.text())
        self.query_to_microclimate.bindValue(':not_norm', self.no_standart_microclimate.text())

        self.query_to_light = QtSql.QSqlQuery()
        self.query_to_light.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[6])
        self.query_to_light.bindValue(':ok_norm', self.ok_standart_light.text())
        self.query_to_light.bindValue(':not_norm', self.no_standart_light.text())

        self.query_to_noise = QtSql.QSqlQuery()
        self.query_to_noise.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[7])
        self.query_to_noise.bindValue(':ok_norm', self.ok_standart_noise.text())
        self.query_to_noise.bindValue(':not_norm', self.no_standart_noise.text())

        self.query_to_vibration = QtSql.QSqlQuery()
        self.query_to_vibration.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[8])
        self.query_to_vibration.bindValue(':ok_norm', self.ok_standart_vibration.text())
        self.query_to_vibration.bindValue(':not_norm', self.no_standart_vibration.text())

        self.query_to_emf = QtSql.QSqlQuery()
        self.query_to_emf.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[9])
        self.query_to_emf.bindValue(':ok_norm', self.ok_standart_emf.text())
        self.query_to_emf.bindValue(':not_norm', self.no_standart_emf.text())

        self.query_to_aeroionics = QtSql.QSqlQuery()
        self.query_to_aeroionics.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[10])
        self.query_to_aeroionics.bindValue(':ok_norm', self.ok_standart_aeroionics.text())
        self.query_to_aeroionics.bindValue(':not_norm', self.no_standart_aeroionics.text())

        self.query_to_ventilation = QtSql.QSqlQuery()
        self.query_to_ventilation.prepare(constants.PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB[11])
        self.query_to_ventilation.bindValue(':ok_norm', self.ok_standart_ventilation.text())
        self.query_to_ventilation.bindValue(':not_norm', self.no_standart_ventilation.text())

        self.queries_list = (self.query_to_protocols, self.query_to_first_date, self.query_to_last_date,
                             self.query_to_object_name, self.query_to_object_address, self.query_to_microclimate,
                             self.query_to_light, self.query_to_noise, self.query_to_vibration, self.query_to_emf,
                             self.query_to_aeroionics, self.query_to_ventilation)

    @QtCore.pyqtSlot()
    def add_record_to_database(self):
        self.connection_with_database.open()

        self.ready_queries_to_database()

        '''if self.query_to_protocols.exec():
            print('Ok!')
        else:
            print('Bad!')
        if self.query_to_first_date.exec():
            print('Ok!')
        else:
            print('Bad!')
        if self.query_to_last_date.exec():
            print('Ok!')
        else:
            print('Bad!')'''

        for query in self.queries_list:
            check = query.exec()
            if check:
                print('Ok!')
            else:
                print('Bad!')

        self.connection_with_database.close()


class RadiationControlOptions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ok_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.ok_standart_eeva = QtWidgets.QSpinBox(self)                  # equivalent equilibrium volumetric activity
        self.ok_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.no_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.no_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.no_standart_eeva = QtWidgets.QSpinBox(self)
        self.no_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.entry_objects_radiation_control = (self.ok_standart_gamma_radiation,
                                                self.ok_standart_radon_volume_activity, self.ok_standart_eeva,
                                                self.ok_standart_radon_flux_density, self.no_standart_gamma_radiation,
                                                self.no_standart_radon_volume_activity, self.no_standart_eeva,
                                                self.no_standart_radon_flux_density)

        for entry_object in self.entry_objects_radiation_control:
            entry_object.setFixedSize(constants.SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS)
            entry_object.setRange(0, 999)


class RadiationControlRegister(BaseRegister, RadiationControlOptions):
    def __init__(self):
        super().__init__()

        self.show()

    def create_radiation_control_area(self):








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table = PhysicalFactorsRegister()
    sys.exit(app.exec())
