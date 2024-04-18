import os
import re
from docx import Document
import pandas as pd
import json
from docx import Document
import docx2txt


doc = Document('C:\\Users\\RIMinullin\\Desktop\\для ворда\\новый\\scan400.docx')
doc2 = Document('C:\\\\Users\\\\RIMinullin\\\\Desktop\\\\для ворда\\\\32008 27.04.2023_продукция_Рыбная.docx')
file = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\новый\\scan300.docx'
s = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\32008 27.04.2023_продукция_Рыбная.docx'
DIR_WITH_WORD = r'C:\\Users\\RIMinullin\\Desktop\\для ворда\\'


def get_str_from_word(input_file: str) -> str:
    """
    Прочитать word файл, вернуть строку

    :param input_file:
    :return:
    """
    text = docx2txt.process(input_file)
    return text


def get_number_and_data_testing_from_file(word_file: str):
    """
    Вернуть номер и дату из протокола испытания

    :param word_file:
    :return:
    """
    # Получаем текст из Word файла.
    text = get_str_from_word(word_file)
    # Ищем начало номера и даты протокола.
    ind_start_name_of_protocol = text.find('Протокол исп')
    # Ищем конец наименования и даты протокола
    ind_end_name_fo_protocol = ind_start_name_of_protocol + text[ind_start_name_of_protocol:].find('.')
    # Подстрока с номером и датой протокола.
    name_and_date_of_protocol = text[ind_start_name_of_protocol:ind_end_name_fo_protocol]
    # Паттерн для поиска номера протокола.
    number_pattern = r'№\s(\d+)\s*\/\d+-Д'
    # Ищем номер протокола.
    number_protocol_search = re.search(number_pattern, name_and_date_of_protocol)
    # Ищем дату
    try:
        # Индекс для старта поиска даты протокола
        index_start_search_date = number_protocol_search.end()
        # Подстрока, в которой содержится дата протокола.
        text_with_date = name_and_date_of_protocol[index_start_search_date:].replace('\n', '')
        # Индекса подстроки, по которым располагаются цифры.
        indexes_of_digit = []
        # Наполняем индексы цифр
        for i in range(len(text_with_date)):
            if text_with_date[i].isdigit():
                indexes_of_digit.append(i)

        # Проверяем, что цифры в строке найдены.
        if indexes_of_digit:
            # Вырезаем подстроку начинающуюся и заканчивающуюся цифрами.
            text = text_with_date[indexes_of_digit[0]:indexes_of_digit[-1]+1]
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

            try:
                return number_protocol_search.group().replace(' ', '').replace('\t', ''), date_of_protocol
            except AttributeError:
                return 'не нашел'
        print('Не найдено цифр')

    except AttributeError:
        print('не найдено')


def get_dict_from_tables(word_file: str) -> dict:
    # Все таблицы из Word документа.
    all_tables: list = word_file.tables

    # Создаем пустой словарь под данные из таблиц, находящихся в WORD файле.
    # Количество ключей соответствует количеству таблиц в WORD файле.
    data_from_tables: dict = {i: None for i in range(len(all_tables))}

    # Идем циклом по всем таблицам из Word файла.
    for i, table in enumerate(all_tables):
        # В словаре номеру таблицы создаем список списков для заполнения строками.
        data_from_tables[i] = [[] for _ in range(len(table.rows))]
        # Проходимся по строкам одной таблицы из WORD файла.
        for j, row in enumerate(table.rows):
            # проходимся по ячейкам таблицы `i` и строки `j`
            for cell in row.cells:
                # добавляем значение ячейки в соответствующий
                # список, созданного словаря под данные таблиц
                data_from_tables[i][j].append(cell.text)

    result_dict = {}
    for item in data_from_tables:
        result_dict.update({i[0]:i[1] for i in data_from_tables[item]})

    return result_dict


required_keys = (
    'Место отбора проб',
    'Дата и время отбора проб',
    'Сопроводительные документы',
    'Группа продукции',
    'Наименование продукции',
    'Дата производства продукции',
    'Производитель (фирма, предприятие, организация)',
    'Дата проведения исследований'
)


def print_required_items_from_dict(word_file):
    dict_from_word = get_dict_from_tables(word_file)
    for i in dict_from_word.items():
        if i[0] in required_keys:
            print(i)


# print(get_number_and_data_testing_from_file(str(doc)))
print_required_items_from_dict(doc)






def do_some(path_to_dir: str):

    word_files = {i for i in os.listdir(path_to_dir) if i[0] != '~' and i[-5:] == '.docx'}
    not_found = []
    found = []
    iterations = 0

    for file in word_files:
        if iterations > 50:
            break
        print('Название файла: ', file)
        iterations += 1
        filename = path_to_dir + file
        res = get_number_and_data_testing_from_file(filename)
        print("Найденный результат", res)



# ЗАПУСК ОДИНОЧНЫХ
# print(get_number_and_data_testing_from_file(str(file)))
# print(get_number_and_data_testing_from_file(str(s)))

# ЗАПУСК В ЦИКЛЕ
# do_some(DIR_WITH_WORD)
# get_number_and_data_testing(str(s))


