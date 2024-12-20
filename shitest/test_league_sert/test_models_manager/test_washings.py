import datetime

import pytest

from league_sert.models.models import Washings
from league_sert.models.models_creator import create_washings


@pytest.fixture(scope='module')
def test_data():
    """ Вернуть тестовые данные. """
    return {'name_indic': 'БГКП', 'result': 'Не обнаружено', 'norm': '-',
            'norm_doc_of_method': '-', 'conformity_main': True}


def test_create_washings(test_data):
    """ Протестировать создание модели основных данных. """
    object_of_model = create_washings(**test_data)
    assert isinstance(object_of_model, Washings)
    assert object_of_model.name_indic == test_data['name_indic']
    assert object_of_model.result == test_data['result']
    assert object_of_model.norm == test_data['norm']
    assert object_of_model.conformity_main == test_data['conformity_main']
    assert object_of_model.conformity_deviation == True
