class MyException(Exception):
    """Базовое исключение для всех исключений, связанных с приложением."""


class WrongNameOfTableError(MyException):
    """ Исключение, возникающее, когда не определен тип таблицы с показателями. """
    def __init__(self, message='Не установленный тип таблицы '
                               'при создании объектов моделей.'):
        self.message = message
        super().__init__(self.message)


class TypeIndicatorsError(MyException):
    """ Исключение, возникает, когда у показателей неверный тип данных. """
    def __init__(self, message='У значения показателей - неверный тип данных.'
                               'Требуемый тип - словарь'):
        self.message = message
        super().__init__(self.message)
