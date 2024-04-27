"""
Модуль с функциями для изъятия сбора необходимых данных из word документа.

get_text_from_word_file: прочитать текст из word файла с помощью библиотеки docx2txt
get_number_and_date_protocol: найти в файле номер и дату протокола
get_all_items_from_tables_in_word_file: собрать все данные из таблиц в word в один словарь
get_required_items_from_tables_in_word_file: в word файле собрать словарь
    по необходимым ключам, внутри используется функция get_all_items_from_tables_in_word_file
    и из возвращаемого данной функцией словаря выбираются нужные ключи
get_indicators_from_word_file: собрать в список словарей показатели из протокола
get_all_data_from_word_file: общая функция собирает все необходимые данные из протокола,
    внутри использует предыдущие функции, возвращает результат в виде словаря
apply_function_through_for: функция, которая принимает директорию с word файлами и функцию
    и через цикл for применяет функцию к файлами, результаты выводит через print

"""
import json
import os
import re

from docx import Document
import docx2txt


FILE_0 = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\новый\\scan300.docx'
FILE_1 = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\32002 19.09.2023.docx'
FILE_2 = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\33203 20.09.2023.docx'
FILE_3 = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\32008 27.04.2023_продукция_Рыбная.docx'
DIR_WITH_WORD = r'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\'


# Ключи для поиска на первой странице протокола.
REQUIRED_KEYS_FOR_FIRST_PAGE = (
    'Место отбора проб',
    'Дата и время отбора проб',
    'Сопроводительные документы',
    'Группа продукции',
    'Наименование продукции',
    'Дата производства продукции',
    'Производитель (фирма, предприятие, организация)',
    'Дата проведения исследований'
)


def get_text_from_word_file(input_file: str) -> str:
    """ Прочитать word файл, вернуть строку, для поиска номера и даты протокола. """
    text = docx2txt.process(input_file)
    return text


def get_number_and_date_protocol(word_file: str) -> tuple[str, str]:
    """ Вернуть номер и дату из протокола испытания """
    # Получаем текст из Word файла.
    text = get_text_from_word_file(word_file)
    # Ищем начало номера и даты протокола.
    index_start_protocol = text.find('Протокол исп')
    # Ищем конец наименования и даты протокола
    index_end_protocol = index_start_protocol + text[index_start_protocol:].find('.')
    # Подстрока с номером и датой протокола.
    name_and_date_of_protocol = text[index_start_protocol:index_end_protocol]
    # Паттерн для поиска номера протокола.
    number_pattern = r'№\s(\d+)\s*\/\d+-Д'
    # Ищем номер протокола по паттерну.
    number_protocol = re.search(number_pattern, name_and_date_of_protocol)

    # Проверяем найден ли номер протокола по шаблону, если нет,
    # то возвращаем строки "Не найдено" и дату не ищем, если найден номер, то ищем дату.
    if number_protocol:
        # Индекс для старта поиска даты протокола
        index_start_date = number_protocol.end()
        # Подстрока, в которой содержится дата протокола.
        text_with_date = name_and_date_of_protocol[index_start_date:].replace('\n', '')
        # Индексы, по которым располагаются цифры.
        indexes_of_digits_in_date = []
        # Наполняем индексы цифр
        for index, symbol in enumerate(text_with_date):
            if symbol.isdigit():
                indexes_of_digits_in_date.append(index)

        # Проверяем, что цифры в строке найдены.
        if indexes_of_digits_in_date:
            # Вырезаем подстроку, начинающуюся и заканчивающуюся цифрами.
            text = text_with_date[indexes_of_digits_in_date[0]:indexes_of_digits_in_date[-1]+1]
            # Преобразуем ее.
            text = text.replace('»', '').replace('\t', '').replace(' ', '')
            # Новая строка для даты протокола.
            date_of_protocol = ''

            # Перебираем символы, добавляем в новую строку, между месяцем и датой добавляем пробел.
            for i in range(len(text) - 1):
                if text[i].isalpha() and text[i-1].isdigit():
                    date_of_protocol += (' ' + text[i])
                elif text[i].isalpha() and text[i + 1].isdigit():
                    date_of_protocol += (text[i] + ' ')
                else:
                    date_of_protocol += text[i]
            date_of_protocol += text[-1]
            number_protocol = number_protocol.group().replace(' ', '').replace('\t', '')

            # Возвращаем номер и дату протокола.
            return number_protocol, date_of_protocol
    # Если строка, совпадающая по паттерну не найдена.
    return 'Номер протокола не найден', 'Дата протокола не найдена'


def get_all_items_from_tables_in_word_file(document: Document) -> dict:
    """ Собрать в словарь, все данные из таблиц word файла. """
    all_tables: list = document.tables
    # Создаем пустой словарь под данные из таблиц, находящихся в WORD файле.
    # Количество ключей соответствует количеству таблиц в WORD файле.
    data_from_tables: dict = {table: None for table in range(len(all_tables))}

    # Идем циклом по всем таблицам из Word файла.
    for number_of_table, table in enumerate(all_tables):
        # В словаре номеру таблицы создаем список списков для заполнения строками.
        data_from_tables[number_of_table] = [[] for _ in range(len(table.rows))]
        # Проходимся по строкам одной таблицы из WORD файла.
        for number_of_row, row in enumerate(table.rows):
            # Проходимся по ячейкам строки таблицы
            for cell in row.cells:
                # Добавляем значение ячейки в соответствующий
                # список, созданного словаря под данные таблиц
                data_from_tables[number_of_table][number_of_row].append(cell.text)

    # Итоговый словарь.
    result_dict = {}
    # Наполняем итоговый словарь данными из таблиц, исходим из структуры в виде двух колонок.
    for item in data_from_tables:
        result_dict.update({i[0]: i[1] for i in data_from_tables[item]})

    return result_dict


