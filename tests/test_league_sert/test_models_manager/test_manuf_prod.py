import pytest

from league_sert.models import ManufProd
from league_sert.models_manager import create_manuf_prod


@pytest.fixture(scope='module')
def test_data():
    """ Вернуть тестовые данные. """
    return {'Шифр пробы': '2635-1', 'Группа продукции': 'Продукция производителя',
            'Наименование продукции': 'Консервы. Опята маринованные отборные',
            'Дата производства продукции': '14.12.2023 г. Срок годности 3 года',
            'Производитель (фирма, предприятие, организация)': 'ПК «Самобранка»',
            'Дата проведения исследований': '22.03.2024 г.-01.04.2024 г.',
            'indicators': [
                {
                'Внешний вид тары после термостатирования. Микроскопия консервированного продукта': {
                    'result': 'не изменен<10',
                    'norm': 'отсутствие дефектов не более 10 клеток м.о. в поле зрения',
                    'norm_doc': 'ГОСТ 26669-85',
                    'conformity_main': True},
                'violations_of_norms': (False, False)
            }
            ]}


def test_create_manuf_prod(test_data):
    """ Протестировать создание модели основных данных. """
    object_of_model = create_manuf_prod(test_data)
    assert isinstance(object_of_model, ManufProd)
    assert object_of_model.sample_code == test_data['Шифр пробы']
    assert object_of_model.prod_name == test_data['Наименование продукции']
    assert object_of_model.prod_date == test_data['Дата производства продукции']
    assert object_of_model.manuf == test_data['Производитель (фирма, предприятие, организация)']
    assert object_of_model.indic == test_data['indicators']
    assert object_of_model.indic_compl == test_data['indicators'][0]['violations_of_norms']
    assert isinstance(object_of_model.indic_compl, tuple)
