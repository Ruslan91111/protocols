import pytest

from league_sert.models import MainProtocol
from league_sert.models_manager import create_main_protocol


@pytest.fixture(scope='module')
def test_data():
    """ Вернуть тестовые данные. """
    main_number = '4225/24-Д'
    main_date = '23 мая 2024'
    table_data = {
        'Заявитель и его адрес (юридический и фактический)':
            'АО «ДИКСИ ЮГ», ИНН: 5036045205, МО, г. Подольск, ул. Юбилейная, д. 32 А; '
            'Ленинградская область, Тихвинский р-н, г. Тихвин, ул. Карла Маркса, '
            'д. 50, ал. В (№47116)',
        'Номер заявки и дата': '№8/24 от 10.01.2024 г.',
        'Место отбора проб': 'Ленинградская область, Тихвинский р-н, г. Тихвин, '
                             'ул. Карла Маркса, д. 50, ал. В (№47116)',
        'Дата и время отбора проб': '03.05.2024 г., 13 ч. 30 мин.',
        'Ф.И.О., должность сотрудника, производившего отбор проб':
            'Руденко Н.А., помощник с/врача',
        'Дата и время доставки проб в лабораторию': '03.05.2024 г., 18 ч. 00 мин.',
        'Сопроводительные документы': 'Акт отбора проб № 4371 от 03.05.2024 г.',
        'Количество зашифрованных проб': '3',
        'Протокол составлен в 2-х экземплярах': 'Протокол составлен в 2-х экземплярах'}

    return {'main_number': main_number,
            'main_date': main_date,
            'table_data': table_data}


def test_create_main_protocol(test_data):
    """ Протестировать создание модели основных данных. """
    object_model = create_main_protocol(**test_data)
    assert isinstance(object_model, MainProtocol)
    assert object_model.number == test_data['main_number']
    assert object_model.date == test_data['main_date']
    assert object_model.sampling_site == test_data['table_data']['Место отбора проб']
    assert object_model.sampling_date == test_data['table_data']['Дата и время отбора проб']