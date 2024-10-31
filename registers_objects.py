from PyQt6 import QtWidgets, QtCore, QtSql

from constants import (BASE_REGISTER_TITLE_NAMES, SIZE_BASE_REGISTER_PROTOCOL_INFO, SIZE_BASE_REGISTER_OBJECT_DATA,
                       WORK_TYPE_AUTO_NAMES, EMPLOYEE_AUTO_NAMES, DATABASE_NAME, BASE_REGISTER_COMMANDS_INSERT,
                       PHYSICAL_FACTORS_TITLE_NAMES, SIZE_OPTIONS_AREA_ENTRY_OBJECTS, RADIATION_CONTROL_TITLE_NAMES,
                       PHYSICAL_REGISTER_COMMANDS_INSERT, RADIATION_REGISTER_COMMANDS_INSERT)

from application_classes import AbstractEntryArea


class BaseRegister(AbstractEntryArea):
    def __init__(self):
        super().__init__()
        self.box.setVerticalSpacing(15)
        self.box.setHorizontalSpacing(30)

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

        self.create_title_objects(BASE_REGISTER_TITLE_NAMES)
        self.create_entry_objects(self.entry_objects, row_count=0, column_count=1)
        self.set_size_entry_objects(self.entry_objects[:4], SIZE_BASE_REGISTER_PROTOCOL_INFO)
        self.set_size_entry_objects(self.entry_objects[4:6], SIZE_BASE_REGISTER_OBJECT_DATA)
        self.entry_objects[6].setFixedSize(120, 30)
        self.entry_objects[0].setMaxLength(10)

        self.work_type_completer = QtWidgets.QCompleter(WORK_TYPE_AUTO_NAMES, self)
        self.entry_objects[3].setCompleter(self.work_type_completer)
        self.administrator_completer = QtWidgets.QCompleter(EMPLOYEE_AUTO_NAMES, self)
        self.entry_objects[6].setCompleter(self.administrator_completer)

        self.connection_with_database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connection_with_database.setDatabaseName(DATABASE_NAME)

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
    def __init__(self):
        super().__init__()
        #self.setFixedSize(300, 400)
        self.box.setHorizontalSpacing(10)
        self.box.setVerticalSpacing(10)

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

        self.entry_objects_ok_standart_with_title = (self.create_ok_standart_title(), self.ok_standart_microclimate,
                                                     self.ok_standart_light, self.ok_standart_noise,
                                                     self.ok_standart_vibration, self.ok_standart_emf,
                                                     self.ok_standart_aeroionics, self.ok_standart_ventilation)

        self.entry_objects_no_standart_with_title = (self.create_no_standart_title(), self.no_standart_microclimate,
                                                     self.no_standart_light, self.no_standart_noise,
                                                     self.no_standart_vibration, self.no_standart_emf,
                                                     self.no_standart_aeroionics, self.no_standart_ventilation)

        self.entry_objects = self.entry_objects_ok_standart_with_title[1:] + self.entry_objects_no_standart_with_title[
                                                                             1:]

        self.create_title_objects(PHYSICAL_FACTORS_TITLE_NAMES)
        self.create_entry_objects(self.entry_objects_ok_standart_with_title, row_count=0, column_count=1)
        self.create_entry_objects(self.entry_objects_no_standart_with_title, row_count=0, column_count=2)
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
    def __init__(self):
        super().__init__()
        self.box.setHorizontalSpacing(20)
        self.box.setVerticalSpacing(5)

        self.ok_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_equivalent_equilibrium_volumetric_activity = QtWidgets.QSpinBox(self)
        self.ok_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.no_standart_gamma_radiation = QtWidgets.QSpinBox(self)
        self.no_standart_radon_volume_activity = QtWidgets.QSpinBox(self)
        self.no_standart_radon_equivalent_equilibrium_volumetric_activity = QtWidgets.QSpinBox(self)
        self.no_standart_radon_flux_density = QtWidgets.QSpinBox(self)

        self.entry_objects_ok_standart_with_title = (self.create_ok_standart_title(), self.ok_standart_gamma_radiation,
                                                     self.ok_standart_radon_volume_activity,
                                                     self.ok_standart_radon_equivalent_equilibrium_volumetric_activity,
                                                     self.ok_standart_radon_flux_density)

        self.entry_objects_no_standart_with_title = (self.create_no_standart_title(), self.no_standart_gamma_radiation,
                                                     self.no_standart_radon_volume_activity,
                                                     self.no_standart_radon_equivalent_equilibrium_volumetric_activity,
                                                     self.no_standart_radon_flux_density)

        self.entry_objects = self.entry_objects_ok_standart_with_title[1:] + self.entry_objects_no_standart_with_title[
                                                                             1:]

        self.create_title_objects(RADIATION_CONTROL_TITLE_NAMES)
        self.create_entry_objects(self.entry_objects_ok_standart_with_title, row_count=0, column_count=1)
        self.create_entry_objects(self.entry_objects_no_standart_with_title, row_count=0, column_count=2)
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