def get_required_items_from_tables_in_word_file(
        document: Document,
        required_keys: tuple = REQUIRED_KEYS_FOR_FIRST_PAGE) -> dict:
    """
    В словаре, собранного из word документа оставить только нужные ключи.
    Из word документа сюда не войдет номер и дата протокола, а также
    показатели.
    """

    def find_code_of_store(data: dict) -> dict:
        """ Подфункция - найти код магазина - место отбора проб. """
        pattern_for_code = r'\d{5}'
        code = re.search(pattern_for_code, data['Место отбора проб'])
        data['Место отбора проб'] = code.group()
        return data

    # Общий словарь со всеми данными из таблиц word файла.
    dict_from_word = get_all_items_from_tables_in_word_file(document)
    result_dict = {}
    # Перебираем пары в словаре данных, полученных из таблиц word файла и если ключ есть
    # в перечне нужных, то добавляем в словарь - результат.
    for item in dict_from_word.items():
        if item[0] in set(required_keys):
            result_dict[item[0]] = item[1]
    result_dict = find_code_of_store(result_dict)
    return result_dict


def get_indicators_from_word_file(document: Document) -> list[dict[str: list]]:
    """
    Получить показатели из протокола.

    На вход получает word файл, в котором ищет таблицы, в которых первые
    две ячейки в первой строке это "Наименование показателя" и "Результат".
    Если такие таблицы найдены, то значения из них сохраняются в словарь.
    Если таких таблиц несколько, то словари объединяются в список.

    :param word_file:
    :return:
    """
    # Выбираем таблицы из документа.
    all_tables = document.tables
    result_list = []
    # Перебираем таблицы из word файла.
    for table in all_tables:
        # Проверяем, что в таблице есть хотя бы две строки.
        if len(table.rows) > 1:
            # Получаем ячейки первой строки
            first_row = table.row_cells(0)
            # Проверяем, что значения в первой строке отвечают необходимым критериям.
            if (len(first_row) > 1 and first_row[0].text == "Наименование показателя" and
                    first_row[1].text == "Результат"):
                # Данные из таблицы, отвечающей критериям.
                table_data = {}
                # Итерируемся по строкам, начиная со второй
                for _, row in enumerate(table.rows[1:], start=1):
                    cells = row.cells
                    indicator_name = cells[0].text.strip()  # Имя показателя
                    results = cells[1].text.strip()  # Результаты
                    requirements = cells[2].text.strip()  # Требования НД
                    # Сохраняем пару ключ - значение в результате.
                    table_data[indicator_name] = (results, requirements)
                # Добавляем в выходной список.
                result_list.append(table_data)
    return result_list


def get_all_data_from_word_file(word_file: str) -> dict:
    """ Функция объединяет в себе три функции по поиску данных в word файле,
    формируя результат в виде словаря."""

    data_from_protocol = {}
    # Добавить номер и дату протокола.
    data_from_protocol['Номер протокола'], data_from_protocol['Дата протокола'] = (
        get_number_and_date_protocol(word_file))
    # Создаем объект класса для работы с таблицами Word.
    document = Document(word_file)
    # Добавить в словарь все пары с первой таблицы.
    data_from_protocol.update(get_required_items_from_tables_in_word_file(document))
    # Добавить в словарь показатели.
    data_from_protocol['Показатели'] = json.dumps(get_indicators_from_word_file(document))
    return data_from_protocol


def apply_function_through_for(path_to_dir: str, func):
    """
    Применить одну из функций модуля через цикл ко всем документам в директории.
    И наглядно через print посмотреть работу функции.

    :param path_to_dir:
    :param func:
    :return:
    """
    # Множество из имен word файлов в папке.
    word_files = {i for i in os.listdir(path_to_dir) if i[0] != '~' and i[-5:] == '.docx'}
    for file in word_files:
        filename = path_to_dir + file
        if func in {get_number_and_date_protocol, get_all_data_from_word_file}:
            res = func(filename)
        elif func in {get_all_items_from_tables_in_word_file,
                      get_required_items_from_tables_in_word_file,
                      get_indicators_from_word_file}:
            document = Document(filename)
            res = func(document)
        # Вывести то, что возвращает функция.
        print(res)


if __name__ == "__main__":
    apply_function_through_for(DIR_WITH_WORD, get_number_and_date_protocol)
    apply_function_through_for(DIR_WITH_WORD, get_required_items_from_tables_in_word_file)
    apply_function_through_for(DIR_WITH_WORD, get_indicators_from_word_file)
    apply_function_through_for(DIR_WITH_WORD, get_all_data_from_word_file)
