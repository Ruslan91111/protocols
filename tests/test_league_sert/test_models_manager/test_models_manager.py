import pytest

from league_sert.models.models import MainProtocol, ProdControl, ManufProd, Air
from league_sert.models.models_creator import create_common_violations, create_all_objects

data_proc_viol = {'indicators': [{'violations_of_norms': (True, True)},
                                 {'violations_of_norms': (False, True)},
                                 {'violations_of_norms': (False, False)}]}
data_proc_viol_not_list = {'indicators': [{'violations_of_norms': (False, False)}]}


@pytest.mark.parametrize('data, expected', [
    (data_proc_viol, [True, True]),
    (data_proc_viol_not_list, [False, False])])
def test_process_violations(data, expected):
    """ Проверить выдачу общего для всего образца вывода
    о нарушении результатов исследования нормам. """
    result = create_common_violations(data)
    assert result == expected


def test_create_all_objects(main_collector):
    """ Тестирование создание из данных, собранных MainCollector набора
    объектов моделей. """

    objects = create_all_objects(main_collector)
    assert len(objects) == 7
    assert isinstance(objects, dict)
    assert isinstance(objects[(0, 'MAIN')], MainProtocol)
    assert isinstance(objects[(1, 'manuf_prod')], list)
    assert isinstance(objects[(1, 'manuf_prod')][0], ManufProd)
    assert len(objects[(1, 'manuf_prod')]) == 7
    assert isinstance(objects[(10, 'air')], list)
    assert isinstance(objects[(10, 'air')][0], Air)
    assert len(objects[(10, 'air')]) == 1
    assert isinstance(objects[(13, 'PROD_CONTROL')], list)
    assert isinstance(objects[(13, 'PROD_CONTROL')][0], ProdControl)
    assert len(objects[(13, 'PROD_CONTROL')]) == 3
