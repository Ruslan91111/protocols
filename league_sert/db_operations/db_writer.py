"""
Код для записи данных в БД.


"""
import sys
import time
import os
import multiprocessing
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.db_config_postgres import PROTOCOLS_DB
from league_sert.data_preparation.launch_data_preparation import extract_and_prepare_data
from league_sert.exceptions import DirDontExistError
from league_sert.models.models import MainProtocol
from league_sert.models.models_creator import ObjectsForDB, create_all_objects
from league_sert.constants import RECORDED_FILE
from league_sert.db_operations.file_utils import read_viewed_from_file, move_unrecorded_files


global_process_engine = None
global_process_session = None


def init_process(db_url: str):
    """Инициализация соединения для каждого процесса"""

    global global_process_engine, global_process_session
    global_process_engine = create_engine(db_url)
    global_process_session = sessionmaker(bind=global_process_engine)


def _write_objects_from_file_to_db(objects: ObjectsForDB, session_maker):
    """Записать объекты, сформированные из одного word файла в БД."""

    session = session_maker()

    try:
        main_object = None
        # Сначала находим и обрабатываем главный объект
        for key, value in objects.items():
            if key[1] == 'MAIN':
                main_object = value
                existing_main = session.query(MainProtocol).filter_by(
                    number=main_object.number).first()
                if not existing_main:
                    session.add(main_object)
                else:
                    main_object = existing_main  # Используем существующий объект
                break
        session.commit()

        # Затем обрабатываем остальные объекты, связывая их с главным
        for key, value in objects.items():
            if key[1] != 'MAIN':
                for obj in value:
                    # Устанавливаем связь с основными данными.
                    obj.main_prot = main_object
                    session.add(obj)
        session.commit()

    # Обработка исключения, протокол уже есть в БД.
    except IntegrityError as e:
        session.rollback()
        print('УЖЕ ЕСТЬ В БД.', e)
        raise

    # Отлавливаем иные исключения.
    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка при записи в БД: {e}")
        raise


def process_and_write_file_task(file, word_dir):
    """Задача для отдельного процесса по обработке файла
    и записи данных из него в БД."""

    try:
        # Используем глобальные объекты процесса
        session = global_process_session()
        data = extract_and_prepare_data(os.path.join(word_dir, file))
        objects = create_all_objects(data)
        _write_objects_from_file_to_db(objects, global_process_session)
        session.close()
        return file, None
    except Exception as e:
        return None, file


def write_files_to_db_from_dir(dir_path, db_url, num_processes=4):
    """Обработать и записать в БД все файлы, находящиеся в передаваемой директории,
    используя многопроцессорность."""

    # Директория с ПДФ файлами не существует
    if not os.path.isdir(dir_path):
        raise DirDontExistError(dir_path)

    # В директории с ПДФ отсутствует директория с word файлами.
    word_dir = os.path.join(dir_path, 'word_files')
    if not os.path.isdir(word_dir):
        raise DirDontExistError(word_dir)

    not_recorded = []  # Файлы, незаписанные в БД.
    recorded = read_viewed_from_file(RECORDED_FILE)  # Файлы, уже записанные в БД.

    # Файлы для обработки.
    files_to_process = [
        f for f in os.listdir(word_dir) if
        not ('$' in f or f in recorded or os.path.isdir(os.path.join(word_dir, f)))
    ]

    try:
        with multiprocessing.Pool(
                processes=num_processes,
                initializer=init_process,
                initargs=(db_url,)
        ) as pool:
            results = []

            for file in files_to_process:
                results.append(
                    pool.apply_async(
                        process_and_write_file_task,
                        (file, word_dir)
                    )
                )

            recorded = set()
            not_recorded = []
            for res in results:
                try:
                    recorded_file, not_recorded_file = res.get(timeout=30)
                    if recorded_file:
                        recorded.add(recorded_file)
                    if not_recorded_file:
                        not_recorded.append(not_recorded_file)
                except Exception as e:
                    print(f"Ошибка в процессе: {e}")
                    not_recorded.append("unknown_file")

    except Exception as e:
        print(e)

    # Обновить файл с записанными файлами.
    with open(RECORDED_FILE, 'w', encoding='utf-8') as word_file:
        word_file.write(",".join(recorded))

    print(f'В Базу Данных записано {len(recorded)} файлов.')
    print(f'Не записано {len(not_recorded)} файлов. '
          f'Файлы перемещены в директорию {os.path.join(word_dir, "unrecorded")}')


examp_path1 = (r'C:\Users\RIMinullin\Desktop\ППК 2025 — большие переименованные')
examp_path2 = (r'C:\Users\RIMinullin\Desktop\август-октябрь все')
# examp_path2 = (r'C:\Users\RIMinullin\Desktop\2024')

if __name__ == '__main__':

    # x = (examp_path1 + '\\' +'word_files\\50331 07.10.2024.docx')
    try:
        start = time.time()
        write_files_to_db_from_dir(examp_path1, PROTOCOLS_DB)
        write_files_to_db_from_dir(examp_path2, PROTOCOLS_DB)

        print(time.time() - start)

    except Exception as e:

        print(e)
        print(time.time() - start)
