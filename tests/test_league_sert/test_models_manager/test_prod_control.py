import pytest

from league_sert.models import MainProtocol, ManufProd, ProdControl
from league_sert.models_creator import create_main_protocol, create_common_violations, create_prod_control


@pytest.fixture(scope='module')
def test_data():
    """ Вернуть тестовые данные. """
    return {
        'number_of_protocol': '4218/24-Д',
        'date_of_protocol': '07 мая 2024',
        'act': '4218 ОТ 02.05.2024',
        'place_of_measurement': 'Ленинградская обл., г. Гатчина, '
                                'ул. Куприна, д.48А, лит. А, магазин № 47109',
        'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                            'уровни шума и общей вибрации соответствуют требованиям',
        'indicators': [
            {
                'Отдел «Овощи/фрукты», рабочее место работника торгового зала(Па)': {
                    'parameter': 'Относительная влажность воздуха'
                                 'Относительная влажность воздуха', 'unit': '%',
                    'result': '41,1±3,0',
                    'norm': '15-75', 'conformity_main': True, 'conformity_deviation': True},
                'violations_of_norms': (False, False)
            }
        ]
    }


def test_create_prod_control(test_data):
    """ Протестировать создание модели ProdControl - контроля производства. """
    object_of_model = create_prod_control(**test_data)
    assert isinstance(object_of_model, ProdControl)
    assert object_of_model.number == test_data['number_of_protocol']
    assert object_of_model.date == test_data['date_of_protocol']
    assert object_of_model.act == test_data['act']
    assert object_of_model.conclusion == test_data['inner_conclusion']
    assert object_of_model.conclusion_compl == True
    assert object_of_model.indic == test_data['indicators']
    assert object_of_model.violat_main == test_data['indicators'][0]['violations_of_norms'][0]
    assert object_of_model.violat_dev == test_data['indicators'][0]['violations_of_norms'][1]

