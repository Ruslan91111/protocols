""" Тестирование м"""
import pytest

from compare_results_and_norms import compare_res_and_norms


def test_find_violations_of_value():
    assert compare_res_and_norms('<0,01', 'не допускаются') is True
    assert compare_res_and_norms('<0,11', 'не допускаются') is False
    assert compare_res_and_norms('0', 'не допускаются') is True
    assert compare_res_and_norms('не обнаружено', 'не допускаются') is True
    assert compare_res_and_norms('не более 0,2', 'не допускаются') is False
    assert compare_res_and_norms('не более 0,02', 'не допускаются') is True
    assert compare_res_and_norms('0,185±0,055', 'не более 0,35') is True
    assert compare_res_and_norms('<0,02', 'не более 0,015') is False
    assert compare_res_and_norms('0,2', 'не более 0,015') is False
    assert compare_res_and_norms('0,185±0,055', 'не более 0,015') is False
    assert compare_res_and_norms('не более 0,20', 'не более 0,15') is False
    assert compare_res_and_norms('0', 'не более 0,15') is True
    assert compare_res_and_norms('<0,01', 'отсутствие') is True
    assert compare_res_and_norms('<0,11', 'отсутствие') is False
    assert compare_res_and_norms('0', 'отсутствие') is True
    assert compare_res_and_norms('не обнаружено', 'отсутствие') is True
    assert compare_res_and_norms('не более 0,2', 'отсутствие') is False
    assert compare_res_and_norms('не более 0,02', 'отсутствие') is True


if __name__ == "__main__":
    pytest.main()
