""" Исключения для пакета data_preparation. """


class MyException(Exception):
    """Базовое исключение для всех исключений, связанных с приложением."""
    pass


class TypeOfIndicatorTableError(MyException):
    """Исключение, возникающее при неверном вводе пользователя."""

    def __init__(self, message='Не определен тип таблицы показателей, '
                               'невозможно в дальнейшем сравнить и сохранить результаты.'):
        self.message = message
        super().__init__(self.message)


class NoneConformityError(MyException):
    """Если в результате сравнения вывод None"""
    def __init__(self, result, norm):
        self.message = (f'В результате вычисления соответствия результата нормам произошла ошибка. '
                   f'result - {result}, norm - {norm}')
        super().__init__(self.message)


class TypeViolationsError(MyException):
    """Исключение, возникающее при неверном вводе пользователя."""
    def __init__(self, violations, norm):
        self.message = (f'У сформированного вывода для всей таблицы неверный тип данных '
                   f'violations - {violations}, тип данных - {type(violations)}')
        super().__init__(self.message)
        