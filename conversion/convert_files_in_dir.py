"""
Модуль для конвертации PDF файлов в Word и проверки наличия
номеров и дат протоколов в конвертированных файлах.

Этот модуль предоставляет функциональность для автоматического
конвертирования всех PDF файлов в указанной директории в формат Word
с помощью "кликера" и программы FineReader и последующей проверки данных в каждом
конвертированном документе. Модуль включает в себя два основных
класса: `FileConverter` для выполнения самой конвертации и
`WordChecker` для проверки содержимого файлов на наличие специфических
данных, таких как номера и даты протоколов.

Классы:

    - `FileConverter`: Класс, реализующий логику конвертации одного
      документа из PDF в Word. Он позволяет выбрать исходный PDF файл
      и задать целевую директорию для сохранения результата в формате Word.

    - `WordChecker`: Класс, предоставляющий методы для проверки
      конвертированного файла в формате Word. Он ищет в документе
      номера основного протокола и даты протоколов производственного контроля.

Функции:

    - `check_word_file(file_path: str) -> tuple | False`:
      Проверяет указанный Word файл на наличие номеров и дат протоколов.
      Возвращает кортеж с найденными значениями, если проверки успешны,
      либо False, если необходимые данные не найдены.

    - `convert_a_file(file_path: str, dir_with_pdf_files: str, dir_for_word_files: str) -> None`:
      Конвертирует один указанный PDF файл в формат Word и сохраняет
      его в заданную директорию. Осуществляет взаимодействие с
      внешним "кликером" для выполнения конвертации.

    - `convert_all_pdf_in_dir_to_word(dir_with_pdf_files: str) -> None`:
      Запрашивает у пользователя путь к директории с PDF файлами. Создаёт
      директорию для сохранения Word файлов и запускает процесс
      конвертации всех PDF файлов в указанной директории.
      После конвертации, выполняет проверку каждого Word файла
      на наличие номеров и дат протоколов, используя `WordChecker`.

Пример использования:
    convert_all_pdf_in_dir_to_word(dir_with_pdf_files)

"""
import os
import re
from docx import Document
from docx2txt import docx2txt

from league_sert.constants import FRScreens, FINE_READER_PROCESS, PattNumbDate, ProdControlPatt
from league_sert.data_preparation.extract_numb_and_date import get_main_numb_and_date

from conversion.exceptions import ScreenshotNotFoundError
from conversion.remove_back_elements import process_pdf

from conversion.files_and_proc_works import (return_or_create_dir,
                                             fetch_files_for_conversion,
                                             is_file_in_dir)

from conversion.screen_work import (click_scr, launch_desktop_app,
                                    wait_fr_app_loading, click_convert_main_menu,
                                    input_filename, is_in_convert_to_word_section,
                                    uncheck_save_image, uncheck_open_doc,
                                    click_convert_blue_button, handle_fr_warning,
                                    check_save_image, wait_scr)


class FileConverter:
    """ Класс конвертер одного документа."""

    def __init__(self, file: str, dir_pdf_files: str, dir_word_files: str):
        self.file = file
        self.dir_pdf_files = dir_pdf_files
        self.dir_word_files = dir_word_files
        self.file_pdf_original = os.path.join(dir_pdf_files, file) + '.pdf'
        self.file_word_original = os.path.join(dir_word_files, file) + '.docx'
        self.temp_pdf_file = self.file_pdf_original.replace('.pdf', '_no_stamps.pdf')
        self.temp_word_file = self.file_word_original.replace('.docx', '_temp.docx')
        self.numbs_and_dates = None

    def input_pdf_origin(self):
        """ Ввести путь к оригинальному ПДФ файлу. """
        input_filename(self.file_pdf_original)
        try:
            wait_scr(FRScreens.CONVERT_TO_WORD_INNER_BUTTON.value)
        except ScreenshotNotFoundError:
            input_filename(self.file_pdf_original)

    def input_path_to_word(self):
        """ Ввести путь к word файлу, в который будет конвертирован ПДФ. """
        input_filename(self.file_word_original)

        try:
            click_scr(FRScreens.PROCESS_OF_CONVERSION.value)
        except:
            input_filename(self.file_word_original)

    def convert_file(self):
        """ Выполнить действия по конвертированию одного файла. """
        click_convert_main_menu()
        self.input_pdf_origin()
        check_save_image()
        click_convert_blue_button()
        uncheck_open_doc()
        self.input_path_to_word()
        is_file_in_dir(self.dir_word_files, self.file + '.docx')
        handle_fr_warning()
        click_scr(FRScreens.BUTTON_CANCEL.value)

    def check_numbs_and_date(self):
        """ Проверить есть ли в протоколе номера и даты. """
        self.numbs_and_dates = check_word_file(self.file_word_original)
        if self.numbs_and_dates:
            return True

    def extract_numbs_and_dates(self):
        """ Набор действий по повторной конвертации pdf файла без печатей. """
        process_pdf(self.file_pdf_original, self.temp_pdf_file)
        click_convert_main_menu()
        input_filename(self.temp_pdf_file)
        uncheck_save_image()
        click_convert_blue_button()
        uncheck_open_doc()
        input_filename(self.temp_word_file)
        is_file_in_dir(self.dir_word_files,
                       self.temp_word_file[self.temp_word_file.rfind('\\') + 1:])
        handle_fr_warning()
        click_scr(FRScreens.BUTTON_CANCEL.value)

    def add_numbs_and_dates_to_file(self):
        """ Получить из word файла без печатей номера и даты протоколов
        и дописать их в оригинальный word файл."""
        try:
            (main_date,
             main_numb,
             prod_contr_numb,
             prod_contr_date) = check_word_file(self.temp_word_file)

        except TypeError:
            print('Нет номеров и дат протоколов.')
            return

        doc = Document(self.file_word_original)

        doc.add_paragraph(f'Протокол испытаний № {main_numb} от {main_date}')
        doc.add_paragraph(f'ПРОТОКОЛ № {prod_contr_numb} измерений '
                          f'по производственному контролю от {prod_contr_date}')
        doc.save(self.file_word_original)
        print('Записаны в файл номера и даты протоколов.')
        os.remove(self.temp_pdf_file)
        os.remove(self.temp_word_file)

    def convert_and_check(self):
        """ Весь процесс конвертации файла, проверки на номера. """
        self.convert_file()
        numbs_and_dates = self.check_numbs_and_date()
        if numbs_and_dates:
            print(numbs_and_dates)
            return
        self.extract_numbs_and_dates()
        self.add_numbs_and_dates_to_file()


