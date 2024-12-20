"""
Модуль содержит функцию запуска всего кода пакета data_preparation

Пример использования:
    prepared_data_from_file = extract_and_prepare_data(path_to_word_file)

"""
import sys
from pathlib import Path

from league_sert.data_preparation.process_tables import process_the_tables

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from league_sert.data_preparation.add_conclusions import add_conclusions_for_all_tables
from league_sert.data_preparation.file_parser import MainCollector
from league_sert.data_preparation.merge_tables import refine_and_merge_tables


def extract_and_prepare_data(word_file: str):
    """Запуск кода модуля по изъятию и подготовке данных для записи в БД."""

    # Создаем объект собирателя данных из word файла.
    data_collector = MainCollector(word_file)

    # Собираем все данные из word документа.
    data_collector.collect_all_data()

    # Обработка данных из таблиц word файла.
    data_collector.data_from_tables = process_the_tables(
        data_collector.data_from_tables)

    # Добавляем выводы о соответствии результатов исследований нормам.
    data_collector.data_from_tables = add_conclusions_for_all_tables(
        data_collector.data_from_tables)

    # Объединяем таблицы описаний проб и таблицы результатов исследований.
    data_collector.data_from_tables = refine_and_merge_tables(data_collector.data_from_tables)

    # Объединяем данные по производственному контролю.
    data_collector.merge_prod_control()
    return data_collector
