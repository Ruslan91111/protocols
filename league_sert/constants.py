""" Константы, в основном используемые в нескольких модулях, на разных уровнях. """
import enum
import re
import sys
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

FINE_READER_PROCESS = 'FineReader.exe'
WORD_PROCESS = 'WINWORD.EXE'

CODE_PATTERN = r'[\s№(]*[^в/ч]\s?\b(\d{5})\b[\s),]|^(\d{5})\b[.,]'

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
    'толя': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
}

FIX_KEYS_MAIN_PROT = {
    'Заявитель': re.compile(
        r'З\s*а\s*я\s*в\s*и?\s*[тг]\s*е\s*л\s*ь',
        flags=re.IGNORECASE
    ),

    'Место отбора проб': re.compile(
        (r"м\s*[ео]\s*[се]\s*[тiг1]\s*[оoае0]\s*?\s*"
         r"[оoае0]\s*[тг1]\s*б\s*о\s*р\s*а\s*?\s*"
         r"п\s*р\s*о\s*б"),
        flags=re.IGNORECASE
    ),

    'Дата и время отбора проб': re.compile(
        (r'а\s?[тчгш]\s?а?\s'
         r'([изпн]|тт)*\s*в\s?р\s?е\s?м\s?я\s'
         r'о\s?[тгi(]\s?б\s?о\s?р\s?а\s'
         r'п\s?р\s?о\s?б\s?|Дша и время отбора проб'),
        flags=re.IGNORECASE
    )
}

FIX_KEYS_SAMPLE = {
    'Производитель (фирма, предприятие, организация)': re.compile(
        (r'\(фирма,|р\s?о\s?и\s?[зэч]\s?[вн]\s?о\s?[дл]\s?и\s?[тг]\s?[еcс]*'
         r'\s?[ля]\s?[ь1][\s>]*\(ф\s*и\s*р\s*м\s*а\s*[,.]*'
         r'\s*п\s*р\s*е\s*д\s*п\s*р\s*и\s*я\s*т\s*и\s*е\s*'),
        flags=re.IGNORECASE
    ),

    'Шифр пробы': re.compile(r'(Ш|Н1|1Н)ифр [п]робы',
                             flags=re.IGNORECASE),

    'Наименование продукции': re.compile(
        (r'а[ип]\.*м[есc][нп]ова[нп]и[есc]|'
         r'(?:\s*[Н1]*[\)]?\s*и\s*м[\s\w>]*|'
         r'[кЕ]шм[се][нп]ова[нп]ие\s*)\s*'
         r'[пи]\s*р\s*о\s*д\s*у\s*к\s*ц\s*и\s*и\s*'),
        flags=re.IGNORECASE
    ),

    'Дата производства продукции': re.compile(
        (r'[дл]\s*а\s*[тгз>]?\s*а\s*п\s*р\s*о\s*и\s*з\s*'
         r'в\s*о\s*д\s*с\s*т\s*в\s*а\s*[пи]\s*р\s*о\s*д\s*у\s*к\s*ц\s*и\s*и'),
        flags=re.IGNORECASE
    ),

    'Группа продукции': re.compile(
        r'\s*[рp]\s*[уиv]\s*[пшиnнh]\s*[пнn]*\s*[аa]\s*п\s*р\s*о\s*[дл]\s*у\s*к\s*ц\s*и\s*и',
        flags=re.IGNORECASE),

    'Объект исследования': re.compile(
        (r'(\(\)|о)\s*[б&]\s*([ъьзвт])*\s*[\,\.]*\s*[ес]'
         r'\s*[ксвю][\w\s!]*с\s*с\s*л\s*е\s*д\s*о\s*в\s*а\s*н\s*и\s*[йия]\s*'),
        flags=re.IGNORECASE)
}

FIX_KEYS_OBJECT_MERGE = {'air': r'В\s*о\s*з\s*д\s*у\s*х',
                         'washings': r'С\s*м\s*ы\s*в\s*ы',
                         'water': r'В\s*о\s*д\s*а', }


