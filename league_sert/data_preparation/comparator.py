"""
Модуль для сравнения результатов исследований и норм. Принимает и обрабатывает два значения,
которые сравнивает, исходя из типа значений. Возвращает результат сравнения в виде
bool | list[bool]. list[bool] - возвращается, когда результат содержит число с погрешностью.

Пример использования:
    - create_conformity_conclusion(result: str, norm: str)

Классы:

    - ComparatorResNorms:
        Класс для сравнения результатов исследования с нормами.
        Принимает два значения: результат исследования и нормы для показателя.
        Определяет тип сравнения, производит сравнение и формирует вывод.
        Вывод о соответствии нормам присваивается атрибуту - self.conclusion.
        В своей работе создает и использует объекты класса ValueProcessor

Функции:

    - create_conformity_conclusion:
        Функция для сравнения результатов исследования с нормой.
        Возвращает либо bool если значение результат исследования одно число,
        и list[bool] если значение результата исследования имеет погрешность
        в виде '±'. В своей работе создает и оперирует классом CompareResultAndNorms.


enum классы:
    - ComparisonTypes:
        Тип сравнения в зависимости от содержания в поле норма,
        для определения логики, используемой при сравнении.

Пример использования:
    - conclusion = compare_result_and_norms(result: str, norm: str)

"""
from league_sert.data_preparation.common import ComparTypes
from league_sert.data_preparation.exceptions import MethodOfComparisonError
from league_sert.data_preparation.value_processor import to_process_the_value, \
    define_value_type


class Comparator:
    """ Класс для сравнения результатов исследования с нормами.
    если показатель соответствует норме, то self.conclusion = True. """

    def __init__(self, result: str, norm: str):
        self.comparison_type = define_value_type(norm, ComparTypes)
        self.result = to_process_the_value(result)  # Результат исследования
        self.norm = to_process_the_value(norm)  # Нормы
        self.conclusion = None  # Вывод о наличии нарушений нормам.

    def compare_within(self):
        """ Сравнение, когда нормы определены в виде нижнего
         и верхнего допустимого значения. """
        if isinstance(self.result, list):
            self.conclusion = (self.norm[0] < self.result[0] <= self.norm[1],
                               self.norm[0] < self.result[1] <= self.norm[1])
        else:
            self.conclusion = self.norm[0] < self.result <= self.norm[1]

    def compare_up_to(self):
        """ Сравнение, когда нормы определены в виде
        'до определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] <= self.norm, self.result[1] <= self.norm)
        else:
            self.conclusion = self.result <= self.norm

    def compare_not_allowed(self):
        """ Сравнение, когда нормы определены в виде
        'не допускаются'. """
        self.conclusion = True if self.result == 0 or self.result == 0.01 else False

    def compare_at_least(self):
        """ Сравнение, когда нормы определены в виде
        'не менее определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] > self.norm, self.result[1] > self.norm)
        else:
            self.conclusion = self.result >= self.norm

    def compare_no_more(self):
        """ Сравнение, когда нормы определены в виде
        'не более определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] <= self.norm, self.result[1] <= self.norm)
        else:
            self.conclusion = self.result <= self.norm

    def compare(self):
        """ Выполнение операции сравнения в зависимости от типа сравнения. """
        comparison_methods = {
            ComparTypes.WITHIN.name: self.compare_within,
            ComparTypes.UP_TO.name: self.compare_up_to,
            ComparTypes.NOT_ALLOWED.name: self.compare_not_allowed,
            ComparTypes.AT_LEAST.name: self.compare_at_least,
            ComparTypes.NO_MORE.name: self.compare_no_more,
            ComparTypes.DIGIT.name: self.compare_no_more,
            ComparTypes.NO_CHANGE.name: self.compare_no_more,
        }
        comparison_method = comparison_methods.get(self.comparison_type)
        if comparison_method:
            comparison_method()
        else:
            raise MethodOfComparisonError(self.comparison_type)


def create_conformity_conclusion(result: str, norm: str) -> bool | list[bool]:
    """ Функция для сравнения результатов исследования с нормой.
     Возвращает либо bool если значение результат исследования одно число,
     и list[bool] если значение результата исследования имеет погрешность
     в виде '±' """

    comparator = Comparator(result, norm)
    comparator.compare()
    return comparator.conclusion