"""
Основной файл пакета
 содержит класс ProtocolMainWorker - связующий класс для работы всего пакета protocols.
 Консолидирует в себе работу классов и модулей всего пакета.

     def __init__(self, dir_path):
       :param dir_path - директория с файлами word

"""
import os

from league_sert.convert_files_in_dir import convert_all_pdf_in_dir_to_word
from league_sert.get_data_from_word_file import WordFileParser
from return_in_excel import write_protocols_from_db_in_xlsx_file
from work_with_tables_in_db import ProtocolManager


PATH_TO_XLSX_FILE_WITH_PROTOCOLS = r'../protocols_from_db.xlsx'


class ProtocolMainWorker:
    """ Основной - связующий класс для работы всего пакета protocols.
     Консолидирует в себе работу классов и модулей всего пакета.
     """
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.protocol_manager = ProtocolManager()

    def get_data_from_word_file(self, word_file: str) -> dict:
        """ Получить словарь данных из word файла. """
        data_from_file = WordFileParser(word_file).get_all_required_data_from_word_file()
        return data_from_file

    def write_protocol_in_db(self, data_for_db):
        """ Записать протокол в БД. """
        self.protocol_manager.add_protocol_to_db(data_for_db)

    def conver_pdf_to_words(self):
        """ Получить словарь данных из word файла. """
        convert_all_pdf_in_dir_to_word()

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

    def protocols_from_db_write_to_excel(self, path_to_output_xlsx_file):
        """ Записать все хранящиеся в БД протоколы в xlsx файл."""
        all_protocols = self.protocol_manager.get_all_protocols()
        write_protocols_from_db_in_xlsx_file(all_protocols, path_to_output_xlsx_file)


if '__main__' == __name__:
    worker = ProtocolMainWorker(
        r'C:\Users\RIMinullin\Desktop\для ворда\в высоком качестве\word_files')
    # worker.conver_pdf_to_words()
    data_from_new_type_of_protocol = worker.get_data_from_word_file(
        r'C:\Users\RIMinullin\Documents\протоколы\молочка\word_files\scan1.docx')
    print(data_from_new_type_of_protocol)
    # worker.protocol_manager.delete_all_protocols_from_table()
    # worker.write_protocols_in_dir_to_db()
    # protocol_manager = ProtocolManager()
    # protocols = protocol_manager.get_all_protocols()
    # worker.protocols_from_db_write_to_excel(PATH_TO_XLSX_FILE_WITH_PROTOCOLS)