class FRScreens(Enum):
    """ Пути к скриншотам, необходимым для работы с FineReader с помощью pyautogui. """
    DESKTOP_ICON: str = r'fine_reader_desktop.png'
    PANEL_ICON: str = r'fine_reader_panel.png'
    DESKTOP_APP_LOADING: str = r'fine_reader_loading.png'
    CONVERT_TO_WORD_MAIN_MENU: str = r'button_convert_to_word_main_menu.png'
    CONVERT_TO_WORD_INNER_BUTTON: str = r'blue_button_convert_to_word.png'
    INPUT_FIELD_FILE_NAME: str = r'input_file_name.png'
    PROCESS_OF_CONVERSION: str = r'process_of_conversion.png'
    BUTTON_CANCEL: str = r'button_cancel.png'
    CHECKBOX_SAVE_PICS_WITH_MARK: str = r'save_pictures.png'
    CHECKBOX_SAVE_PICS_UNMARKED: str = r'save_pictures_.png'
    CHECKMARK: str = r'remark.png'
    OPEN_DOC: str = r'open_doc.png'
    OPEN_DOC_CHECKMARK: str = r'open_doc_checkmark.png'
    IN_CONVERSION_MENU: str = r'in_fine_reader.png'
    WARNING_AFTER_CONVERT: str = r'warning.png'
    WARNING_IN_PROC: str = r'warning_in_proc.png'
    SHUT_WARNING: str = r'shut_warning.png'
    SHUT_WARNING_BLUE_FRAME: str = r'shut_warning_blue_frame.png'
    PROCESS_FINISHED: str = r'process_finished.png'
    ERROR_PAGE_NEED_TO_RM: str = r'error_page_need_to_rm.png'
    FOR_WORD_DIR: str = r'for_word_dir.png'
    CHOICE_DIR: str = r'choice_dir.png'


