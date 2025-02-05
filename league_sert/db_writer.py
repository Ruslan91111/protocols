""" Модуль с верхне-уровневым кодом записи данных в БД.

- Функции:
    - write_objects_to_db: записать переданный словарь объектов классов в БД.

    - process_and_write_files_to_db: получить путь к директории, через цикл
    обработать файлы и записать их в БД.

"""
import re
import shutil
import sys
import os
import time

from pathlib import Path

from sqlalchemy.exc import IntegrityError

from database.db_config_postgres import prot_session_maker
from league_sert.data_preparation.launch_data_preparation import extract_and_prepare_data
from league_sert.exceptions import DirDontExistError
from league_sert.models.models import MainProtocol
from league_sert.models.models_creator import ObjectsForDB, create_all_objects

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

VIEWED_FILE = r'viewed.txt'


def _write_objects_from_file_to_db(objects: ObjectsForDB, session_maker):
    """ Записать объекты, сформированные из одного word файла в БД.
    Сначала в БД записывается основной объект, затем он передается
    в дополнительные объекты для оформления внешних ключей. """
    with session_maker() as session:
        try:
            # Перебираем данные из таблиц.
            for key, value in objects.items():
                # Добавление основного объекта (с основным номером и датой протокола) в БД.
                if key[1] == 'MAIN':
                    main_object = value
                    # Проверяем есть ли уже такой главный объект в main_prot БД.
                    existing_main = session.query(MainProtocol).filter_by(
                        number=main_object.number).first()
                    # Если в БД нет такого
                    if not existing_main:
                        session.add(main_object)
                    else:  # Берем его id из БД.
                        main_object = existing_main
                    break
            session.commit()

            # Повторно перебираем данные из таблиц.
            for key, value in objects.items():
                # Добавление остальных объектов в сессию.
                if key[1] != 'MAIN':
                    for obj in value:
                        # Добавляем ссылку на основной объект.
                        obj.main_prot = main_object
                        session.add(obj)
            session.commit()

        # Ошибка в случае, если в БД существует подобный объект.
        except IntegrityError as e:
            session.rollback()
            print(e)
        # except Exception as e:
        #     print(e)


def write_file_to_db(file):
    """ Записать один word файл в БД."""
    # Собрать данные из word файла.
    data_from_file = extract_and_prepare_data(file)
    # Создать из собранных данных объекты для записи в БД.
    objects_for_db = create_all_objects(data_from_file)
    # Записать объекты в БД.
    _write_objects_from_file_to_db(objects_for_db, prot_session_maker)


def read_viewed_from_file(file: str = VIEWED_FILE):
    """Прочитать номера просмотренных документов из файла."""
    if not os.path.isfile(file):
        with open(file, 'w', encoding='utf-8') as file:
            file.write('')
            return set()
    with open(file, 'r', encoding='utf-8') as file:
        viewed_files = set(file.read().split(','))
        return viewed_files


def move_unrecorded_files(word_file, dir_with_word_files):
    """ Переместить файл, который не удалось записать в DB
    в отельную директорию. """

    unrecorded_word_dir = Path(dir_with_word_files) / 'unrecorded'
    unrecorded_word_dir.mkdir(parents=True, exist_ok=True)

    # Перемещаем word файл.
    original_word_path = Path(dir_with_word_files) / word_file
    destination_word_path = Path(unrecorded_word_dir) / word_file
    shutil.move(original_word_path, destination_word_path)

    # Перемещаем pdf файл.
    pdf_file = word_file.replace('.docx', '.pdf')
    pdf_path = Path(dir_with_word_files).parent
    unrecorded_pdf_path = Path(pdf_path) / 'unrecorded'
    unrecorded_pdf_path.mkdir(parents=True, exist_ok=True)
    original_pdf_path = Path(pdf_path) / pdf_file
    destination_pdf_path = Path(unrecorded_pdf_path) / pdf_file
    shutil.move(original_pdf_path, destination_pdf_path)


def move_recorded_from_unrecorded(word_file, unrecorded_word_files):
    """ Переместить файл, который не удалось записать в DB
    в отельную директорию. """
    # Перемещаем word файл.
    original_word_path = Path(unrecorded_word_files) / word_file
    destination_word_path = Path(unrecorded_word_files).parent / word_file
    shutil.move(original_word_path, destination_word_path)

    # Перемещаем pdf файл.
    pdf_file = word_file.replace('.docx', '.pdf')

    pdf_path = Path(unrecorded_word_files).parent.parent
    unrecorded_pdf_path = Path(pdf_path) / 'unrecorded'
    original_pdf_path = Path(unrecorded_pdf_path) / pdf_file
    destination_pdf_path = Path(unrecorded_pdf_path).parent / pdf_file
    shutil.move(original_pdf_path, destination_pdf_path)


