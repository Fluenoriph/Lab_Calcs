from PyQt6 import QtCore


data_library = {
    "Справка": "1.  Расчет единичного измерения массовой концентрации взвешенных веществ в атмосферном воздухе.\n"
                     "РД 52.04.896-2020 «Массовая концентрация взвешенных веществ в пробах атмосферного воздуха. "
                     "Методика измерений гравиметрическим методом»\n\n2.  Расчет единичного измерения массовой "
                     "концентрации пыли (дисперсной фазы аэрозолей) в пробах воздуха рабочей зоны.\n"
                     "МУК 4.1.2468-09 «Измерение массовых концентраций пыли в воздухе рабочей зоны предприятий "
                     "горнорудной и нерудной промышленности»\n\n3.  Определение показателей эффективности вентиляции.\n"
                     "МР 4.3.0212-20 «Контроль систем вентиляции»\n\n4.  Расчет поправок для учета влияния  "
                     "фонового шума.\nМУК 4.3.3722-21 «Контроль уровня шума на территории жилой застройки, в жилых и "
                     "общественных зданиях и помещениях»",

    "О программе": "Лабораторные калькуляторы 2.1.0 Beta\n\nFree software\n\n"
                                     "(C) Иван Богданов, 2025. Все права защищены\n\nfluenoriph@gmail.com",

    "Отчет": ("\\air_calc_result_log.txt", "\\work_zone_calc_result_log.txt", "\\ventilation_calc_result_log.txt",
              "\\noise_calc_result_log.txt", "Данные рассчета будут сохранены\nна рабочий стол в файл ",
              "\n----------------------------------------------------------------------\n"),

    "Светлая тема": {
        "Главный стиль": "* {font: 13px arial, sans-serif; background-color: #fff5ee;} "
                         "QMenuBar, QMenu {color: #1b1116; background-color: #c7fcec;}",
        "Стиль селектора": "border-style: hidden; border-radius: 9px; background-color: #c7fcec; color: #1b1116;",
        "Цвет названий калькуляторов": "color: #1e213d;",
        "Стиль области ввода": "* {color: #151719;} QLineEdit {background-color: #1cd3a2; color: #4d4234;}",
        "Стиль поля результатов": "border-style: hidden; border-radius: 5px; background-color: #6699cc; color: #4d1933;"
    },

    "Темная тема": {
        "Главный стиль": "* {font: 13px arial, sans-serif; background-color: #fcfcee;} "
                         "QMenuBar, QMenu {color: red; background-color: #18171c;}",
        "Стиль селектора": "border-style: hidden; border-radius: 9px; background-color: red; color: blue;",
        "Цвет названий калькуляторов": "color: blue;",
        "Стиль области ввода": "* {color: green;} QLineEdit {background-color: red; color: blue;}",
        "Стиль поля результатов": "border-style: hidden; border-radius: 5px; background-color: #181454; color: ;"
    },

    "Размеры зоны выбора": QtCore.QSize(150, 493),

    "Размеры кнопок": QtCore.QSize(40, 40),

    "Позиция левый-центр": QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft,

    "Позиция центр": QtCore.Qt.AlignmentFlag.AlignCenter,

    "Позиция левый-верхний": QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft,

    "Позиция нижний-центр": QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter,

    "Калькуляторы": {
        "Пыль в атмосф. воздухе": {
            "Параметры": ("Объем взятого на анализ атмосферного воздуха, л",
                          "Температура воздуха, прошедшего через ротаметр, ℃",
                          "Атмосферное давление в месте отбора, мм.рт.ст., кПа",
                          "Среднее значение массы фильтра до отбора пробы, г",
                          "Среднее значение массы фильтра после отбора пробы, г"),
            "Результаты": ("Массовая концентрация взвешенных веществ:",
                           "Массовая концентрация взвешенных веществ: менее 0,15 мг/м³",
                           "Массовая концентрация взвешенных веществ: более 10 мг/м³")
        },

        "Пыль в воздухе раб. зоны": {
            "Параметры": ("Объем воздуха, отобранный для анализа, л",
                        "Температура воздуха в месте отбора пробы, ℃",
                        "Барометрическое давление в месте отбора пробы, мм.рт.ст., кПа",
                        "Масса фильтра до отбора пробы, г",
                        "Масса фильтра (с пылью) после отбора пробы, г"),
            "Результаты": ("Массовая концентрация пыли:", "Массовая концентрация пыли: менее 1,0 мг/м³",
                           "Массовая концентрация пыли: более 250 мг/м³")
        },

        "Эффектив. вентиляции": {
            "Параметры": ("Площадь помещения, м²", "Высота помещения, м",
                          "Скорость движения воздуха в вентиляционном отверстии, м/с", "Диаметр, см", "Ширина, см",
                          "Высота, см"),
            "Результаты": ("Производительность вентиляции:", "Кратность воздухообмена:"),
            "Размеры поля ввода параметров отверстия": QtCore.QSize(60, 30)
        },

        "Учет влияния фонового шума": {
            "Параметры": ("31.5", "63", "125", "250", "500", "1K", "2K", "4K", "8K", "L(AS)"),
            "Результаты": ("Общий уровень", "Фоновый уровень", "Разность с фоном", "С поправкой на фон"),
            "Размеры": QtCore.QSize(680, 230),
            "Размеры поля ввода": QtCore.QSize(40, 30)
        },

        "Размеры базовые": QtCore.QSize(600, 470),
        "Размеры поля ввода": QtCore.QSize(80, 30),
        "Размеры поля результатов": QtCore.QSize(550, 70),
        "Отступы": QtCore.QMargins(10, 30, 10, 10)
    },

    "Журналы": {
        "Основной регистратор": {
            "Параметры": ("Дата проведения измерений", "Дата выпуска протокола", "Номер протокола", "Вид работ",
                          "Наименование объекта", "Адрес объекта", "Исполнитель (Ф.И.О.)"),
            "Тип": ("поручение", "план", "проф. визит", "заявка", "договор", "контракт"),
            "Сотрудники": ("Люлькова Н.В.", "Мотыляк А.А.", "Житникова В.В.", "Богданов И.И."),
            "Запись в базу данных": ("INSERT INTO protocols (number, protocol_date, work_type, employee) "
                                     "VALUES (:number, :protocol_date, :work_type, :employee)",
                                     "INSERT INTO dates_of_research (current_date) VALUES (:current_date)",
                                     "INSERT INTO objects_names (name) VALUES (:name)",
                                     "INSERT INTO objects_addresses (address) VALUES (:address)"),
            "Размеры поля ввода инфо. протокола": QtCore.QSize(100, 30),
            "Размеры поля ввода инфо. объекта": QtCore.QSize(200, 30)
        },

        "Физические факторы": {
            "Параметры": ("(соотв./ не соотв.)", "Микроклимат", "Освещенность", "Шум", "Вибрация", "ЭМП", "Аэроионы",
                          "Вентиляция"),
            "Запись в базу данных": ("INSERT INTO microclimate (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO light (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO noise (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO vibration (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO emf (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO aeroionics (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO ventilation (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)")
        },

        "Радиационные факторы": {
            "Параметры": ("(соотв./ не соотв.)", "МЭД гамма-излучения", "Объемная активность радона", "ЭРОА радона",
                               "Плотность потока радона"),
            "Запись в базу данных": ("INSERT INTO gamma_radiation (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO radon_volume_activity (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO eeva (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)",
                                     "INSERT INTO radon_flux_density (ok_standart, no_standart) VALUES (:ok_standart, :no_standart)")
        },

        "Размеры поля ввода факторов": QtCore.QSize(55, 30)
    }
}