class ComparTypes(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма,
    для определения логики, используемой при сравнении. """
    WITHIN: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    UP_TO: str = r'\bдо\b\s\d+\,?\d*\b'  # до 1,5

    NOT_ALLOWED: str = (r'\b[нпли][ес] допускаю\s*[тг]\s*[се]я|'
                        r'^[“\s]*[-—]\s*$|'
                        r'^[\•\*]$|'
                        r'^$|'
                        r'[нпл][ес] обнаружено|'
                        r'^о[тг]сутствие$|'
                        r'^\s*[■-]*\s*$')

    AT_LEAST: str = r'\bне\s*менее\b'  # не менее 9,0
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
    START_SUBSTR: str = (
        r'п\s*о\s*п\s*р\s*о\s*и\s*з\s*в\s*о\s*д\s*с\s*т\s*в\s*е\s*н\s*н\s*о\s*м\s*у\s*'
        r'к\s*о\s*н\s*т\s*р\s*о\s*л\s*ю\s*')
    DATE: str = r'«\s?(\d{2})\s?»?\s?(\w{3,})\s?(\d{4})'
    NUMB_AND_DATE_OF_MEASUR = (r'Акта [ик] дата проведения измерений[:;]\s*'
                               r'([\d\w\s,\.\-]+)\s[гГ][,.]')
    PLACE_OF_MEASUR = (r'Адрес проведения измерени[йи][:;]\s*([\s\S]+)[\d\s\.]*'
                       r'Сведения о средствах измерения')
    START_OF_CONCLUSION = r'ЗАКЛЮЧЕНИЕ'
    INNER_PART_OF_CONCLUSION = r'-\s?на момент.*\n\n'
    NUMBER: str = r'№\s?(\d+/\d+-Д)\s*измерений'


class WordsPatterns(Enum):
    NAME = r'[Н]а[ин]м[ес]нова[ня]\s*[ин][е]'
    INDICATORS = r'Показател[ия]'
    RESULT = r"Р[ес]зул\s*[ьы][тг]*а[тг]\s*"
    REQUIREMENTS = r'Требовани[яи]'
    RESULT_OF_MEASUREMENT = RESULT + "измерений"
    SAMPLING_SITE = r"Место отбора проб"
    PLACE_OF_MEASUREMENT = "Мест[ое] измерени[йи]"
    PARAMETER = r"Измеряемый параметр"
    UNITS = r"Единицы"
    OBJECT_WASHINGS = r"(Об[ъз]\.?ект см[ыь])"
    SAMPLE_CODE = '(111|Ш)ифр пробы'


class TypesOfTable(enum.Enum):
    """ Паттерны для определения типа таблицы. """

    MAIN: str = r'З\s*а\s*я\s*в\s*и?\s*[тг]\s*е\s*л\s*ь'

    MEASURING: str = r'аим[ес]нова[нк]и[ес] ср[ео]дс[гт]\s*ва\s+изм'

    SAMPLE: str = WordsPatterns.SAMPLE_CODE.value

    PROD_CONTROL: str = (f'({WordsPatterns.PLACE_OF_MEASUREMENT.value}|'
                         f'{WordsPatterns.PARAMETER.value})')

    RESULTS: str = (f'({WordsPatterns.INDICATORS.value}|{WordsPatterns.NAME.value})|'
                    f'{WordsPatterns.SAMPLING_SITE.value}|{WordsPatterns.OBJECT_WASHINGS.value}')


class PattNumbAndDateByParts(enum.Enum):
    number = r'№?\s?(\d{,6}\s?/\d{2}-Д)'
    month = (r'января|февраля|марта|апреля|мая|июня|'
             r'июля|августа|сентября|октября|ноября|декабря|толя')
    year = r'2\s?0\s*\d{2}\s*г.'
    day = r'«\s?\d{1,2}\s?»'


class PattNumbDate(Enum):
    """  """
    SUBSTRING_START: str = \
        r'П\s?р\s?о\s?т\s?о\s?к\s?о\s?л\s+и\s?с\s?п\s?ы\s?т\s?а\s?н\s?и\s?й'
    NUMBER: str = r'№?\s?(\d{,6}\s?/\d{2}-Д)'
    DATE: str = (r'«(\d{2}|II)»\s*(января|февраля|марта|апреля|'
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
    AT_LEAST: str = r'\bне\s*менее\b'  # менее 0,10 <0,001
    NOT_FOUND: str = r'([нлпия][есо]|tie) обнару(ж|ок)[ес]н[оы]'  # не обнаружено в 25,0 г
    DIGIT: str = r'\d+,?\d*'  # 9,0
    NONE: str = r'^\s*[-—]\s*$|^$|^\s*■\s*$|^\s*⁰\s*$|^\s*■-\s*$|^[\*•]$'  # '-'
    NO_CHANGE: str = r'о[тг]сутствие изменений|о[тг]сутствие|не изменен'
    NOT_ALLOWED: str = r'[пнли][ес] допускаю\s?[тг]\s*[се]я'
    SMELL_TASTE: str = r'(з\s*а\s*[пн]\s*а\s*х\s*)|(в\s*к\s*у\s*с)'


WRONG_PARTS_IN_ROW = [
    'Физико-химические показатели',
    'Жир[ни]ок[ип]слот[пни]ый состав',
    'Микробиологические (показатели|исследования)',
    r'От\s*ветственный за оформление',
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

TABLE_TYPES_IN_RUS = {
    'store_prod': 'Продукция магазина',
    'manuf_prod': 'Продукция производителя',
    'air': 'Воздух',
    'water': 'Вода',
    'PROD_CONTROL': 'Производственный контроль',
    'MAIN': 'Основная таблица',
    'main_protocol': 'Основная таблица',
}

RECORDED_FILE = BASE_DIR / r'.\league_sert\db_operations\viewed.txt'
