from PyQt6 import QtCore


# Постоянные значения главного интерфейса и меню #######################################################################

HELP_INFO_MESSAGE = ("Справка",
                     "1.  Расчет единичного измерения массовой концентрации взвешенных веществ в атмосферном воздухе.\n"
                     "РД 52.04.896-2020 «Массовая концентрация взвешенных веществ в пробах атмосферного воздуха. "
                     "Методика измерений гравиметрическим методом»\n\n2.  Расчет единичного измерения массовой "
                     "концентрации пыли (дисперсной фазы аэрозолей) в пробах воздуха рабочей зоны.\n"
                     "МУК 4.1.2468-09 «Измерение массовых концентраций пыли в воздухе рабочей зоны предприятий "
                     "горнорудной и нерудной промышленности»\n\n3.  Определение показателей эффективности вентиляции.\n"
                     "МР 4.3.0212-20 «Контроль систем вентиляции»\n\n4.  Расчет поправок для учета влияния  "
                     "фонового шума.\nМУК 4.3.3722-21 «Контроль уровня шума на территории жилой застройки, в жилых и "
                     "общественных зданиях и помещениях»")

ABOUT_INFO_MESSAGE = ("О программе", "Калькулятор Лабораторный 2.1\n\nСвободное ПО с окрытым исходным кодом\n\n"
                                     "(C) Иван Богданов, 2024. Все права защищены")

DARK_COLORS = ("#0a0a0a;", "#bbbbbb;", "#414a4c;", "#2c3337;", "#00bfff;", "#1a0000;", "#00b300;",
               "#1c1c1c;", "#022027;", "#9d9101;")

LIGHT_COLORS = ("#fcfcee;", "#18171c;", "#f5f5f5;", "#f0f8ff;", "#140f0b;", "#afeeee;", "#003399;",
                "#45cea2;", "#eedc82;", "#282828;")

MAIN_MENU_TITLE_NAMES = ("Файл", "Правка", "Вид", "Помощь", "Выход", "Темы", "Темная", "Светлая")

SELECTOR_PANEL_TITLE_NAMES = ("Калькуляторы", "Журналы")


# Значения объектов калькуляторов ######################################################################################

CALCULATORS_NAMES = ("Пыль в атмосферном воздухе", "Пыль в воздухе рабочей зоны", "Эффективность вентиляции",
                     "Учет влияния фонового шума")

ATMOSPHERIC_CALC_DUST_TITLE_NAMES = ("Объем взятого на анализ атмосферного воздуха, л",
                                     "Температура воздуха, прошедшего через ротаметр, ℃",
                                     "Атмосферное давление в месте отбора, мм.рт.ст., кПа",
                                     "Среднее значение массы фильтра до отбора пробы, г",
                                     "Среднее значение массы фильтра после отбора пробы, г")

ATMOSPHERIC_CALC_DUST_RESULT_NAMES = ("Массовая концентрация взвешенных веществ:",
                                      "Массовая концентрация взвешенных веществ: менее 0,15 мг/м³",
                                      "Массовая концентрация взвешенных веществ: более 10 мг/м³")

WORK_AREA_CALC_DUST_TITLE_NAMES = ("Объем воздуха, отобранный для анализа, л",
                                   "Температура воздуха в месте отбора пробы, ℃",
                                   "Барометрическое давление в месте отбора пробы, мм.рт.ст., кПа",
                                   "Масса фильтра до отбора пробы, г",
                                   "Масса фильтра (с пылью) после отбора пробы, г")

WORK_AREA_CALC_DUST_RESULT_NAMES = ("Массовая концентрация пыли:", "Массовая концентрация пыли: менее 1,0 мг/м³",
                                    "Массовая концентрация пыли: более 250 мг/м³")

VENTILATION_CALC_TITLE_NAMES = ("Площадь помещения, м²", "Высота помещения, м", "Скорость движения воздуха "
                                                                                "в вентиляционном отверстии, м/с",
                                "Диаметр, см", "Ширина, см", "Высота, см")

VENTILATION_CALC_RESULT_NAMES = ("Производительность вентиляции:", "Кратность воздухообмена:")

