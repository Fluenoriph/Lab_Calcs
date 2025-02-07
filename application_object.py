from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import sys
from winpath import get_desktop
import constants as ct
from calculators_objects import (AtmosphericAirDust, VentilationEfficiency, NoiseLevelsWithBackground, MainRegister,
                                 FactorsRegister, AbstractBaseCalc as calc_base)


class BaseAbstractController(QtWidgets.QWidget):
    def __init__(self, calcs_names, calcs_objects, icon_path):
        super().__init__()
        self.calcs_names = calcs_names
        self.calcs_objects = calcs_objects
        self.icon_path = icon_path
        self.buttons = []

        self.box = QtWidgets.QGridLayout(self)
        self.box.setContentsMargins(ct.data_library["Отступы контроллеров"])

    def create_options(self):
        area = QtWidgets.QTabWidget(self)
        area.setCurrentIndex(0)
        area.setUsesScrollButtons(False)

        r = range(len(self.calcs_names))
        [area.addTab(self.calcs_objects[_], self.calcs_names[_]) for _ in r]
        self.box.addWidget(area, 0, self.box.columnCount(), 8, 1, alignment=ct.data_library["Позиция левый-верхний"])
        return area

    def create_control_buttons(self):
        r = len(self.icon_path)
        y = self.box.columnCount()

        if r == 3:
            tooltips = ct.data_library["Иконки"][4:7]
        else:
            self.icon_path.reverse()
            tooltips = ct.data_library["Иконки"][7:9]

        f = lambda x: x + 1
        for _ in range(r):
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(self.icon_path[_]))
            button.setToolTip(tooltips[_])
            button.setToolTipDuration(3000)
            button.setIconSize(ct.data_library["Размеры кнопок"])
            button.setAutoDefault(True)
            self.buttons.append(button)
            self.box.addWidget(button, f(_), y, r, 1, ct.data_library["Позиция левый-верхний"])


class RegistersController(BaseAbstractController):
    n = list(ct.data_library["Журналы"].keys())

    def __init__(self):
        super().__init__(self.n[1:3],(FactorsRegister(),
                                          FactorsRegister(ct.data_library["Журналы"]["Радиационные факторы"])),
                                          list(ct.data_library["Иконки"][1:3]))
        self.register = MainRegister()
        self.box.addWidget(self.register, 0, 0, 8, 2, alignment=ct.data_library["Позиция левый-верхний"])

        self.reg_options = self.create_options()
        self.create_control_buttons()

        #self.options_zone.currentChanged.connect(self.clear_protocol_number)



    def get_visual_data(self):

        window = QtWidgets.QWidget()
        window.setWindowFlags(QtCore.Qt.WindowType.Window)
        window.resize(600, 800)
        box = QtWidgets.QVBoxLayout(window)
        data_model = QtSql.QSqlTableModel(window)
        data_model.setTable('protocols')
        data_model.setSort(1, QtCore.Qt.SortOrder.AscendingOrder)
        data_model.select()
        view_type = QtWidgets.QTableView(window)
        view_type.setModel(data_model)
        box.addWidget(view_type)
        window.show()






'''def save_physical_protocol(self):
        self.base_register_area.connection_with_database.open()

        queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
                        self.base_register_area.ready_insert_to_dates_of_research_table(),
                        self.base_register_area.ready_insert_to_objects_names_table(),
                        self.base_register_area.ready_insert_to_objects_addresses_table(),
                        
                        self.physical_register_options.ready_insert_to_microclimate_table(),
                        self.physical_register_options.ready_insert_to_light_table(),
                        self.physical_register_options.ready_insert_to_noise_table(),
                        self.physical_register_options.ready_insert_to_vibration_table(),
                        self.physical_register_options.ready_insert_to_emf_table(),
                        self.physical_register_options.ready_insert_to_aeroionics_table(),
                        self.physical_register_options.ready_insert_to_ventilation_table())

        self.check_read_to_database(queries_list)
        self.base_register_area.connection_with_database.close()

    def save_radiation_protocol(self):
        self.base_register_area.connection_with_database.open()

        queries_list = (self.base_register_area.ready_insert_to_protocol_table(),
                        self.base_register_area.ready_insert_to_dates_of_research_table(),
                        self.base_register_area.ready_insert_to_objects_names_table(),
                        self.base_register_area.ready_insert_to_objects_addresses_table(),
                        
                        self.radiation_control_register_options.ready_insert_to_gamma_radiation_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_volume_activity_table(),
                        self.radiation_control_register_options.ready_insert_to_eeva_table(),
                        self.radiation_control_register_options.ready_insert_to_radon_flux_density_table())

        self.check_read_to_database(queries_list)
        self.base_register_area.connection_with_database.close()

    def check_read_to_database(self, queries):
        for query in queries:
            check = query.exec()
            if not check:
                self.show_database_error()

    def show_database_error(self):
        QtWidgets.QMessageBox.critical(self, " ", "Ошибка записи в базу данных."
                                                  "\nНекоторые данные могли не сохраниться !")

    @QtCore.pyqtSlot()
    def select_insert_command(self):
        match self.options_area.currentIndex():
            case 0:
                self.save_physical_protocol()
            case 1:
                self.save_radiation_protocol()

    

    @QtCore.pyqtSlot()
    def clear_protocol_number(self):
        self.base_register_area.entry_objects_others[0].clear()'''


