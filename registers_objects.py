from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants
from application_classes import AbstractEntryArea


class BaseRegister(AbstractEntryArea):
    def __init__(self):
        super().__init__()
        self.visual_date = QtCore.QDate(2025, 1, 1)

        self.protocol_number = QtWidgets.QLineEdit(self)
        self.date_of_research = QtWidgets.QDateEdit(self.visual_date, self)
        self.protocol_date = QtWidgets.QDateEdit(self.visual_date, self)
        self.work_type = QtWidgets.QLineEdit(self)
        self.object_name = QtWidgets.QLineEdit(self)
        self.object_address = QtWidgets.QLineEdit(self)
        self.administrator = QtWidgets.QLineEdit(self)

        self.entry_objects = (self.protocol_number, self.date_of_research, self.protocol_date, self.work_type,
                              self.object_name, self.object_address, self.administrator)

        self.create_title_objects(constants.BASE_REGISTER_TITLE_NAMES)
        self.create_entry_objects(self.entry_objects)
        self.set_size_entry_objects(self.entry_objects[:4], constants.SIZE_OTHERS_ENTRY_OBJECTS)
        self.set_size_entry_objects(self.entry_objects[4:6], constants.SIZE_BASE_REGISTER_OBJECT_DATA)
        self.entry_objects[6].setFixedSize(100, 25)

        self.entry_objects[0].setMaxLength(10)     # add fields on len !!!!

        self.work_type_completer = QtWidgets.QCompleter(constants.WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(self.work_type_completer)

        self.administrator_completer = QtWidgets.QCompleter(constants.EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(self.administrator_completer)

        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connection_with_database.setDatabaseName(constants.DATABASE_NAME)

    def ready_insert_to_protocol_table(self):
        self.query_to_protocols = QtSql.QSqlQuery()
        self.query_to_protocols.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[0])
        self.query_to_protocols.bindValue(':number', self.protocol_number.text())
        self.query_to_protocols.bindValue(':protocol_date', self.protocol_date.text())
        self.query_to_protocols.bindValue(':work_type', self.work_type.text())
        self.query_to_protocols.bindValue(':employee', self.administrator.text())

    def ready_insert_to_dates_of_research_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':current_date', self.date_of_research.text())
        return query



    def ready_insert_to_objects_addresses_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':address', self.object_address.text())
        return query


class PhysicalFactorsOptions(QtWidgets.QWidget):
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

        self.entry_objects_phys_factors = (self.ok_standart_microclimate, self.ok_standart_light,
                                           self.ok_standart_noise, self.ok_standart_vibration, self.ok_standart_emf,
                                           self.ok_standart_aeroionics, self.ok_standart_ventilation,
                                           self.no_standart_microclimate, self.no_standart_light,
                                           self.no_standart_noise, self.no_standart_vibration, self.no_standart_emf,
                                           self.no_standart_aeroionics, self.no_standart_ventilation)

        for entry_object in self.entry_objects_phys_factors:
            entry_object.setFixedSize(constants.SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS)
            entry_object.setRange(0, 999)

        self.box =


'''class PhysicalFactorsRegister(BaseRegister, PhysicalFactorsOptions):
    def __init__(self):
        super().__init__()
        self.create_physical_factors_area()
        #self.show()

        # self.button_add_to_database.clicked.connect(self.add_record_to_database)

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


    def insert_to_database(self):
        self.connection_with_database.open()

        ob_name = self.object_name.text()
        self.query = QtSql.QSqlQuery()
        self.query.prepare(constants.BASE_REGISTER_COMMANDS_INSERT[2])
        self.query.bindValue(':name', ob_name)

        check = self.query.exec()
        if check:
            print('Ok!')
        else:
            print('Bad!')

        self.connection_with_database.close()'''


class RadiationControlOptions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.ok_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_equivalent_equilibrium_volumetric_activity = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.no_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.no_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.no_standart_radon_equivalent_equilibrium_volumetric_activity = QtWidgets.QSpinBox(self)
        self.no_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.entry_objects_radiation_control = (self.ok_standart_gamma_radiation,
                                                self.ok_standart_radon_volume_activity,
                                                self.ok_standart_radon_equivalent_equilibrium_volumetric_activity,
                                                self.ok_standart_radon_flux_density, self.no_standart_gamma_radiation,
                                                self.no_standart_radon_volume_activity,
                                                self.no_standart_radon_equivalent_equilibrium_volumetric_activity,
                                                self.no_standart_radon_flux_density)

        for entry_object in self.entry_objects_radiation_control:
            entry_object.setFixedSize(constants.SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS)
            entry_object.setRange(0, 999)


'''class RadiationControlRegister(BaseRegister, RadiationControlOptions):
    def __init__(self):
        super().__init__()
        self.create_radiation_control_area()
        #self.show()

    def create_radiation_control_area(self):
        self.box.addWidget(self.ok_standart_title, 0, 3, constants.ALIGNMENT_LEFT_BOTTOM)
        self.box.addWidget(self.no_standart_title, 0, 4, constants.ALIGNMENT_LEFT_BOTTOM)

        i = 1
        j = 0
        for title_object in range(len(constants.RADIATION_CONTROL_TITLE_NAMES)):
            title_object = QtWidgets.QLabel(constants.RADIATION_CONTROL_TITLE_NAMES[j], self)
            self.box.addWidget(title_object, i, 2, constants.ALIGNMENT_LEFT_CENTER)
            i += 1
            j += 1

        i = 1
        for entry_object_ok_standart in self.entry_objects_radiation_control[0:4]:
            self.box.addWidget(entry_object_ok_standart, i, 3, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

        i = 1
        for entry_object_no_standart in self.entry_objects_radiation_control[4:8]:
            self.box.addWidget(entry_object_no_standart, i, 4, constants.ALIGNMENT_LEFT_CENTER)
            i += 1

    def insert_to_database(self):
        self.connection_with_database.open()

        queries_list = (self.ready_insert_to_protocol_table(), self.ready_insert_to_dates_of_research_table(),
                        self.ready_insert_to_objects_names_table(), self.ready_insert_to_objects_addresses_table())

        for query in queries_list:
            check = query.exec()
            if check:
                print('Ok!')
            else:
                print('Bad!')

        self.connection_with_database.close()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #table = PhysicalFactorsRegister()
    rad = RadiationControlRegister()
    sys.exit(app.exec())'''
