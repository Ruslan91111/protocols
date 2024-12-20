""" Объект класса MainCollector с уже собранными данными,
для проведения тестов."""

from league_sert.data_preparation.file_parser import MainCollector


def full_main_collector():
    """Тестовый объект класса MainCollector"""
    main_collector = MainCollector('file')
    main_collector.main_number = '8281/24-Д'
    main_collector.main_date = '29 августа 2024'
    main_collector.prod_control_data = {
        'number_of_protocol': '8303/24-Д', 'date_of_protocol': '23 августа 2024',
        'act': '8303 ОТ 13.08.2024',
        'place_of_measurement': 'г. Калуга, ул. Ленина, д. 58, магазин № 40515',
        'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                            'уровни освещенности рабочей поверхности, '
                            'шума и общей вибрации соответствуют требованиям'}

    main_collector.data_from_tables = {
        (1, 'MAIN'): {
            'Заявитель, ИНН': 'АО «ДИКСИ ЮГ», ИНН: 5036045205',
            'Юридический адрес': 'МО, г. Подольск, ул. Юбилейная, д. 32 А',
            'Фактический адрес места осуществления деятельности': 'г. Калуга, ул. Ленина, д.58 (№40515)',
            'Номер заявки и дата': '№8/24 от 10.01.2024 г.',
            'Место отбора проб': 'г. Калуга, ул. Ленина, д.58 (№40515)',
            'Дата и время отбора проб': '13.08.2024 г.. 09 ч. 15 мин.',
            'Дата и время доставки проб в лабораторию': '13.08.2024 г., 17 ч. 00 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 8281 от 13.08.2024 г.',
            'Количество зашифрованных проб': '3',
            'Протокол составлен в 2-х экземплярах': 'Протокол составлен в 2-х экземплярах'},

        (2, 'store_prod'): {
            'Шифр пробы': '8281-1', 'Г руппа продукции': 'Производство магазина',
            'Наименование продукции': 'Лепешка томаты с базиликом',
            'НД на продукцию': 'СТО 56811319-002-2017',
            'Дата производства продукции': '13.08.2024 г. Срок годности 12 часов',
            'Производитель (фирма, предприятие, организация)': 'АО «ДИКСИ ЮГ»',
            'Условия доставки': 'Автотранспорт, сумка-холодильник',
            'Температура при доставке проб': '+2°С',
            'Нарушения при доставке проб': 'Упаковка не нарушена',
            'Вид упаковки': 'Производственная упаковка', 'Масса пробы': '1200 г',
            'Цель исследования': 'Производственный контроль. На соответствие требованиям ТР ТС 021/2011 «О безопасности пищевой продукции», утв. Решением КТС от 9 декабря 2011 года № 880. На соответствие требованиям ТР ТС 029/2012 "Требования безопасности пищевых добавок, ароматизаторов и технологических вспомогательных средств", утв. Решением Совета ЕЭК от 20 июля 2012 года № 58',
            'Сведения о СИ': 'Весы лабораторные электронные AF-R220CE, № 086550117; хроматограф жидкост- ной/ионный Shimadzu Prominence L20495373590/L20105478938, L20155476179/ 20105478938; спектрометр атомно-абсорбционный «Квант-Z», № 042; спектрометр атомно-эмиссионный с индуктивно-связанной плазмой PlasmaQuant мод. PQ 9000, №13-5850Е-АТ 287; хроматограф газовый «Хроматэк-Кристалл 5000.2»/ЭЗД/ТИД.',
            'indicators': [
                {'Массовая доля сорбиновой кислоты, мг/кг': {'result': '<1,0*',
                                                             'norm': 'не более 2000',
                                                             'norm_doc': 'М 04-58-2009',
                                                             'conformity_main': True},
                 '1 Массовая доля бензойной кислоты, мг/кг': {'result': '<1,0*', 'norm': '-',
                                                              'norm_doc': 'М 04-58-2009',
                                                              'conformity_main': False}}, {
                    '- свинец': {'result': '0,058±0,021', 'norm': 'не более 0,35',
                                 'norm_doc': 'М-02-1702-20', 'conformity_main': True,
                                 'conformity_deviation': True},
                    '- мышьяк': {'result': '<0,01*', 'norm': 'не более 0,15',
                                 'norm_doc': 'М-02-1702-20', 'conformity_main': True},
                    '- кадмий': {'result': '< 0,005*', 'norm': 'не более 0,07',
                                 'norm_doc': 'М-02-1702-20', 'conformity_main': True},
                    '• ртуть': {'result': '< 0,002*', 'norm': 'не более 0,015',
                                'norm_doc': 'ГОСТ Р 53183-2008', 'conformity_main': True},
                    '- ГХЦГ (а, 0, у - изомеры)': {'result': '<0,01*',
                                                   'norm': 'не более 0,5',
                                                   'norm_doc': 'ГОСТ 32689.3-2014',
                                                   'conformity_main': True},
                    '- ДДТ и его метаболиты': {'result': '<0,01*', 'norm': 'не более 0,02',
                                               'norm_doc': 'ГОСТ 32689.3-2014',
                                               'conformity_main': True},
                    '-гексахлорбензол': {'result': '<0,01*', 'norm': 'не более 0,01',
                                         'norm_doc': 'ГОСТ 32689.3-2014',
                                         'conformity_main': True},
                    '- ртутьорганические': {'result': '<0,01*', 'norm': 'не допускаются',
                                            'norm_doc': 'СТ РК 2040-2010',
                                            'conformity_main': True},
                    '- 2,4-Д кислота, ее соли, эфиры': {'result': '<0,02*',
                                                        'norm': 'не допускаются',
                                                        'norm_doc': 'МУ 1541-76',
                                                        'conformity_main': False}}, {
                    'Общее количество мезофильных аэробных и факультативно-анаэробных бактерий (КМАФАнМ), КОЕ/г': {
                        'result': '5,1х10²', 'norm': 'не более 1,0x10³',
                        'norm_doc': 'МУК 4.2.2578-2010', 'conformity_main': True},
                    'Колиформные бактерии': {'result': 'не обнаружено в 1.0 г',
                                             'norm': 'не допускаются в 1,0 г',
                                             'norm_doc': 'ГОСТ 31747-2012',
                                             'conformity_main': True},
                    'S. aureus': {'result': 'не обнаружено в 1,0 г',
                                  'norm': 'не допускаются в 1,0 г',
                                  'norm_doc': 'ГОСТ 31746-2012', 'conformity_main': True},
                    'Бактерии рода Proteus': {'result': 'нс обнаружено в 0,1 г',
                                              'norm': 'не допускаются в 0,1 г',
                                              'norm_doc': 'ГОСТ 28560-90',
                                              'conformity_main': True},
                    'Бактерии рода Salmonella': {'result': 'не обнаружено в 25 г',
                                                 'norm': 'не допускаются в 25 г',
                                                 'norm_doc': 'ГОСТ 31659-2012',
                                                 'conformity_main': True},
                    'Плесневые грибы, КОЕ/г': {'result': 'Менее 1,0x10’',
                                               'norm': 'не более 50',
                                               'norm_doc': 'ГОСТ 10444.12-2013',
                                               'conformity_main': True}}],
            'Группа продукции': 'Производство магазина'},
        (7, 'air'): {'Шифр пробы': '8281 -2', 'Объект исследования': 'Воздух (микробная обсемененность)',
                     'Условия доставки': 'Автотранспорт, сумка-холодильник', 'Температура при доставке проб': '+з°с',
                     'Нарушения при доставке проб': 'Упаковка не нарушена',
                     'Цель исследований': 'Производственный контроль',
                     'Дата проведения исследований': '13.08.2024 г.- 18.08.2024 г.', 'indicators': [{
                'Холодильная камера «Молочные продукты»': {
                    'name': 'Плесневые грибы, КОЕ',
                    'sampling_site': 'Холодильная камера «Молочные продукты»',
                    'result': '0',
                    'norm': '',
                    'norm_doc': 'Методические рекомендации по определению зараженности '
                                'плесневыми грибами холодильных камер (с дополнениями)',
                    'conformity_main': True}}]},
        (9, 'washings'): {
            'Шифр пробы': '8281 -3', 'Объект исследований': 'Смывы',
            'Условия доставки': 'Автотранспорт, сумка-холодильник',
            'Температура при доставке проб': '+3°С',
            'Нарушения при доставке проб': 'Упаковка не нарушена',
            'Цель исследований': 'Производственный контроль',
            'Дата проведения исследований': '13.08.2024 г.-19.08.2024 г.', 'indicators': [{'БГКП': {
                'result': 'не обнаружено', 'norm': '', 'norm_doc_of_method': 'МР 4.2.0220-20',
                'sampling_site': 'Касса',
                'conformity_main': True},
                'БГКП_0': {'result': 'не обнаружено', 'norm': '-',
                           'norm_doc_of_method': 'МР 4.2.0220-20',
                           'sampling_site': 'Стеллаж «Хлеб»', 'conformity_main': True},
                'БГКП_1': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'МР 4.2.0220-20',
                    'sampling_site': 'Стеллаж «Кондитерские изделия»',
                    'conformity_main': True},
                'Бактерии рода Salmonella': {
                    'result': 'нс обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'МУ 4.2.2723-10, п.10',
                    'sampling_site': 'Холодильник «Сыры»',
                    'conformity_main': True},
                'Бактерии вида L. monocytogenes': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'ГОСТ 32031',
                    'sampling_site': 'Холодильник «Сыры»',
                    'conformity_main': True},
                'Бактерии рода Salmonella_0': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'МУ 4.2.2723-10, п.10',
                    'sampling_site': 'Холодильник «Колбаса»',
                    'conformity_main': True},
                'Бактерии вида L. monocytogenes_0': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'ГОСТ 32031',
                    'sampling_site': 'Холодильник «Колбаса»',
                    'conformity_main': True},
                'Бактерии рода Salmonella_1': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'МУ 4.2.2723-10, п. 10',
                    'sampling_site': 'Холодильник «Мясо»',
                    'conformity_main': True},
                'Бактерии вида L. monocytogenes_1': {
                    'result': 'не обнаружено',
                    'norm': '-',
                    'norm_doc_of_method': 'ГОСТ 32031',
                    'sampling_site': 'Холодильник «Мясо»',
                    'conformity_main': True}}],
            'Объект исследования': 'Смывы'},
        (12, 'PROD_CONTROL'): {
            'number_of_protocol': '8303/24-Д', 'date_of_protocol': '23 августа 2024',
            'act': '8303 ОТ 13.08.2024',
            'place_of_measurement': 'г. Калуга, ул. Ленина, д. 58, магазин № 40515',
            'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                                'уровни освещенности рабочей поверхности, '
                                'шума и общей вибрации соответствуют требованиям',
            'indicators': [{'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)': {
                'name': 'Температура воздуха 0,1м', 'unit': '°C', 'result': '20,3±0,6',
                'norm': '18-27',
                'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                'conformity_main': True, 'conformity_deviation': True},
                'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)_0': {
                    'name': 'Температура воздуха 1,5м', 'unit': '°C',
                    'result': '20,4±0,6', 'norm': '18-27',
                    'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)_1': {
                    'name': 'Скорость движения воздуха 0,1м', 'unit': 'м/сек',
                    'result': '0,10±0,06', 'norm': '0,4, не более',
                    'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)_2': {
                    'name': 'Скорость движения воздуха 1,5м', 'unit': 'м/сек',
                    'result': '0,10±0,06', 'norm': '0,4, не более',
                    'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)_3': {
                    'name': 'Относительная влажность воздуха Относительная влажность воздуха',
                    'unit': '%', 'result': '41,1±5,8', 'norm': '15-75',
                    'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)_4': {
                    'name': 'Освещенность рабочей поверхности (общ.) Освещенность рабочей поверхности (общ.)',
                    'unit': 'лк', 'result': '650,0±60,0', 'norm': '300, не менее',
                    'sampling_site': 'Отдел«Овощи/ фрукты», рабочее место работника торгового зала(Па)',
                    'conformity_main': False, 'conformity_deviation': False},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)': {
                    'name': 'Температура воздуха 0,1м', 'unit': '°C',
                    'result': '20,1±0,6', 'norm': '18-27',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)_0': {
                    'name': 'Температура воздуха 1,5м', 'unit': '°C',
                    'result': '20,2±0,6', 'norm': '18-27',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)_1': {
                    'name': 'Скорость движения воздуха 0,1м', 'unit': 'м/сек',
                    'result': '0,10±0,0б', 'norm': '0,4, не более',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': False},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)_2': {
                    'name': 'Скорость движения воздуха 1,5м', 'unit': 'м/сек',
                    'result': '0,10±0,06', 'norm': '0,4, не более',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)_3': {
                    'name': 'Относительная влажность воздуха Относительная влажность воздуха',
                    'unit': '%', 'result': '41,3±5,8', 'norm': '15-75',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': True, 'conformity_deviation': True},
                'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)_4': {
                    'name': 'Освещенность рабочей поверхности (общ.) Освещенность рабочей поверхности (общ.)',
                    'unit': 'лк', 'result': '650,0±60,0', 'norm': '300, не менее',
                    'sampling_site': 'Отдел «Хлебобулочные изделия», рабочее место работника торгового зала(Па)',
                    'conformity_main': False, 'conformity_deviation': False},
                'Торговый зал у холодильной витрины с молочной продукцией': {
                    'name': 'Шум Шум', 'unit': 'ДБА', 'result': '42,0±0,8', 'norm': '60',
                    'sampling_site': 'Торговый зал у холодильной витрины с молочной продукцией',
                    'conformity_main': True, 'conformity_deviation': True},
                'Торговый зал у холодильной витрины с молочной продукцией_0': {
                    'name': 'Вибрация общая Хо', 'unit': 'ДБ', 'result': 'менее 70**',
                    'norm': '80',
                    'sampling_site': 'Торговый зал у холодильной витрины с молочной продукцией',
                    'conformity_main': True},
                'Торговый зал у холодильной витрины с молочной продукцией_1': {
                    'name': 'Вибрация общая Yo', 'unit': 'ДБ', 'result': 'менее 70',
                    'norm': '80',
                    'sampling_site': 'Торговый зал у холодильной витрины с молочной продукцией',
                    'conformity_main': True},
                'Торговый зал у холодильной витрины с молочной продукцией_2': {
                    'name': 'Вибрация общая Zo', 'unit': 'ДБ', 'result': 'менее 70',
                    'norm': '80',
                    'sampling_site': 'Торговый зал у холодильной витрины с молочной продукцией',
                    'conformity_main': True}}]}}
    return main_collector