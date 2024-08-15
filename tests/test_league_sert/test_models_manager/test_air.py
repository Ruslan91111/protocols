import pytest

from league_sert.models import Air
from league_sert.models_manager import create_air, create_manuf_prod


@pytest.fixture(scope='module')
def test_data():
    """ Вернуть тестовые данные. """
    return {'Шифр пробы': '2890-2', 'indicators': [
            {
                'Холодильная камера «Молочные продукты»': {
                    'result': '0',
                    'norm': '-',
                    'norm_doc': 'СП 4695-88',
                    'conformity_main': True},
                'Холодильная камера«Молочные продукты»': {
                    'result': '0',
                    'norm': '-',
                    'norm_doc': 'СП 4695-88',
                    'conformity_main': True},
                'violations_of_norms': (
                    False, False)}]}


def test_create_air(test_data):
    """ Протестировать создание модели основных данных. """
    object_of_model = create_air(test_data)
    assert isinstance(object_of_model, Air)
    assert object_of_model.sample_code == test_data['Шифр пробы']
    assert object_of_model.indic == test_data['indicators']
    assert object_of_model.indic_compl == test_data['indicators'][0]['violations_of_norms']
    assert isinstance(object_of_model.indic_compl, tuple)
