""" Константы, в основном используемые в нескольких модулях, на разных уровнях. """
import enum
from enum import Enum


FINE_READER_PROCESS = 'FineReader.exe'
WORD_PROCESS = 'WINWORD.EXE'

CODE_PATTERN = r'[\s№(]*[^в/ч]\s?\b(\d{5})\b[\s),]|^(\d{5})\b[.,]'

# Старый
# CODE_PATTERN = r'[\s№(]\s?(\d{5})[\s),]|^(\d{5})[.,]'

DIGITS_IN_DEGREE = {'⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4,
                    '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9}

MONTHS = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
}


class FRScreens(Enum):
    """ Пути к скриншотам, необходимым для работы с FineReader с помощью pyautogui. """
    DESKTOP_ICON: str = r'./screenshots/fine_reader_desktop.png'
    PANEL_ICON: str = r'./screenshots/fine_reader_panel.png'
    DESKTOP_APP_LOADING: str = r'./screenshots/fine_reader_loading.png'
    CONVERT_TO_WORD_MAIN_MENU: str = r'./screenshots/button_convert_to_word_main_menu.png'
    CONVERT_TO_WORD_INNER_BUTTON: str = r'./screenshots/blue_button_convert_to_word.png'
    INPUT_FIELD_FILE_NAME: str = r'screenshots/input_file_name.png'
    PROCESS_OF_CONVERSION: str = r'./screenshots/process_of_conversion.png'
    BUTTON_CANCEL: str = r'./screenshots/button_cancel.png'
    CHECKBOX_SAVE_PICS_WITH_MARK: str = r'./screenshots/save_pictures.png'
    CHECKBOX_SAVE_PICS_UNMARKED: str = r'./screenshots/save_pictures_.png'
    CHECKMARK: str = r'./screenshots/remark.png'
    OPEN_DOC: str = r'./screenshots/open_doc.png'
    OPEN_DOC_CHECKMARK: str = r'./screenshots/open_doc_checkmark.png'
    IN_CONVERSION_MENU: str = r'./screenshots/in_fine_reader.png'
    WARNING_AFTER_CONVERT: str = r'./screenshots/warning.png'
    WARNING_IN_PROC: str = r'./screenshots/warning_in_proc.png'
    SHUT_WARNING: str = r'./screenshots/shut_warning.png'
    PROCESS_FINISHED: str = r'./screenshots/process_finished.png'


