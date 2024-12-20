"""
Переименовать файлы в директории, передать путь к директории с ПДФ файлами,
далее код проверяет наличие в директории с конвертированными файлами word,
затем перебирает через цикл word файлы, открывает и читает их, находит внутри
код магазина и дату протокола, из чего составляет новое наименование и
заменяет на него старое наименование, как для PDF, так и для word файла.

Пример использования:
    rename_the_files_in_dir(путь к директории с ПДФ файлами и директорией с
                            конвертированными word файлами)
"""
import os
import random
import re

from docx import Document

from conversion.exceptions import DataNotFounError
from league_sert.constants import MONTHS, CODE_PATTERN
from conversion.convert_files_in_dir import WordChecker


def check_word_files_dir(path_to_dir: str) -> str:
    """ Вернуть или создать директорию. """
    if os.path.isdir(path_to_dir):
        return path_to_dir
    raise Exception('Внутри нет папки с word файлами.')


def check_name_word_file(file_name: str) -> bool:
    """ Проверить переименован ли word файл в соответствии с паттерном. """
    pattern_renamed = r'\d+\s\d{2}\.\d{2}\.\d{4}(_\d{,2})?\.docx'
    return bool(re.search(pattern_renamed, file_name))


def get_main_date(file_path: str) -> str | bool:
    """ Вернуть дату протокола. """
    word_checker = WordChecker(file_path)
    try:
        word_checker.get_main_numb_and_date()
    except Exception:
        re.search(r'гарантийное письмо', word_checker.text, re.IGNORECASE)
        return 'guarantee'
    if word_checker.main_date:
        return word_checker.main_date
    return False


def search_code(text: str) -> str:
    """ Ищем код магазина в переданном тексте. """

    # На случай наличия в адресе наименования воинской части.
    army = re.search('в/ч', text)
    if army:
        # Если в строке есть наименование воинской части, то ищем код в тексте вне ВЧ
        match = re.search(r'\b\d{5}\b', text[:army.start()] + text[army.end()+5:])
        if match:
            result = match.group()
            if result != '31112':
                return result

    # Если в наименовании нет указаний на воинскую часть.
    else:
        match = re.search(CODE_PATTERN, text)
        if match:
            result = match.group(1) if match.group(1) else match.group(2)
            if result != '31112':
                return result


def get_store_code(file_path: str) -> str | None:
    """ Получить из документа код магазина. """

    document = Document(file_path)  # Преобразуем документ
    all_tables_in_file = document.tables  # Собираем таблицы.

    # Итерируемся по таблицам.
    for table_ in all_tables_in_file:

        # Считаем и проверяем количество колонок в таблице.
        cols_count = len(table_.columns)
        if len(table_.rows) <= 1 or cols_count <= 1:
            continue

        # Итерируемся по строкам в таблице.
        for row in table_.rows:
            cells = row.cells  # Ячейки строки
            cell_text = cells[1].text.strip()  # Текст из второй колонки.

            # Ищем код магазина
            result = search_code(cell_text)
            if result:
                return result


            # # Ищем код магазина
            # match = re.search(CODE_PATTERN, cell_text)
            # if match:
            #     result = match.group(1) if match.group(1) else match.group(2)
            #     if result != '31112':
            #         return result


def rename_a_file(dir_: str, old_name: str, new_name: str, extension: str) -> None:
    """
    Переименовать один файл в директории по определенному паттерну.

    :param dir_: Директория с файлами
    :param old_name: старое название файла
    :param new_name: новое название файла
    :param extension: расширение файла
    :return: None
    """
    path_new_name = dir_ + '\\' + new_name + extension
    path_old_name = dir_ + '\\' + old_name

    # Если файл с новым наименованием уже существует в директории,
    # то добавляем цифру в наименование.
    if os.path.isfile(path_new_name):
        done = False
        i = 1
        while not done:
            path_new_name = dir_ + '\\' + new_name + '_' + str(i) + extension
            if os.path.isfile(path_new_name):
                i += 1
                continue
            done = True

    # Переименовываем файл.
    os.rename(path_old_name, path_new_name)


def process_date(date: str) -> str:
    """ Обработать дату. """
    # Заменить ошибочное слово.
    if 'толя' in date:
        date = re.sub('толя', 'июля', date)

    # Убрать пробел в годе.
    date = re.sub(r'(\d{2})\s(\d{2})', r'\1\2', date)

    # Заменить месяц на числовой формат
    date_ = date.split(' ')
    date_[1] = MONTHS[date_[1]]

    proc_date = ".".join(date_)  # Собрать дату в строку
    return proc_date


def rename_the_files_in_dir(dir_with_pdf_files: str) -> None:
    """
    Переименовать файлы в определенной директории.
    :param dir_with_pdf_files:
    :return: None
    """

    dir_for_word_files = check_word_files_dir(dir_with_pdf_files + '\\word_files\\')
    word_files = os.listdir(dir_for_word_files)  # Список word файлов.

    # Цикл по word файлам.
    for word_file in word_files:
        print(word_file)

        # Проверка, что файл еще не переименованный.
        if check_name_word_file(word_file):
            continue

        # Если файл не переименованный.
        pdf_file = word_file.replace('.docx', '.pdf')  # Старый pdf файл.
        path_word_file = dir_for_word_files + '\\' + word_file

        # Получить из файла код магазина.
        store_code = get_store_code(path_word_file)

        # Получить дату протокола.
        date = get_main_date(path_word_file)

        # Проверка, что дата протокола найдена.
        if isinstance(date, bool):
            raise DataNotFounError(path_word_file)

        # Проверка, что не гарантийное письмо.
        if date == 'guarantee':
            new_name = 'Гарантийное письмо' + str(random.randint(1, 1000))

        else:
            # Обработать дату.
            date = process_date(date)
            new_name = store_code + ' ' + date

        rename_a_file(dir_with_pdf_files, pdf_file, new_name, '.pdf')
        rename_a_file(dir_for_word_files, word_file, new_name, '.docx')

    print('Все файлы успешно переименованы.')


if __name__ == '__main__':
    rename_the_files_in_dir(r'C:\Users\RIMinullin\Desktop\не конвертирует\pdf')