NOISE_CALC_BANDLINE_NAMES = ("31.5", "63", "125", "250", "500", "1K", "2K", "4K", "8K", "L(AS)")

NOISE_CALC_RESULT_NAMES = ("Общий уровень", "Фоновый уровень", "Разность с фоном >", "С поправкой на фон >")


# Значения журналов ####################################################################################################

DATABASE_NAME = 'registers_data.db'

REGISTERS_NAMES = ("Журнал физических факторов", "Журнал радиационного контроля")

BASE_REGISTER_TITLE_NAMES = ("Номер протокола", "Дата проведения измерений", "Дата выпуска протокола", "Вид работ",
                             "Наименование объекта", "Адрес объекта", "Исполнитель (Ф.И.О.)")

WORK_TYPE_AUTO_NAMES = ("поручение", "план", "проф. визит", "заявка", "договор", "контракт")

EMPLOYEE_AUTO_NAMES = ("Люлькова Н.В.", "Мотыляк А.А.", "Житникова В.В.", "Богданов И.И.")

TYPE_STANDART_NAMES = ("соотв.", "не соотв.")

PHYSICAL_FACTORS_TITLE_NAMES = ("Микроклимат", "Освещенность", "Шум", "Вибрация", "ЭМП", "Аэроионы", "Вентиляция")

RADIATION_CONTROL_TITLE_NAMES = ("МЭД гамма-излучения", "Объемная активность радона", "ЭРОА радона",
                                 "Плотность потока радона")

#BUTTON_TEXT = ("Сохранить протокол")

BASE_REGISTER_COMMANDS_INSERT = ("INSERT INTO protocols (number, protocol_date, work_type, employee) "
                                 "VALUES (:number, :protocol_date, :work_type, :employee)",
                                 "INSERT INTO dates_of_research (current_date) VALUES (:current_date)",
                                 "INSERT INTO objects_names (name) VALUES (:name)",
                                 "INSERT INTO objects_addresses (address) VALUES (:address)")




'''PHYSICAL_FACTORS_COMMANDS_ADD_TO_DB = ("INSERT INTO protocols (number, type, employee) "
                                       "VALUES (:number, :type, :employee)",
                                       "INSERT INTO first_date (date) VALUES (:date)",
                                       "INSERT INTO last_date (date) VALUES (:date)",
                                       "INSERT INTO object_name (name) VALUES (:name)",
                                       "INSERT INTO object_address (address) VALUES (:address)",
                                       "INSERT INTO microclimate (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO light (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO noise (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO vibration (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO emf (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO aeroionics (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)",
                                       "INSERT INTO ventilation (ok_norm, not_norm) VALUES (:ok_norm, :not_norm)")'''


# Выравнивания и размеры объектов и элементов ##########################################################################

ALIGNMENT_LEFT_CENTER = QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft

ALIGNMENT_CENTER_CENTER = QtCore.Qt.AlignmentFlag.AlignCenter

ALIGNMENT_TOP_LEFT = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft

ALIGNMENT_LEFT_BOTTOM = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft

SIZE_AIR_CALC_OBJECT = QtCore.QSize(500, 250)

SIZE_VENTILATION_CALC_OBJECT = QtCore.QSize(500, 300)

SIZE_NOISE_CALC_OBJECT = QtCore.QSize(630, 100)

SIZE_OTHERS_ENTRY_OBJECTS = QtCore.QSize(80, 25)

SIZE_VENTILATION_HOLE_ENTRY_OBJECTS = QtCore.QSize(60, 30)

SIZE_NOISE_CALC_ENTRY_OBJECTS = QtCore.QSize(40, 25)

SIZE_SELECTOR_AREA = QtCore.QSize(150, 200)

SIZE_PHYS_FACTORS_TABLE_ENTRY_OBJECTS = QtCore.QSize(45, 25)

SIZE_BASE_REGISTER_OBJECT_DATA = QtCore.QSize(200, 25)

CONTENTS_MARGINS_CALC_OBJECTS = QtCore.QMargins(5, 5, 5, 5)
