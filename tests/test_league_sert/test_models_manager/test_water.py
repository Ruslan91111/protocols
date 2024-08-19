import pytest

from league_sert.models import Water
from league_sert.models_creator import create_water


@pytest.fixture(scope='function')
def test_data():
    """ Вернуть тестовые данные. """
    return {'Шифр пробы': '2890-1', 'Объект исследований': 'Вода питьевая. Комната принятия пищи',
            'indicators': [{
                'Споры сульфитредуцирующих клостридий, число спор в 20 см³': {
                    'result': 'Не обнаружены',
                    'norm': 'Отсутствие',
                    'norm_doc': 'МУК 4.2.3963-23/МУК 4.2.1018-01',
                    'conformity_main': True},
                'violations_of_norms': (
                    False, False)}]}


def test_create_main_protocol(test_data):
    """ Протестировать создание модели основных данных. """
    object_of_model = create_water(test_data)
    assert isinstance(object_of_model, Water)
    assert object_of_model.test_object == test_data['Объект исследований']
    assert object_of_model.sample_code == test_data['Шифр пробы']
    assert object_of_model.indic == test_data['indicators']
    assert object_of_model.violat_main == test_data['indicators'][0]['violations_of_norms'][0]
    assert object_of_model.violat_dev == test_data['indicators'][0]['violations_of_norms'][1]
