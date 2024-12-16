from PyQt6 import QtCore
from winpath import get_desktop


# Файлы сохранения результатов

USER_DESKTOP_PATH = get_desktop() + '\\'

CALCS_RESULT_FILES = ('air_calc_result_log.txt', 'work_zone_calc_result_log.txt', 'ventilation_calc_result_log.txt',
                      'noise_calc_result_log.txt')

ATMOSPHERIC_CALC_RESULT_PATH = USER_DESKTOP_PATH + CALCS_RESULT_FILES[0]

WORK_AREA_CALC_RESULT_PATH = USER_DESKTOP_PATH + CALCS_RESULT_FILES[1]

VENTILATION_CALC_RESULT_PATH = USER_DESKTOP_PATH + CALCS_RESULT_FILES[2]

NOISE_CALC_RESULT_PATH = USER_DESKTOP_PATH + CALCS_RESULT_FILES[3]

SEPARATOR = "\n----------------------------------------------------------------------\n"


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

ABOUT_INFO_MESSAGE = ("О программе", "Лабораторные калькуляторы 2.1.0 Beta\n\nFree software\n\n"
                                     "(C) Иван Богданов, 2025. Все права защищены\n\nfluenoriph@gmail.com")


# 0. Главный стиль; 1. Стиль селектора; 2. Цвет названий калькуляторов; 3. Стиль области ввода; 4. Стиль поля результатов;

TYPE_LIGHT_STYLE = ("* {font: 13px arial, sans-serif; background-color: #fff5ee;} "
                    "QMenuBar {color: #161a1e; background-color: #f0f8ff;}",
                    "border-style: hidden; border-radius: 9px; background-color: #a3c6c0; color: #1b1116;",
                    "color: #151719;", "* {color: #18171c;} QLineEdit {background-color: #e4a010; color: #1d1018;}", "border-style: hidden; "
                    "border-radius: 5px; background-color: #6699cc; color: #1c1c1c;")

TYPE_DARK_STYLE = ("* {font: 13px arial, sans-serif; background-color: #fcfcee;} "
                    "QMenuBar {color: red; background-color: #18171c;}",
                    "border-style: hidden; border-radius: 9px; background-color: red; color: blue;", "color: blue;",
                    "* {color: green;} QLineEdit {background-color: red; color: blue;}", "border-style: hidden; "
                    "border-radius: 5px; background-color: #181454; color: ;")


MAIN_MENU_TITLE_NAMES = ("Файл", "Вид", "Помощь", "Выход", "Темы", "Темная", "Светлая")

SELECTOR_PANEL_TITLE_NAMES = ("Калькуляторы", "Журналы")


# Значения объектов калькуляторов ######################################################################################

CALCULATORS_NAMES = ("Пыль в атмосф. воздухе", "Пыль в воздухе раб. зоны", "Эффектив. вентиляции", "Учет влияния фонового шума")

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

NOISE_CALC_RESULT_NAMES = ("Общий уровень", "Фоновый уровень", "Разность с фоном", "С поправкой на фон")


# Значения журналов ####################################################################################################

DATABASE_NAME = 'register_data.db'

REGISTERS_NAMES = ("Физические факторы", "Радиационные факторы")

BASE_REGISTER_TITLE_NAMES = ("Дата проведения измерений", "Дата выпуска протокола", "Номер протокола", "Вид работ",
                             "Наименование объекта", "Адрес объекта", "Исполнитель (Ф.И.О.)")

WORK_TYPE_AUTO_NAMES = ("поручение", "план", "проф. визит", "заявка", "договор", "контракт")

EMPLOYEE_AUTO_NAMES = ("Люлькова Н.В.", "Мотыляк А.А.", "Житникова В.В.", "Богданов И.И.")

PHYSICAL_FACTORS_TITLE_NAMES = ("(соотв./ не соотв.)", "Микроклимат", "Освещенность", "Шум", "Вибрация", "ЭМП",
                                "Аэроионы", "Вентиляция")

RADIATION_CONTROL_TITLE_NAMES = ("(соотв./ не соотв.)", "МЭД гамма-излучения", "Объемная активность радона", "ЭРОА радона",
                                 "Плотность потока радона")

BASE_REGISTER_COMMANDS_INSERT = ("INSERT INTO protocols (number, protocol_date, work_type, employee) "
                                 "VALUES (:number, :protocol_date, :work_type, :employee)",
                                 "INSERT INTO dates_of_research (current_date) VALUES (:current_date)",
                                 "INSERT INTO objects_names (name) VALUES (:name)",
                                 "INSERT INTO objects_addresses (address) VALUES (:address)")

PHYSICAL_REGISTER_COMMANDS_INSERT = ("INSERT INTO microclimate (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO light (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO noise (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO vibration (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO emf (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO aeroionics (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO ventilation (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)")

RADIATION_REGISTER_COMMANDS_INSERT = ("INSERT INTO gamma_radiation (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                      "INSERT INTO radon_volume_activity (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                      "INSERT INTO eeva (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                      "INSERT INTO radon_flux_density (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)")


# Выравнивания и размеры объектов и элементов ##########################################################################

ALIGNMENT_LEFT_CENTER = QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft

ALIGNMENT_CENTER_CENTER = QtCore.Qt.AlignmentFlag.AlignCenter

ALIGNMENT_TOP_LEFT = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft

ALIGNMENT_LEFT_BOTTOM = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft

ALIGNMENT_TOP_RIGHT = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight

ALIGNMENT_BOTTOM_CENTER = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter

SIZE_AIR_FLOW_CALC = QtCore.QSize(600, 470)

SIZE_NOISE_CALC = QtCore.QSize(680, 230)

SIZE_OTHERS_ENTRY_OBJECTS = QtCore.QSize(80, 30)

SIZE_VENTILATION_HOLE_ENTRY_OBJECTS = QtCore.QSize(60, 30)

SIZE_NOISE_CALC_ENTRY_OBJECTS = QtCore.QSize(40, 30)

SIZE_RESULT_FIELD = QtCore.QSize(550, 70)

SIZE_SELECTOR_AREA = QtCore.QSize(150, 488)

SIZE_OPTIONS_AREA_ENTRY_OBJECTS = QtCore.QSize(55, 30)

SIZE_BASE_REGISTER_OBJECT_DATA = QtCore.QSize(200, 30)

SIZE_BASE_REGISTER_PROTOCOL_INFO = QtCore.QSize(100, 30)

CONTENTS_MARGINS_ALL_OBJECTS = QtCore.QMargins(5, 5, 5, 5)

CONTENTS_MARGINS_NULLS = QtCore.QMargins(0, 0, 0, 0)

CONTENTS_MARGINS_CALCS = QtCore.QMargins(10, 30, 10, 10)
