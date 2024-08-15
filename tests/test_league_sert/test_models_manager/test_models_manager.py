import pytest

from league_sert.models import MainProtocol, ProdControl, ManufProd, Air, Water
from league_sert.models_manager import process_violations, create_all_objects

data_proc_viol = {'indicators': [{'violations_of_norms': (True, True)},
                                 {'violations_of_norms': (False, True)},
                                 {'violations_of_norms': (False, False)}]}
data_proc_viol_not_list = {'indicators': [{'violations_of_norms': (False, False)}]}


@pytest.mark.parametrize('data, expected', [
    (data_proc_viol, (True, True)),
    (data_proc_viol_not_list, (False, False))])
def test_process_violations(data, expected):
    """ Проверить выдачу общего для всего образца вывода
    о нарушении результатов исследования нормам. """
    result = process_violations(data)
    assert result == expected


def test_create_all_objects(main_collector):
    """ Тестирование создание из данных, собранных MainCollector набора
    объектов моделей. """
    objects = create_all_objects(main_collector)
    assert len(objects) == 5
    objects_content = list(objects.items())
    assert isinstance(objects_content[0][1], MainProtocol)
    assert isinstance(objects_content[1][1], ManufProd)
    assert isinstance(objects_content[2][1], ManufProd)
    assert isinstance(objects_content[3][1], Air)
    assert isinstance(objects_content[4][1], ProdControl)


def test_create_all_objects(main_collector):
    """ Тестирование создание из данных, собранных MainCollector набора
    объектов моделей. """
    objects = create_all_objects(main_collector)
    assert len(objects) == 5
    objects_content = list(objects.items())
    assert isinstance(objects_content[0][1], MainProtocol)
    assert isinstance(objects_content[1][1], ManufProd)
    assert isinstance(objects_content[2][1], ManufProd)
    assert isinstance(objects_content[3][1], Air)
    assert isinstance(objects_content[4][1], ProdControl)
