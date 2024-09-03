"""
Модуль для парсинга word файл.

Код модуля обрабатывает word файл и получает из него нужные данные,
подлежащие передаче для дальнейшей работе по преобразования и сравнения.
Необходимые данные становятся свойствами объекта класса MainDataGetter.
Содержит классы и методы, направленные на извлечение данных.

Класс:
    - MainCollector:
        Верхне-уровневый класс для сбора данных.

    - CollectorFromTable:
        Класс для получения информации из таблиц word файла.


Функции:
    - prepare_for_work_with_tables:
        Подготовить word файл для работы с таблицами - преобразовать в нужный формат.

    - find_out_type_of_table:
        Определить тип таблицы по содержанию первой строки, сопоставив с паттернами.

    - get_one_string_from_file:
        Прочитать word файл, вернуть одну большую строку.

    - get_main_information:
        Найти и вернуть номер и дату протокола.

    - collect_prod_control_data:
        Найти и вернуть данные, относящиеся к измерениям производственного контроля

Пример использования:
    data_getter = MainCollector(FILE)
    data_getter.collect_all_data() - собрать все данные
    data_getter.main_number - атрибут
    data_getter.main_date - атрибут
    data_getter.data_from_tables - атрибут
    data_getter.prod_control_data - атрибут

"""
import enum
import re

from docx import Document, table
from docx2txt import docx2txt

from league_sert.data_preparation.exceptions import TypeOfTableError


class TypesOfTable(enum.Enum):
    """ Паттерны для определения типа таблицы. """
    MAIN: str = r'Заявитель'
    SAMPLE: str = r'Шифр пробы'
    RESULTS: str = r'(Показатели|Наименование\sпоказателя)|Место отбора пробы|Объект смыва'
    MEASURING: str = r'Наименование средства измерения'
    PROD_CONTROL: str = r'№ п/п\s?Место измерений'


class TextPatt(enum.Enum):
    """ Паттерны для определения типа таблицы. """
    SUBSTRING_START: str = r'П\s?р\s?о\s?т\s?о\s?к\s?о\s?л\s+и\s?с\s?п\s?ы\s?т\s?а\s?н\s?и\s?й'
    SUBSTRING_END: str = r'г.'
    NUMBER: str = r'№?([\d/]+\s?-Д)'
    DATE: str = r'«?(\d{2})»?(\w{3,})(\d{4})'


class ProdControlPatt(enum.Enum):
    """ Паттерны для извлечения данных, относящихся к измерениям
    производственного контроля. """
    START_SUBSTR: str = r'ПРОТОКОЛ\s?№?'
    DATE: str = r'«\s?(\d{2})\s?»?\s?(\w{3,})\s?(\d{4})'
    NUMB_AND_DATE_OF_MEASUR = r'№ Акта и дата проведения измерений:\s*([\d\w\s\.]+)\s[гГ][,.]'
    PLACE_OF_MEASUR = (r'Адрес проведения измерений:'
                            r'\s*([\s\S]+)[\d\s\.]*Сведения о средствах измерения')
    START_OF_CONCLUSION = r'ЗАКЛЮЧЕНИЕ'
    INNER_PART_OF_CONCLUSION = r'- на[\s\w\d\,\.]*\n\n'


def prepare_for_work_with_tables(word_file: str) -> Document():
    """ Подготовить word файл для работы с таблицами. """
    document = Document(word_file)
    return document


def get_text_with_superscripts(cell):
    """ Получить текст ячейки, обрабатывая при этом числа со степенью. """
    text = ""

    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if run.font.superscript:
                if run.text == 'б':
                    text += f"{'⁰¹²³⁴⁵⁶⁷⁸⁹'[int(6)]}"
                else:
                    text += f"{'⁰¹²³⁴⁵⁶⁷⁸⁹'[int(run.text)]}"
            else:
                text += run.text
    return text


def find_out_type_of_table(first_two_cells_text: str) -> TypesOfTable | None:
    """ Определить тип таблицы по содержанию первой строки. """
    for pattern in TypesOfTable:
        if re.search(pattern.value, first_two_cells_text):
            return pattern.name
        if re.search(r'Данная проба по исследованным ', first_two_cells_text):
            return None
    raise TypeOfTableError(first_two_cells_text)


def get_main_numb_and_date(text) -> tuple[str, str]:
    """ Найти и вернуть номер и дату протокола. """
    substring_start = re.search(TextPatt.SUBSTRING_START.value, text).start()
    substring_end = (re.search(TextPatt.SUBSTRING_END.value,
                               text[substring_start:]).start() + substring_start)
    substring_with_number = re.sub(r'[\t\n\s]*', '', text[substring_start:substring_end])

    # Найти и вернуть номер и дату протокола.
    number_of_protocol = re.search(TextPatt.NUMBER.value, substring_with_number).group(1)
    match = re.search(TextPatt.DATE.value, substring_with_number)
    date_of_protocol = match.group(1) + ' ' + match.group(2) + ' ' + match.group(3)
    return number_of_protocol, date_of_protocol


