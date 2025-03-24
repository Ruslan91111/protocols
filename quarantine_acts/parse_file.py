"""
Код связанные с поиском и изъятием текста из файлов html.
"""
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from bs4 import BeautifulSoup

from league_sert.constants import MONTHS
from quarantine_acts.models import QuarantineAct


START_FOR_MINI_TABLE = r'действие с образ[цн]ом'


class Words(Enum):
    """ Слова, используемое в паттернах """
    NAME: str = r'(\(на[ипн]м|\(iiaiiMe|\(псп/менсваине)'
    AS_A_RESULT: str = r'[вкI]* результате'


class PatternsHalfAttrs(Enum):
    """ Паттерны для поиска первой половины атрибутов, без данных из таблицы из приложения. """
    date = r'[осе][тгr]\s*(\d{2}\s*\w{3,8}\s*\d{4})\s*[гт][оес]да'
    number = r'№\s*(\d{15})'
    vehicle = r'и транспортных средств(.*\d{2}.\d{2}.\d{4})'
    exporter = fr'экспортер \(отправитель\):\s*([\s\S]*?)(?=\s*(?:импортер|{Words.NAME.value}))'
    importer = fr'импортер \(получатель\):\s*(.*?)\s*(?:\([^)]*\))?\s*{Words.AS_A_RESULT.value}'


class PatternsDataFromAppendix(Enum):
    """ Паттерны для поиска второй половины атрибутов, с данными из таблицы из приложения. """
    name_of_prod = r'[\w\s]+,[\w\s]+'
    certificate_number = r'[\w\s]*\d{6,}'
    certificate_date = r'\d{2}[,\.]\d{2}[,\.]\d{4}'
    weight = r'\d+[,\.]*\d*\s*т'


@dataclass
class Information:
    """ Класс для хранения данных из акта карантинного акта. """
    # Первая часть атрибутов.
    number: int = None
    date: datetime = None
    vehicle: str = None
    exporter: str = None
    importer: str = None
    # Вторя часть атрибутов.
    name_of_prod: str = None
    certificate_number: str = None
    certificate_date: datetime = None
    weight: float = None

    def to_model(self):
        """ Конвертировать в объект класса QuarantineAct. """
        quarantine_act = QuarantineAct()
        quarantine_act.number = self.number
        quarantine_act.date = self.date
        quarantine_act.vehicle = self.vehicle
        quarantine_act.exporter = self.exporter
        quarantine_act.importer = self.importer
        quarantine_act.name_of_prod = self.name_of_prod
        quarantine_act.certificate_number = self.certificate_number
        quarantine_act.certificate_date = self.certificate_date
        quarantine_act.weight = self.weight
        return quarantine_act

    def to_dict(self):
        """ Преобразует объект в словарь. """
        return {
            "main_date": self.date,
            "main_number": self.number,
            "vehicle": self.vehicle,
            "exporter": self.exporter,
            "importer": self.importer,
            "name_of_prod": self.name_of_prod,
            "certificate_number": self.certificate_number,
            "certificate_date": self.certificate_date,
            "weight": self.weight
        }


def read_html_file(file_path: Path) -> BeautifulSoup | None:
    """ Прочитать html-файл и вернуть объект soup. """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None

    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None


def traverse_soup(soup: BeautifulSoup) -> None:
    """ Получить объект soup, рекурсивно обойти все узлы и элементы и
     вывести весь текст, который содержится у узлах. """

    def recursive_traverse(element):
        if element.name is not None:
            print(f"Тег: {element.name}")
            if element.text.strip():
                print(f"Текст: {element.text.strip()}")
        for child in element.children:
            if child.name is not None:
                recursive_traverse(child)
            elif child.strip():
                print(f"Текст: {child.strip()}")

    recursive_traverse(soup)


def iterate_text_elements(soup: BeautifulSoup):
    """
    Рекурсивная функция-генератор для перебора элементов, содержащих текст.
    возвращает текст по-строчно из одного элемента html.

    :param soup: Объект BeautifulSoup.
    :yield: Текст элемента.
    """

    def recursive_iterate(element):
        if element and element.text.strip():
            yield element.text.strip()

        for child in element.children:
            if not isinstance(child, str):  # Пропускаем строки, т.к. они не имеют детей
                yield from recursive_iterate(child)

    yield from recursive_iterate(soup)


