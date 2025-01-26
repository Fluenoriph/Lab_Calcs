from PyQt6 import QtCore


data_library = {
    "Главное меню": ("Файл", "Выход", "Помощь", "Сменить тему"),

    "Справка": "1.  Расчет единичного измерения массовой концентрации взвешенных веществ в атмосферном воздухе.\n"
                    "РД 52.04.896-2020 «Массовая концентрация взвешенных веществ в пробах атмосферного воздуха. "
                    "Методика измерений гравиметрическим методом»\n\n"
               "2.  Расчет единичного измерения массовой концентрации пыли (дисперсной фазы аэрозолей) в пробах воздуха "
                    "рабочей зоны.\n"
                    "МУК 4.1.2468-09 «Измерение массовых концентраций пыли в воздухе рабочей зоны предприятий "
                    "горнорудной и нерудной промышленности»\n\n"
               "3.  Определение показателей эффективности вентиляции.\n"
                    "МР 4.3.0212-20 «Контроль систем вентиляции»\n\n"
               "4.  Расчет поправок для учета влияния фонового шума.\n"
                    "МУК 4.3.3722-21 «Контроль уровня шума на территории жилой застройки, в жилых и общественных "
                    "зданиях и помещениях»",

    "О программе": "Calculators 2.1.0 Beta\n\n"
                   "Free software\n\n"
                   "(C) Иван Богданов, 2025. Все права защищены\n"
                   "fluenoriph@gmail.com, fluenoriph@yandex.ru",

    "Отчет": ("\\air_calc_result_log.txt", "\\work_zone_calc_result_log.txt", "\\ventilation_calc_result_log.txt",
              "\\noise_calc_result_log.txt", "Данные рассчета будут сохранены\nна рабочий стол в файл ",
              "\n----------------------------------------------------------------------\n"),

    "Светлая тема": {
        "Главный стиль": "* {border-style: none; background: #fff5ee; font: 13px arial, sans-serif;} "
                         
                         "QMenuBar, QMenu {background: #c7fcec; color: #1b1116;} "
                         "QMenuBar::item:selected {background: red;} "
                         "QMenu::item:selected {background: red;} "
                                                                         
                         "QPushButton {border-radius: 11px; padding: 3px;} "
                         "QPushButton:hover {background: blue;} "
                         "QPushButton:pressed {background: red;} "
                         "QPushButton:focus {background: blue;} "
                                                  
                         "QMessageBox QWidget {color: #1b1116;} "
                         "QMessageBox .QPushButton {border-radius: 4px; padding: 6px 12px 4px 12px; "
                         "background: red;} "
                         "QMessageBox .QPushButton:pressed {background: blue;}",

        "Стиль селектора": "* {outline: 0; border-radius: 9px; background: #c7fcec; color: #1b1116;} "
                           
                           "QListView::item {border-radius: 3px; padding: 2px;} "
                           "QListView::item:hover {background: red;} "
                           "QListView::item:selected {background: blue;}",

        "Стиль контроллера": "* {color: #781f19;} ",

        "Стиль области ввода": "QLabel {color: #151719;} "
                               "QLineEdit, QDateEdit, QSpinBox {border-radius: 5px; background: #1cd3a2; color: #4d4234;} "
                               "QLineEdit:focus {background: green;} "
                               "QDateEdit:focus {background: green;} "
                               "QSpinBox:focus {background: green;}",

        "Стиль поля результатов": "border-radius: 5px; background: #6699cc; color: #641c34;"
    },

    "Темная тема": {
        "Главный стиль": "* {border-style: none; background: #fff5ee; font: 13px arial, sans-serif;} "
                         
                         "QMenuBar, QMenu {background: #c7fcec; color: #1b1116;} "
                         "QMenuBar::item:selected {background: red;} "
                         "QMenu::item:selected {background: red;} "
                                                                         
                         "QPushButton {border-radius: 11px; padding: 3px;} "
                         "QPushButton:hover {background: blue;} "
                         "QPushButton:pressed {background: red;} "
                         "QPushButton:focus {background: blue;} "
                                                  
                         "QMessageBox QWidget {color: #1b1116;} "
                         "QMessageBox .QPushButton {border-radius: 4px; padding: 6px 12px 4px 12px; "
                         "background: red;} "
                         "QMessageBox .QPushButton:pressed {background: blue;}",

        "Стиль селектора": "* {outline: 0; border-radius: 9px; background: #c7fcec; color: #1b1116;} "
                           
                           "QListView::item {border-radius: 3px; padding: 2px;} "
                           "QListView::item:hover {background: red;} "
                           "QListView::item:selected {background: blue;}",

        "Стиль контроллера": "* {color: #781f19;} ",

        "Стиль области ввода": "QLabel {color: #151719;} "
                               "QLineEdit, QDateEdit, QSpinBox {border-radius: 5px; background: #1cd3a2; color: #4d4234;} "
                               "QLineEdit:focus {background: green;} "
                               "QDateEdit:focus {background: green;} "
                               "QSpinBox:focus {background: green;}",

        "Стиль поля результатов": "border-radius: 5px; background: #6699cc; color: #641c34;"
    },

    "Размеры зоны выбора": QtCore.QSize(150, 493),

    "Размеры кнопок": QtCore.QSize(40, 40),

    "Позиция левый-центр": QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft,

    "Позиция центр": QtCore.Qt.AlignmentFlag.AlignCenter,

    "Позиция левый-верхний": QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft,

    "Позиция нижний-центр": QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter,

    "Отступы контроллеров": QtCore.QMargins(15, 15, 15, 15),

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



'''"Главный стиль": "* {font: 13px arial, sans-serif; background-color: #26252d;} "
                         "QMenuBar, QMenu {color: #c9c0bb; background-color: #151719;} QMessageBox QWidget {color: #c9c0bb;}",

        "Стиль селектора": "border-style: hidden; border-radius: 9px; background-color: #151719; color: #c9c0bb;",
        "Цвет названий калькуляторов": "* {color: #fdbdba;} QTabWidget {background-color: #26252d;}",
        "Стиль области ввода": "* {color: #01796f;} QLineEdit, QDateEdit, QSpinBox {border-style: hidden; border-radius: "
                               "5px; background-color: #343e40; color: #4169e1;}",
        "Стиль поля результатов": "border-style: hidden; border-radius: 5px; background-color: #0e1824; color: #baacc7;"'''