class WordChecker:
    """ Класс для проверки конвертированного файла формата word
    на наличие номера и даты основного протокола и протокола
    производственного контроля. """

    def __init__(self, file_path):
        self.file_path = file_path
        self.text = docx2txt.process(self.file_path)
        self.main_numb = None
        self.main_date = None
        self.prod_contr_numb = None
        self.prod_contr_date = None

    def get_main_numb_and_date(self):
        """ Проверить наличие номера и даты основного протокола. """
        self.main_numb, self.main_date = get_main_numb_and_date(self.text, self.file_path)

    def get_prod_contr_numb_and_date(self):
        """ Проверить наличие номера и даты протокола производственного контроля. """
        try:
            substr_start = re.search(ProdControlPatt.START_SUBSTR.value, self.text).start()
            prod_control_text = self.text[substr_start:]
            self.prod_contr_numb = re.search(PattNumbDate.NUMBER.value, prod_control_text).group(1)
            match = re.search(ProdControlPatt.DATE.value, prod_control_text)
            self.prod_contr_date = match.group(1) + ' ' + match.group(2) + ' ' + match.group(3)

        except Exception as e:
            print(e)


def check_word_file(file_path: str) -> tuple | False:
    """ Проверить ворд файл на наличие номеров и дат протоколов. """
    word_checker = WordChecker(file_path)
    word_checker.get_main_numb_and_date()
    word_checker.get_prod_contr_numb_and_date()
    if (word_checker.main_date and word_checker.main_numb
            and word_checker.prod_contr_numb and word_checker.prod_contr_date):
        return (word_checker.main_date, word_checker.main_numb,
                word_checker.prod_contr_numb, word_checker.prod_contr_date)
    return False


def convert_a_file(file_path: str, dir_with_pdf_files: str, dir_for_word_files: str) -> None:
    """ Конвертировать один файл. """
    converter = FileConverter(file_path, dir_with_pdf_files, dir_for_word_files)
    converter.convert_and_check()


def convert_all_pdf_in_dir_to_word(dir_with_pdf_files: str) -> None:
    """ Получить от пользователя путь к директории с PDF файлами создать директорию,
    в которую будут сохранены файлы в формате word после конвертации. """

    dir_for_word_files = return_or_create_dir(dir_with_pdf_files + '\\word_files\\')

    # Перечень файлов, которые еще не конвертированы.
    files_for_convert = fetch_files_for_conversion(dir_with_pdf_files, dir_for_word_files)

    # Запустить FineReader.
    launch_desktop_app(FINE_READER_PROCESS, FRScreens.PANEL_ICON.value,
                       FRScreens.DESKTOP_ICON.value, 0.8)
    wait_fr_app_loading()
    is_in_convert_to_word_section()

    # Перебираем файлы в перечне файлов, нуждающихся в конвертации.
    for file in files_for_convert:
        convert_a_file(file, dir_with_pdf_files, dir_for_word_files)
        print(file)