class DataExtractor:
    """ Класс для получения данных из файла пдф с карантинным актом. """

    def __init__(self, file: Path):
        self.file = file
        self.soup = read_html_file(self.file)
        self.solid_text = ''
        self.data = Information()

    def set_attrs_for_appendix(self, str_appendix: str):
        """ Получить данные о продукте из одного единого абзаца. """
        found_elems = {}  # Словарь для найденных элементов.
        rows = str_appendix.split("\n")  # Разбить строку по знакам переноса.
        been_attrs = set()  # Найденные атрибуты.
        
        # Перебираем строки и сравниваем их с паттернами, характерными для определенных атрибутов.
        for row in rows:
            for pat in PatternsDataFromAppendix:
                
                # Пропускаем уже найденные атрибуты.
                if pat.name in been_attrs:
                    continue

                # Обработка найденного атрибута.
                match_ = re.search(pat.value, row, re.IGNORECASE)
                if match_:
                    found_elems[pat.name] = match_.group()
                    been_attrs.add(pat.name)
                    
        # Присваиваем и сохраняем найденные элементы.
        self.data.name_of_prod = found_elems.get('name_of_prod', None)
        self.data.certificate_number = found_elems.get('certificate_number', None)
        self.data.certificate_date = found_elems.get('certificate_date', None)
        
        # Обработка и манипуляции с весом перевозки.
        weight = found_elems.get('weight', None)
        if weight:
            weight = re.sub(r'\s*[А-Яа-я]', r'', weight)
            weight = float(weight.replace(',', '.'))
        self.data.weight = weight

    def _extract_importer(self):
        """Извлекает значение importer."""
        text = self.solid_text.replace('\n', ' ')
        importer = re.search(PatternsHalfAttrs.importer.value, text, re.IGNORECASE)
        if importer:
            importer_text = importer.group(0)
            start = importer_text.find(':') + 1
            end = importer_text.rfind('(')
            if end < start:
                end = re.search(Words.AS_A_RESULT.value, importer_text, re.IGNORECASE).start()
            return importer.group()[start:end].strip(' \n')

        return None

    def _set_attribute(self, field_name, value):
        """Устанавливает атрибут, если он еще не установлен."""
        if not getattr(self.data, field_name) and value:
            setattr(self.data, field_name, value)

    def _search_and_extract(self, pattern, group_number=1):
        """Выполняет поиск по регулярному выражению и извлекает значение."""
        value = re.search(pattern, self.solid_text, re.IGNORECASE)
        if value:
            return value.group(group_number).strip(' \n')
        return None

    def set_an_attribute(self, field_name, pattern, group_number=1):
        """В сплошном тексте найти значение для одного переданного атрибута и установить атрибут и значение."""

        if field_name == 'importer':
            value = self._extract_importer()
        else:
            value = self._search_and_extract(pattern, group_number)

        self._set_attribute(field_name, value)

    def set_main_attrs(self):
        """ Установить основные атрибуты."""
        for pattern in PatternsHalfAttrs:
            self.set_an_attribute(pattern.name, pattern.value)

    def set_attrs_from_appendix(self):
        """ Поиск и установка атрибутов из приложения к акту. """

        if not getattr(self.data, 'name_of_prod'):
            substring_text_start = re.search(START_FOR_MINI_TABLE, self.solid_text)
            if substring_text_start:
                substring_text_start = substring_text_start.end()
                substring = self.solid_text[substring_text_start:substring_text_start + 400]
                substring = substring.strip('\n, 1')
                self.set_attrs_for_appendix(substring)

    def process_the_date(self):
        """ Обработка даты протокола, преобразование в нужный формат даты. """
        date_string = self.data.date
        if not isinstance(date_string, str):
            return

        match = re.search(r'(\d{2})\s(\w{3,7})\s(\d{4})', date_string)
        if match:
            month = MONTHS[match.group(2)]
            day = match.group(1)
            year = match.group(3)
            self.data.date = datetime.strptime(day + '-' + month + '-' + year, '%d-%m-%Y')

    def get_data_from_solid_text(self):
        """ Получит нужные данные из сплошного текста. """
        self.set_main_attrs()
        self.process_the_date()
        self.set_attrs_from_appendix()

    def get_required_data(self):
        """ Получить все необходимые данные из акта. """

        # Генератор, который будет выдавать поочередно текст из элементов.
        text_gener = iterate_text_elements(self.soup)

        # Перебираем данные из генератора.
        try:
            while True:
                text = next(text_gener)
                self.solid_text = text
                self.get_data_from_solid_text()

        except StopIteration:
            pass


def create_instance_of_model_from_html(file: Path) -> QuarantineAct:
    """ Получить данные из файла html и преобразовать в определенный вид. """
    data_extractor = DataExtractor(file)
    data_extractor.get_required_data()
    return data_extractor.data.to_model()