class CollectorFromTable:
    """ Класс для получения информации из таблиц word файла. """

    def __init__(self, document_with_tables):
        self.all_tables_in_file: list = document_with_tables.tables
        self.converted_data_from_tables = {}
        self.current_table: table.Table
        self.key_of_current_table: str
        self.value_of_current_table: list | dict

    def process_two_columns_table(self):
        """ Преобразовать таблицу, состоящую из двух колонок в словарь,
         где ключ значение из первой колонки, а значение из второй колонки."""

        self.value_of_current_table = {}
        for _, row in enumerate(self.current_table.rows):
            cells = row.cells
            for _ in cells:
                key_of_row = cells[0].text.strip()
                value_of_row = cells[1].text.strip()
                self.value_of_current_table[key_of_row] = value_of_row
        self.converted_data_from_tables[self.key_of_current_table] = self.value_of_current_table

    def process_more_then_two_cols(self):
        """ Преобразовать таблицу, состоящую из более чем двух колонок
        в список со вложенными списками. Каждый вложенный список это значения
        из одной строки таблицы. """
        self.value_of_current_table = []
        for _, row in enumerate(self.current_table.rows):
            one_row = []
            cells = row.cells
            for cell in cells:
                cell_text = get_text_with_superscripts(cell)
                one_row.append(cell_text)
            self.value_of_current_table.append(one_row)
        self.converted_data_from_tables[self.key_of_current_table] = self.value_of_current_table

    def extract_data_from_all_tables(self):
        """ Собрать в словарь, данные из всех таблиц word файла, 
         ключом будет tuple, где первое значение порядковый номер таблицы в документе
         второе тип таблицы. Значением в итоговом словаре для таблицы
         будут данные либо в виде списка со вложенными списками, 
         либо в виде словаря. """

        for table_number, table_ in enumerate(self.all_tables_in_file):  # Цикл по таблицам.
            self.current_table = table_  # Текущая таблица

            if len(table_.rows) > 1:  # Проверка на наличие в таблице более двух строк.
                first_row_cells = table_.row_cells(0)
                text_from_first_two_cells = first_row_cells[0].text + first_row_cells[1].text
                type_of_table = find_out_type_of_table(text_from_first_two_cells)
                self.key_of_current_table = (table_number, type_of_table)

                if type_of_table in {TypesOfTable.MAIN.name,
                                     TypesOfTable.SAMPLE.name}:
                    self.process_two_columns_table()

                if type_of_table in {TypesOfTable.RESULTS.name,
                                     TypesOfTable.PROD_CONTROL.name}:
                    self.process_more_then_two_cols()


def collect_prod_control_data(text) -> dict:
    """ Найти и вернуть данные, относящиеся к измерениям
    производственного контроля. """
    try:
        substr_start = re.search(ProdControlPatt.START_SUBSTR.value, text).start()
        prod_control_text = text[substr_start:]
        number_of_protocol = re.search(TextPatt.NUMBER.value, prod_control_text).group(1)

        match = re.search(ProdControlPatt.DATE.value, prod_control_text)
        date_of_protocol = (match.group(1) + ' ' + match.group(2) + ' ' + match.group(3))

        match = re.search(ProdControlPatt.NUMB_AND_DATE_OF_MEASUR.value, prod_control_text)
        date_of_measurement = match.group(1)

        match = re.search(ProdControlPatt.PLACE_OF_MEASUR.value, prod_control_text)
        place_of_measurement = match.group(1).strip()

        inner_conclusion = re.search(ProdControlPatt.INNER_PART_OF_CONCLUSION.value,
                                     prod_control_text).group().strip()

        return {'number_of_protocol': number_of_protocol,
                'date_of_protocol': date_of_protocol,
                'act': date_of_measurement,
                'place_of_measurement': place_of_measurement,
                'inner_conclusion': inner_conclusion}

    except AttributeError:
        print('Таблицы производственного контроля не найдено')


class MainCollector:
    """ Верхне-уровневый класс для получения данных"""
    def __init__(self, file_path):
        self.file = file_path
        self.tables_from_file = None
        self.data_from_tables: dict
        self.text = None
        self.main_number = None
        self.main_date = None
        self.prod_control_data = None

    def get_data_from_tables(self):
        """ Получить все данные из таблиц"""
        converter = CollectorFromTable(self.prepare_for_work_with_tables())
        converter.extract_data_from_all_tables()
        self.data_from_tables = converter.converted_data_from_tables

    def get_string(self):
        """ Получить строку для поиска строк, вне таблиц"""
        if not self.text:
            self.text = docx2txt.process(self.file)
        return self.text

    def prepare_for_work_with_tables(self):
        """ Подготовить файл для извлечения данных из таблиц. """
        if not self.tables_from_file:
            self.tables_from_file = prepare_for_work_with_tables(self.file)
        return self.tables_from_file

    def get_main_information(self):
        """ Получить основные данные из файла. """
        if not self.main_number or not self.main_date:
            self.main_number, self.main_date = get_main_numb_and_date(
                self.get_string())

    def get_prod_control_data(self):
        """ Получить из файла данные о производственном контроле. """
        if not self.prod_control_data:
            self.prod_control_data = collect_prod_control_data(self.get_string())

    def collect_all_data(self):
        """ Собрать все данные из word файла. """
        self.get_main_information()
        self.get_data_from_tables()
        self.get_prod_control_data()

    def merge_prod_control(self):
        for key, value in self.data_from_tables.items():
            if key[1] == 'PROD_CONTROL':
                updated = {**self.prod_control_data, 'indicators': [value]}
                self.data_from_tables[key] = updated
                continue