class ComparTypes(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма,
    для определения логики, используемой при сравнении. """
    WITHIN: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    UP_TO: str = r'\bдо\b\s\d+\,?\d*\b'  # до 1,5

    NOT_ALLOWED: str = (r'\b[нпли][ес] допускаю\s*[тг]\s*[се]я|'
                        r'^[“\s]*[-—]\s*$|'
                        r'^$|'
                        r'[нпл][ес] обнаружено|'
                        r'^о[тг]сутствие$|'
                        r'^\s*[■-]*\s*$')

    AT_LEAST: str = r'\bне менее \d+\,?\d*\s?'  # не менее 9,0
    NO_MORE: str = r'\bне более\b'  # не более 220,0
    DIGIT: str = r'\d+,?\d*'  # 220
    NO_CHANGE: str = r'о[тг]сутствие изменений'
    SMELL_TASTE: str = r'(з\s*а\s*п\s*а\s*х\s*)|(в\s*к\s*у\s*с)'


class MsgForUser(Enum):
    """ Сообщения для пользователя. """
    DIR_PDF_WITHOUT_BACKGROUND: str = (
        'Введите полный путь (включая сетевой диск) до директории, '
        'в которой находятся файлы формата PDF, нуждающиеся в конвертации в формат Word:'
        '\n>>>')

    DIR_ORIGINAL_PDF: str = (
        'Введите полный путь (включая сетевой диск) до директории, '
        'в которой находятся файлы формата PDF, нуждающиеся в удалении фона:'
        '\n>>>')


class ProdControlPatt(Enum):
    """ Паттерны для извлечения данных, относящихся к измерениям
    производственного контроля. """
    START_SUBSTR: str = (r'п\s*о\s*п\s*р\s*о\s*и\s*з\s*в\s*о\s*д\s*с\s*т\s*в\s*е\s*н\s*н\s*о\s*м\s*у\s*'
                         r'к\s*о\s*н\s*т\s*р\s*о\s*л\s*ю\s*')
    DATE: str = r'«\s?(\d{2})\s?»?\s?(\w{3,})\s?(\d{4})'
    NUMB_AND_DATE_OF_MEASUR = (r'№[’>\s]*Акта и дата проведения измерений[:;]\s*'
                               r'([\d\w\s,\.]+)\s[гГ][,.]')
    PLACE_OF_MEASUR = (r'Адрес проведения измерений[:;]\s*([\s\S]+)[\d\s\.]*'
                       r'Сведения о средствах измерения')
    START_OF_CONCLUSION = r'ЗАКЛЮЧЕНИЕ'
    INNER_PART_OF_CONCLUSION = r'-\s?на момент.*\n\n'
    NUMBER: str = r'№\s?(\d+/\d+-Д)\s*измерений'


class WordsPatterns(Enum):
    NAME = r'[Н]аим[ес]нован\s*[ин][е]'
    INDICATORS = r'Показател[ия]'
    RESULT = r"Р[ес]зул\s*[ьы][тг]*а[тг]\s*"
    REQUIREMENTS = r'Требовани[яи]'
    RESULT_OF_MEASUREMENT = RESULT + "измерений"
    SAMPLING_SITE = r"Место отбора проб"
    PLACE_OF_MEASUREMENT = "Мест[ое] измерени[йи]"
    PARAMETER = r"Измеряемый параметр"
    UNITS = r"Единицы"
    OBJECT_WASHINGS = r"(Об[ъз]\.?ект см[ыь])"
    SAMPLE_CODE = r'Шифр пробы'


class TypesOfTable(enum.Enum):
    """ Паттерны для определения типа таблицы. """
    MAIN: str = r'Заяви?\s*[тг]ель'
    MEASURING: str = r'аим[ес]нова[нк]и[ес] ср[ео]дс[гт]\s*ва\s+изм'
    SAMPLE: str = WordsPatterns.SAMPLE_CODE.value
    PROD_CONTROL: str = (f'({WordsPatterns.PLACE_OF_MEASUREMENT.value}|'
                         f'{WordsPatterns.PARAMETER.value})')
    RESULTS: str = (f'({WordsPatterns.INDICATORS.value}|{WordsPatterns.NAME.value})|'
                    f'{WordsPatterns.SAMPLING_SITE.value}|{WordsPatterns.OBJECT_WASHINGS.value}')
    # RESULTS: str = r'(Показатели|Наименован\s*[ин][е])|Место отбора пробы|Объект см[ыь]'


class PattNumbAndDateByParts(enum.Enum):
    number = r'№?\s?(\d{,6}\s?/\d{2}-Д)'
    month = (r'января|февраля|марта|апреля|мая|июня|'
             r'июля|августа|сентября|октября|ноября|декабря|толя')
    year = r'\d{2}\s*\d{2}\s*г.'
    day = r'«\s?\d{1,2}\s?»'


class PattNumbDate(Enum):
    """  """
    SUBSTRING_START: str = \
        r'П\s?р\s?о\s?т\s?о\s?к\s?о\s?л\s+и\s?с\s?п\s?ы\s?т\s?а\s?н\s?и\s?й'
    NUMBER: str = r'№?\s?(\d{,6}\s?/\d{2}-Д)'
    DATE: str = (r'«(\d{2})»\s*(января|февраля|марта|апреля|'
                 r'мая|июня|июля|августа|сентября|октября|ноября|декабря)'
                 r'\s*(\d{2}\s*\d{2})')


class ConvertValueTypes(Enum):
    """ Тип преобразования значения. Исходя из типа значение будет
    преобразовано определенным образом. """

    PLUS: str = r'\d\s?[+±]\s?\d'  # 16,34±0,15;  +
    MULTIPLICATION: str = r'\d\s?[•■*xх]\s?\d'  # 1 ■ 101², 1 • 10², 5,5х102
    NO_MORE: str = r'до \d+,?\d*'  # до 1,5
    WITHIN: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    LESS: str = r'менее \d+,?\d*|<\d+,?\d*'  # менее 0,10 <0,001
    NOT_FOUND: str = r'([нлпи][есо]|tie) обнару(ж|ок)[ес]н[оы]'  # не обнаружено в 25,0 г
    DIGIT: str = r'\d+,?\d*'  # 9,0
    NONE: str = r'^\s*[-—]\s*$|^$|^\s*■\s*$|^\s*⁰\s*$|^\s*■-\s*$'  # '-'
    NO_CHANGE: str = r'о[тг]сутствие изменений|о[тг]сутствие|не изменен'
    NOT_ALLOWED: str = r'[пнли][ес] допускаю\s?[тг]\s*[се]я'
    SMELL_TASTE: str = r'(з\s*а\s*п\s*а\s*х\s*)|(в\s*к\s*у\s*с)'


WRONG_PARTS_IN_ROW = [
    'Физико-химические показатели',
    'Жир[ни]ок[ип]слот[пни]ый состав',
    'Микробиологические (показатели|исследования)',
    'От\s*ветственный за оформление',
    'Аверкова',
    '[пХ]одпись',
    'Токсичные элементы, мг/кг:',
    'Пестициды, мг/кг:',
    'Ф.И.О.',
    'анализатор жидкости',
    'Данные о пробе',
    'Прибор комбинированный',
    'Д[ао][нч]ная пр[оея]'
]


WRONG_FIRST_CELLS_IN_TAB = [
    'Физико-химические показатели',
    'Микробиологические показатели',
    'Микробиологические исследования',
]

TEST_OBJECT = r'о\s*б\s*[ъ>]\s*е\s*к\s*т\s*и\s*с\s*с\s*л\s*е\s*д'


class TableWords(Enum):
    UP_TO: str = r'\bдо\b'  # до 1,5
    NOT_ALLOWED: str = (r'\b[нпли][ес] допускаю\s*[тг]\s*[се]я|'
                        r'[нпл][ес] обнаружено|'
                        r'^о[тг]сутствие$|')

    AT_LEAST: str = r'\bне\s*менее\b'  # не менее 9,0
    NO_MORE: str = r'\bне\s*более\b'  # не более 220,0
    NO_CHANGE: str = r'о[тг]сутствие изменений'
    SMELL_TASTE: str = r'(з\s*а\s*п\s*а\s*х\s*)|(в\s*к\s*у\s*с)'


TABLE_WORDS_PATTERN = (r"[Н]аим[ес]нован\s*[ин][е]|"
                 r"Показател|"
                 r"Требовани|"
                 r"измерений|"
                 r"Место|"
                 r"Измеряемый|"
                 r"параметр|"
                 r"Единицы|"
                 r"Шифр|"
                 r"допускаю|"
                 r"обнаружено|"
                 r"сутствие$|"
                 r"запах|"
                 r"вкус")