class CalculatorsController(BaseAbstractController):
    def __init__(self):
        super().__init__(list(ct.data_library["Калькуляторы"].keys()),
        (AtmosphericAirDust(), AtmosphericAirDust(ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"][0:5],
        ct.data_library["Калькуляторы"]["Пыль в воздухе раб. зоны"][5:12]), VentilationEfficiency(), NoiseLevelsWithBackground()),
                         list(ct.data_library["Иконки"][0:3]))

        self.calc_options = self.create_options()
        self.create_control_buttons()

        self.buttons[0].clicked.connect(self.calculating)
        self.buttons[1].clicked.connect(self.clearing)
        self.buttons[2].clicked.connect(self.saving)

        self.message = lambda x: QtWidgets.QMessageBox.information(self, " ",
                                          f"{ct.data_library["Отчет"][4]}\'{ct.data_library["Отчет"][x][1:]}\'")

    def save_basic_calc(self, calc):
        if calc.result_area.text() != "":
            data = [calc.parameters[_] + ': ' + calc.entry_objects[_].text() + '\n' for _ in range(len(calc.parameters))]
            data.append('\n' + calc.result_area.text() + ct.data_library["Отчет"][5])
            i = self.calcs_objects.index(calc)

            self.message(i)
            self.write_to_file(i, data)
        else:
            return

    def save_noise_calc(self):
        if self.calcs_objects[3].octave_table[3][0].text() != "":
            data = [ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][10].ljust(20)]
            [data.append(_.ljust(8)) for _ in ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][0:10]]
            data.append(ct.data_library["Отчет"][5])

            for n, i in enumerate(self.calcs_objects[3].octave_table):
                data.append(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][11:15][n].ljust(20))
                [data.append(j.text().ljust(8)) for j in i]
                data.append('\n')
            data.append('\n')

            self.message(3)
            self.write_to_file(3, data)
        else:
            return

    @QtCore.pyqtSlot()
    def calculating(self):
        match self.calc_options.currentIndex():
            case 0:
                if calc_base.check_parameters(self.calcs_objects[0].entry_objects):
                    self.calcs_objects[0].calculate()
                else:
                    return
            case 1:
                if calc_base.check_parameters(self.calcs_objects[1].entry_objects):
                    self.calcs_objects[1].calculate()
                else:
                    return
            case 2:
                if (calc_base.check_parameters(self.calcs_objects[2].entry_objects[0:3]) and
                        self.calcs_objects[2].set_hole_checks()):
                    self.calcs_objects[2].calculate()
                else:
                    return
            case 3:
                self.calcs_objects[3].calculate()

    @QtCore.pyqtSlot()
    def clearing(self):
        match self.calc_options.currentIndex():
            case 0:
                [_.clear() for _ in self.calcs_objects[0].entry_objects]
                [calc_base.reset_value(_) for _ in self.calcs_objects[0].entry_objects]
                self.calcs_objects[0].result_area.clear()
            case 1:
                [_.clear() for _ in self.calcs_objects[1].entry_objects]
                [calc_base.reset_value(_) for _ in self.calcs_objects[1].entry_objects]
                self.calcs_objects[1].result_area.clear()
            case 2:
                [_.clear() for _ in self.calcs_objects[2].entry_objects]
                [calc_base.reset_value(_) for _ in self.calcs_objects[2].entry_objects]
                self.calcs_objects[2].result_area.clear()
            case 3:
                [j.clear() for i in self.calcs_objects[3].octave_table for j in i]
                [calc_base.reset_value(j) for i in self.calcs_objects[3].octave_table for j in i]

    @QtCore.pyqtSlot()
    def saving(self):
        match self.calc_options.currentIndex():
            case 0:
                self.save_basic_calc(self.calcs_objects[0])
            case 1:
                self.save_basic_calc(self.calcs_objects[1])
            case 2:
                self.save_basic_calc(self.calcs_objects[2])
            case 3:
                self.save_noise_calc()

    @staticmethod
    def write_to_file(calc_index, data):
        with open(get_desktop() + ct.data_library["Отчет"][calc_index], "a", encoding="utf-8") as txt:
            txt.writelines(data)

