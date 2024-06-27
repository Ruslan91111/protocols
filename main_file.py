import json
import os

import pandas as pd
from sqlalchemy.exc import IntegrityError

from constants import DIR_WITH_WORD, KEYS_FOR_MAPPING_MODEL_PROTOCOL
from get_data_from_word_file import WordFileParser
from return_in_excel import make_one_df_from_protocols
from work_with_tables_in_db import ProtocolManager, engine


class ProtocolToDBWorker:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.protocol_manager = ProtocolManager()

    def get_data_from_word_file(self, word_file: str) -> dict:
        """ Получить словарь данных из word файла. """
        data_from_file = WordFileParser(word_file).get_all_required_data_from_word_file()
        return data_from_file

    def write_protocol_in_db(self, data_for_db):
        """ Записать протокол в БД. """
        self.protocol_manager.add_protocol_to_db(data_for_db)

    def write_protocols_in_dir_to_db(self):
        """ Перебрать word файлы в папке, распарсить каждый файл в словарь,
        записать в БД. """
        word_files = {i for i in os.listdir(self.dir_path) if i[0] != '~' and i[-5:] == '.docx'}
        for file in word_files:
            filename = self.dir_path + '\\' + file
            data_from_word_file = self.get_data_from_word_file(filename)
            try:
                self.write_protocol_in_db(data_from_word_file)
            except Exception as error:
                print(f'При записи данных из файла {file} в БД '
                      f'произошла ошибка {error})')

    def protocols_from_db_to_excel(self):
        all_protocols = self.protocol_manager.get_all_protocols()
        make_one_df_from_protocols(all_protocols, r'protocols_from_db.xlsx')


worker = ProtocolToDBWorker(r'C:\Users\RIMinullin\Desktop\для ворда\в высоком качестве\word_files')
# worker.protocol_manager.delete_all_protocols_from_table()
# worker.write_protocols_in_dir_to_db()
# protocol_manager = ProtocolManager()
# protocols = protocol_manager.get_all_protocols()

worker.protocols_from_db_to_excel()