def write_files_to_db_from_dir(dir_path):
    """ Обработать и записать в БД все файлы,
    находящиеся в передаваемой директории """

    if not os.path.isdir(dir_path):
        raise DirDontExistError(dir_path)

    word_dir_path = dir_path + '\\' 'word_files'
    not_recorded = []  # Файлы, незаписанные в БД.
    recorded = read_viewed_from_file(VIEWED_FILE)  # Файлы, уже записанные в БД.

    # Перебираем файлы.
    for word_file in os.listdir(word_dir_path):
        # Пропускаем временные, не скачанные файлы, уже записанные в БД, директории.
        if ('$' in word_file or
                word_file in recorded or
                os.path.isdir(word_dir_path + '\\' + word_file)):
            continue

        try:
            # Получить и подготовить данные из word файла в виде словаря.
            data_from_file = extract_and_prepare_data(word_dir_path + '\\' + word_file)
            # Создать объекты моделей для записи в БД.
            objects_for_db = create_all_objects(data_from_file)
            # Записать объекты в БД.
            _write_objects_from_file_to_db(objects_for_db, prot_session_maker)
            # Добавить файл в перечень записанных файлов.
            recorded.add(word_file)

        # В случае ошибки переместить word и pdf файл в директорию не записанных.
        except Exception as e:
            not_recorded.append(word_file)
            move_unrecorded_files(word_file, word_dir_path)

            with open(VIEWED_FILE, 'w', encoding='utf-8') as word_file:
                word_file.write(",".join(recorded))

    print(f'В Базу Данных записано {len(recorded)} файлов.')
    print(f'Не записано {len(not_recorded)} файлов. '
          f'Файлы перемещены в директорию {word_dir_path}\\unrecorded')


def write_files_to_db_from_dir_debug(dir_path):
    """ Обработать и записать в БД все файлы,
    находящиеся в передаваемой директории """
    # Записанные в БД файлы.
    recorded = read_viewed_from_file(VIEWED_FILE)  # Файлы, уже записанные в БД.
    # Директория с файлами не записанными в БД.
    unrecorded_word_dir = Path(dir_path, 'word_files', 'unrecorded')
    # Перебираем файлы.
    for file in os.listdir(unrecorded_word_dir):
        # Пропускаем временные и директории
        if '$' in file or os.path.isdir(Path(unrecorded_word_dir, file)):
            continue
        print(file)
        for _ in range(3):
            # try:
                # Получить и подготовить данные из word файла
            data_from_file = extract_and_prepare_data(Path(unrecorded_word_dir, file))
            # Создать объекты для записи в БД.
            objects_for_db = create_all_objects(data_from_file)
            # Записать объекты в БД.
            _write_objects_from_file_to_db(objects_for_db, prot_session_maker)
            # Добавить в записанный
            recorded.add(file)
            break

        move_recorded_from_unrecorded(file, unrecorded_word_dir)
            # except Exception as e:
            #     print(e.message)

    with open(VIEWED_FILE, 'w', encoding='utf-8') as file:
        file.write(",".join(recorded))




examp_path1 = (r'C:\Users\RIMinullin\Desktop\август-октябрь все')

examp_path2 = (r'C:\Users\RIMinullin\Desktop\2024')

if __name__ == '__main__':

    # x = extract_and_prepare_data(examp_path1 + '\\' +'word_files\\32006 08.08.2024.docx')

    start = time.time()
    # write_files_to_db_from_dir_debug(examp_path1)
    write_files_to_db_from_dir(examp_path1)
    # write_files_to_db_from_dir(examp_path2)

    write_files_to_db_from_dir_debug(examp_path1)


    # write_file_to_db(r'C:\Users\RIMinullin\PycharmProjects\protocols\tests\test_league_sert\test_files\test_word_file_1.docx')
    # write_file_to_db(r'C:\Users\RIMinullin\PycharmProjects\protocols\tests\test_league_sert\test_files\test_word_file_2.docx')
    # write_file_to_db(r'C:\Users\RIMinullin\PycharmProjects\protocols\tests\test_league_sert\test_files\test_word_file_3.docx')
    print(time.time() - start)
