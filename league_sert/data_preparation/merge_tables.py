"""
Модуль для финальной обработки данных из таблиц.

Код добавляет таблицы показателей в соответствующую таблицу образцов,
удаляет лишние данные, определяет тип таблицы и прописывает его в ключе таблицы.

Функции:

    - join_sample_and_results:
        Объединить таблицы образцов(SAMPLE) с таблицами результатов(RESULTS).
        Следующие за таблицей образцов таблицы результатов добавить в поле
        indicators таблицы SAMPLE.

    - remove_results_table:
        Удалить таблицы с результатами исследований(RESULTS)

    - determine_names_of_tables:
        Определить тип таблицы исходя из ее содержимого.
        Под типом понимается к какой модели она относится.
        Тип таблицы - сохраняется в строке, под вторым индексом в ключе.

    - refine_and_merge_tables:
        Завершить обработку таблиц, объединяя, удаляя ненужные,
        и определяя тип таблиц.

"""
import re

from league_sert.models.models_creator import fix_keys

Tables = dict[tuple[int, str]: dict[str]]


def join_sample_and_results(tables: Tables) -> Tables:
    """ Объединить таблицы образцов(SAMPLE) с таблицами результатов(RESULTS).
    Следующие за таблицей образцов таблицы результатов добавить в поле
    indicators таблицы SAMPLE. """

    names_of_tabs = list(tables.keys())
    cur_tab = 0

    while cur_tab < (len(names_of_tabs)):
        # Если ключ таблицы с "SAMPLE" - код шифра.
        if names_of_tabs[cur_tab][1] == 'SAMPLE':
            # Инициализируем поле 'indicators' для текущей 'SAMPLE' таблицы.
            tables[names_of_tabs[cur_tab]]['indicators'] = []
            # Проходим по всем последующим таблицам, пока они являются 'RESULTS'.
            next_table = cur_tab + 1
            while next_table < len(names_of_tabs) and names_of_tabs[next_table][1] == 'RESULTS':
                # Добавляем значения из текущей 'RESULTS' в 'SAMPLE'.
                tables[names_of_tabs[cur_tab]]['indicators'].append(
                    tables[names_of_tabs[next_table]])
                next_table += 1
            # Устанавливаем индекс текущей таблицы на первую не 'RESULTS' таблицу 'SAMPLE'.
            cur_tab = next_table
        else:
            cur_tab += 1
    return tables


def remove_results_table(tables: Tables) -> Tables:
    """ Удалить таблицы с результатами исследований. """
    tables = {name: value for name, value in tables.items() if name[1] != 'RESULTS'}
    return tables


FIX_KEYS_MANUF_PROD = {'Группа продукции':
                           (r'г\s*р\s*у\s*п\s*п\s*а\s*п\s*р\s*о\s*д\s*у\s*к\s*ц\s*и\s*и\s*'),
                       'Объект исследования':
                           (r'о\s*б\s*ъ\s*е\s*к\s*т\s*и\s*с\s*с\s*л\s*е\s*д\s*о\s*в\s*а\s*н\s*и\s*й\s*')}

FIX_KEYS_OBJECT = {'air': r'В\s*о\s*з\s*д\s*у\s*х',
                   'washings': r'С\s*м\s*ы\s*в\s*ы',
                   'water': r'В\s*о\s*д\s*а',}


def determine_names_of_tables(tables: Tables) -> Tables:
    """ Определить тип таблицы исходя из ее содержимого.
    Под типом понимается к какой модели она относится.
    Тип таблицы - сохраняется в строке, под вторым индексом в ключе. """

    result = {}

    for key, value in tables.items():

        if key[1] in {'MAIN', 'PROD_CONTROL'}:
            result[key] = value
            continue

        value = fix_keys(value, FIX_KEYS_MANUF_PROD)

        manuf_prod = value.get('Группа продукции', False)
        if manuf_prod == 'Продукция производителя':
            result[(key[0], 'manuf_prod')] = value
            continue

        if manuf_prod == 'Производство магазина':
            result[(key[0], 'store_prod')] = value
            continue

        object_of_test = value.get('Объект исследования', False)
        if not object_of_test:
            object_of_test = value.get('Объект исследований', False)

        if object_of_test:

            object_of_test = object_of_test.replace(',', '', ).replace(' ', '')

            for k, v in FIX_KEYS_OBJECT.items():
                if re.search(v, object_of_test, re.IGNORECASE):
                    result[(key[0], k)] = value
                    break

    return result


def refine_and_merge_tables(tables: Tables) -> Tables:
    """ Завершить обработку таблиц, объединяя, удаляя ненужные,
    и определяя тип таблиц. """
    tables = join_sample_and_results(tables)
    tables = remove_results_table(tables)
    tables = determine_names_of_tables(tables)
    return tables
