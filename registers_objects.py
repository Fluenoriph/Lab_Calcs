from PyQt6 import QtWidgets, QtCore, QtSql

from constants import (BASE_REGISTER_TITLE_NAMES, SIZE_BASE_REGISTER_PROTOCOL_INFO, SIZE_BASE_REGISTER_OBJECT_DATA,
                       WORK_TYPE_AUTO_NAMES, EMPLOYEE_AUTO_NAMES, DATABASE_NAME, BASE_REGISTER_COMMANDS_INSERT,
                       PHYSICAL_FACTORS_TITLE_NAMES, SIZE_OPTIONS_AREA_ENTRY_OBJECTS, RADIATION_CONTROL_TITLE_NAMES,
                       PHYSICAL_REGISTER_COMMANDS_INSERT, RADIATION_REGISTER_COMMANDS_INSERT, ALIGNMENT_LEFT_CENTER)

from application_classes import AbstractEntryArea


class BaseRegister(AbstractEntryArea):
    def __init__(self, date_of_research=None, protocol_date=None, protocol_number=None, work_type=None,
                 object_name=None, object_address=None, administrator=None):
        super().__init__()
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)
        self.visual_date = QtCore.QDate(2025, 1, 1)

        self.parameters = (date_of_research, protocol_date, protocol_number, work_type, object_name, object_address,
                           administrator)

        self.create_title_objects(BASE_REGISTER_TITLE_NAMES)

        self.entry_objects = self.create_entry_objects(QtWidgets.QLineEdit, self.parameters, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[:4], SIZE_BASE_REGISTER_PROTOCOL_INFO)
        self.set_size_entry_objects(self.entry_objects[4:6], SIZE_BASE_REGISTER_OBJECT_DATA)
        self.entry_objects[6].setFixedSize(120, 30)
        self.entry_objects[2].setMaxLength(10)

        self.work_type_completer = QtWidgets.QCompleter(WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(self.work_type_completer)
        self.administrator_completer = QtWidgets.QCompleter(EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(self.administrator_completer)

        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connection_with_database.setDatabaseName(DATABASE_NAME)

    def create_entry_objects(self, entry_type, entry_objects_list, row_count, column_count):
        entry_objects = []

        for _ in entry_objects_list[0:2]:
            date_object = QtWidgets.QDateEdit(self.visual_date, self)
            entry_objects.append(date_object)
            self.box.addWidget(date_object, row_count, column_count, ALIGNMENT_LEFT_CENTER)
            row_count += 1

        for _ in entry_objects_list[2:7]:
            entry_object = entry_type(self)
            entry_objects.append(entry_object)
            self.box.addWidget(entry_object, row_count, column_count, ALIGNMENT_LEFT_CENTER)
            row_count += 1

        return tuple(entry_objects)

    def ready_insert_to_protocol_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(BASE_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':number', self.protocol_number.text())
        query.bindValue(':protocol_date', self.protocol_date.text())
        query.bindValue(':work_type', self.work_type.text())
        query.bindValue(':employee', self.administrator.text())
        return query

    def ready_insert_to_dates_of_research_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(BASE_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':current_date', self.date_of_research.text())
        return query

    def ready_insert_to_objects_names_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(BASE_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':name', self.object_name.text())
        return query

    def ready_insert_to_objects_addresses_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(BASE_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':address', self.object_address.text())
        return query


class PhysicalFactorsOptions(AbstractEntryArea):
    def __init__(self, microclimate=None, light=None, noise=None, vibration=None, emf=None, aeroionics=None,
                 ventilation=None):
        super().__init__()
        #self.setFixedSize(300, 400)
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)

        self.parameters = (microclimate, light, noise, vibration, emf, aeroionics, ventilation)

        self.create_title_objects(PHYSICAL_FACTORS_TITLE_NAMES)
        self.entry_objects_ok_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=1)
        self.entry_objects_no_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=2)

        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, SIZE_OPTIONS_AREA_ENTRY_OBJECTS)
        self.set_range_value(self.entry_objects)

    def ready_insert_to_microclimate_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':ok_standart', self.ok_standart_microclimate.text())
        query.bindValue(':no_standart', self.no_standart_microclimate.text())
        return query

    def ready_insert_to_light_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':ok_standart', self.ok_standart_light.text())
        query.bindValue(':no_standart', self.no_standart_light.text())
        return query

    def ready_insert_to_noise_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':ok_standart', self.ok_standart_noise.text())
        query.bindValue(':no_standart', self.no_standart_noise.text())
        return query

    def ready_insert_to_vibration_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':ok_standart', self.ok_standart_vibration.text())
        query.bindValue(':no_standart', self.no_standart_vibration.text())
        return query

    def ready_insert_to_emf_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[4])
        query.bindValue(':ok_standart', self.ok_standart_emf.text())
        query.bindValue(':no_standart', self.no_standart_emf.text())
        return query

    def ready_insert_to_aeroionics_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[5])
        query.bindValue(':ok_standart', self.ok_standart_aeroionics.text())
        query.bindValue(':no_standart', self.no_standart_aeroionics.text())
        return query

    def ready_insert_to_ventilation_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(PHYSICAL_REGISTER_COMMANDS_INSERT[6])
        query.bindValue(':ok_standart', self.ok_standart_ventilation.text())
        query.bindValue(':no_standart', self.no_standart_ventilation.text())
        return query


class RadiationControlOptions(AbstractEntryArea):
    def __init__(self, gamma_radiation=None, radon_volume_activity=None,
                 radon_equivalent_equilibrium_volumetric_activity=None, radon_flux_density=None):
        super().__init__()
        self.box.setHorizontalSpacing(20)
        self.box.setVerticalSpacing(5)

        self.parameters = (gamma_radiation, radon_volume_activity, radon_equivalent_equilibrium_volumetric_activity,
                           radon_flux_density)

        self.create_title_objects(RADIATION_CONTROL_TITLE_NAMES)

        self.entry_objects_ok_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=1)
        self.entry_objects_no_standart = self.create_entry_objects(QtWidgets.QSpinBox, self.parameters, row_count=1, column_count=2)

        self.entry_objects = self.entry_objects_ok_standart + self.entry_objects_no_standart
        self.set_size_entry_objects(self.entry_objects, SIZE_OPTIONS_AREA_ENTRY_OBJECTS)
        self.set_range_value(self.entry_objects)

    def ready_insert_to_gamma_radiation_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(RADIATION_REGISTER_COMMANDS_INSERT[0])
        query.bindValue(':ok_standart', self.ok_standart_gamma_radiation.text())
        query.bindValue(':no_standart', self.no_standart_gamma_radiation.text())
        return query

    def ready_insert_to_radon_volume_activity_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(RADIATION_REGISTER_COMMANDS_INSERT[1])
        query.bindValue(':ok_standart', self.ok_standart_radon_volume_activity.text())
        query.bindValue(':no_standart', self.no_standart_radon_volume_activity.text())
        return query

    def ready_insert_to_eeva_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(RADIATION_REGISTER_COMMANDS_INSERT[2])
        query.bindValue(':ok_standart', self.ok_standart_radon_equivalent_equilibrium_volumetric_activity.text())
        query.bindValue(':no_standart', self.no_standart_radon_equivalent_equilibrium_volumetric_activity.text())
        return query

    def ready_insert_to_radon_flux_density_table(self):
        query = QtSql.QSqlQuery()
        query.prepare(RADIATION_REGISTER_COMMANDS_INSERT[3])
        query.bindValue(':ok_standart', self.ok_standart_radon_flux_density.text())
        query.bindValue(':no_standart', self.no_standart_radon_flux_density.text())
        return query