class ApplicationType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        QtWidgets.QApplication.setOrganizationName("Ivan Bogdanov")
        QtWidgets.QApplication.setApplicationName("Calculators 2.1.0 Beta")
        settings = QtCore.QSettings(self)

        self.setWindowTitle("Калькуляторы")
        self.resize(1015, 550)
        self.move(self.width() * -2, 0)
        screen_size = self.screen().availableSize()
        x = (screen_size.width() - self.frameSize().width()) // 2
        y = (screen_size.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.activateWindow()

        self.box = QtWidgets.QGridLayout(self)
        self.box.setHorizontalSpacing(5)
        self.box.setVerticalSpacing(15)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.data_dict_names = list(ct.data_library.keys())

        self.menu_area = self.create_main_menu()
        self.selector_area = self.create_selector_panel()
        self.registers_area = RegistersController()
        self.calculators_area = CalculatorsController()

        self.set_style(ct.data_library["Цвета светлой темы"])

        settings.beginWriteArray("Light Style")
        for i, el in enumerate(ct.data_library["Цвета светлой темы"]):
            settings.setArrayIndex(i)
            settings.setValue("Color", el)

        settings.endArray()
        settings.sync()

        self.box.addWidget(self.menu_area, 0, 0, 1, 4)
        self.box.addWidget(self.selector_area, 1, 1, 1, 1, ct.data_library["Позиция левый-верхний"])
        self.box.addWidget(self.calculators_area, 1, 2, 1, 1, ct.data_library["Позиция левый-верхний"])

        self.box.setColumnMinimumWidth(0, 1)
        self.show()

    def set_style(self, colors):
        x = ("* {outline: 0; border-style: none; background: "+colors[0]+" font: 13px arial, sans-serif;} "
                                                                         
             "QMenuBar, QMenu {background: "+colors[0]+" color: "+colors[2]+"} QLabel {color: "+colors[6]+"} "   
             "QTabBar:tab {border-radius: 5px; padding: 5px; background: "+colors[9]+" color: "+colors[5]+"} "                          
             "QLineEdit, QDateEdit, QSpinBox, QComboBox {border-radius: 5px; background: "+colors[7]+" color: "+colors[8]+"} "
             "QTabWidget:pane {border-style: none;} "
             "QPushButton {border-radius: 9px; padding: 3px;} ")








        self.setStyleSheet(









                            "QMenuBar {border-bottom: 1px solid "+colors[2]+"} "
                            "QMenu::separator {border-bottom: 1px solid "+colors[2]+"} "                                      
                            "QToolTip {color: "+colors[2]+"} "
                           "QMessageBox QLabel {color: "+colors[2]+"} "                                                
                            "QListView::item {border-radius: 5px; padding: 2px; color: "+colors[2]+"} "                                        
                            
                            
                            "QListView::item:hover {background: "+colors[3]+"} "                                                                                        
                           "QMenuBar::item:selected {background: "+colors[3]+"} "
                           "QMenu::item:selected {background: "+colors[3]+"} "                                                                                           
                           "QPushButton:hover {background: "+colors[3]+"} "
                            "QMessageBox .QPushButton {border-radius: 5px; padding: 6px 16px 6px 16px; "
                           "background: "+colors[3]+"} "                            
                            "QTabBar:tab::hover {background: "+colors[3]+"} "       
                                                                       
                           "QPushButton:pressed {background: "+colors[4]+"} "                                                 
                           "QMessageBox .QPushButton:pressed {background: "+colors[4]+"}"
                            
                            "QListView::item:selected {background: "+colors[3]+" color: "+colors[4]+"}"                                                                    
                           "QTabBar:tab::selected {background: "+colors[3]+" color: "+colors[4]+"} "   
                                                                                                           
                                                                               
                                                                                                                                                        
                                                                                    
                           "QLabel#result_field {border-radius: 9px; background: "+colors[9]+" color: "+colors[10]+"} "
                           "QLabel#result_field_noise {border-radius: 5px; background: "+colors[9]+" color: "+colors[10]+"} "         
                                
                            "QListView {border-radius: 9px; background: "+colors[1]+"} "             
                           "QLineEdit:focus {background: "+colors[1]+"} "
                           "QDateEdit:focus {background: "+colors[1]+"} "
                           "QComboBox:selected {background: "+colors[1]+"} "
                           "QSpinBox:focus {background: "+colors[1]+"}")

    def create_main_menu(self):
        main_menu = QtWidgets.QMenuBar(self)
        main_menu.setFixedHeight(21)

        main_menu.submenu_file = QtWidgets.QMenu(ct.data_library["Главное меню"][0], main_menu)
        main_menu.submenu_help = QtWidgets.QMenu(ct.data_library["Главное меню"][2], main_menu)
        main_menu.change_style = QtGui.QAction(ct.data_library["Главное меню"][3], main_menu)
        main_menu.change_style.setCheckable(True)
        main_menu.change_style.toggled.connect(self.change_app_style)

        main_menu.addMenu(main_menu.submenu_file)
        main_menu.addMenu(main_menu.submenu_help)
        main_menu.addAction(main_menu.change_style)

        main_menu.set_calculators_act = QtGui.QAction(self.data_dict_names[24], main_menu.submenu_file)
        main_menu.set_calculators_act.triggered.connect(self.calculators_show_fixed)
        main_menu.set_registers_act = QtGui.QAction(self.data_dict_names[25], main_menu.submenu_file)
        main_menu.set_registers_act.triggered.connect(self.registers_show_fixed)
        main_menu.exit_act = QtGui.QAction(ct.data_library["Главное меню"][1], main_menu.submenu_file)
        main_menu.exit_act.triggered.connect(sys.exit)

        main_menu.submenu_file.addAction(main_menu.set_registers_act)
        main_menu.submenu_file.addAction(main_menu.set_calculators_act)
        main_menu.submenu_file.addSeparator()
        main_menu.submenu_file.addAction(main_menu.exit_act)

        main_menu.help_link = QtGui.QAction(self.data_dict_names[1], main_menu.submenu_help)
        main_menu.help_link.triggered.connect(self.open_help_message)

        main_menu.about = QtGui.QAction(self.data_dict_names[2], main_menu.submenu_help)
        main_menu.about.triggered.connect(self.open_about_app_message)

        main_menu.submenu_help.addAction(main_menu.help_link)
        main_menu.submenu_help.addSeparator()
        main_menu.submenu_help.addAction(main_menu.about)

        return main_menu

    def create_selector_panel(self):
        selector_panel = QtWidgets.QListView(self)
        selector_panel.setFixedSize(ct.data_library["Размеры зоны выбора"])
        selector_panel.setSpacing(10)
        selector_panel.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)

        selector_panel.names = (self.data_dict_names[24], self.data_dict_names[25])
        selector_panel.model_type = QtCore.QStringListModel(selector_panel.names)
        selector_panel.setModel(selector_panel.model_type)

        selector_panel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        selector_panel.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        selector_panel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        selector_panel.calculators_index = selector_panel.model_type.index(0, 0)
        selector_panel.registers_index = selector_panel.model_type.index(1, 0)
        selector_panel.clicked.connect(self.select_calcs_type)
        selector_panel.setCurrentIndex(selector_panel.calculators_index)

        return selector_panel

    @QtCore.pyqtSlot()
    def change_app_style(self):
        match self.menu_area.change_style.isChecked():
            case True:
                self.set_style(ct.data_library["Цвета темной темы"])
            case False:
                self.set_style(ct.data_library["Цвета светлой темы"])

    @QtCore.pyqtSlot()
    def open_about_app_message(self):
        QtWidgets.QMessageBox.about(self, self.data_dict_names[2], ct.data_library["О программе"])

    @QtCore.pyqtSlot()
    def open_help_message(self):
        QtWidgets.QMessageBox.information(self, self.data_dict_names[1], ct.data_library["Справка"])

    @QtCore.pyqtSlot()
    def calculators_show_fixed(self):
        self.registers_area.close()
        self.box.replaceWidget(self.registers_area, self.calculators_area)
        self.calculators_area.show()

    @QtCore.pyqtSlot()
    def registers_show_fixed(self):
        self.calculators_area.close()
        self.box.replaceWidget(self.calculators_area, self.registers_area)
        self.registers_area.show()

    @QtCore.pyqtSlot()
    def select_calcs_type(self):
        match self.selector_area.currentIndex():
            case self.selector_area.calculators_index:
                self.calculators_show_fixed()
            case self.selector_area.registers_index:
                self.registers_show_fixed()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ct.data_library["Иконки"][3]))
    #print(type(ct.data_library["Калькуляторы"]["Учет влияния фонового шума"][16]))
    app_calcs = ApplicationType()
    sys.exit(app.exec())
