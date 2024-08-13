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


def determine_names_of_tables(tables: Tables) -> Tables:
    """ Определить тип таблицы исходя из ее содержимого.
    Под типом понимается к какой модели она относится.
    Тип таблицы - сохраняется в строке, под вторым индексом в ключе. """

    result = {}

    for key, value in tables.items():
        if key[1] in {'MAIN', 'PROD_CONTROL'}:
            result[key] = value
            continue

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
            object_of_test = object_of_test.replace(',', '',).replace(' ', '')
            if 'Воздух' in object_of_test:
                result[(key[0], 'air')] = value
                continue
            if 'Вода' in object_of_test:
                result[(key[0], 'water')] = value
            if 'Смывы' in object_of_test:
                result[(key[0], 'washings')] = value

    return result


def refine_and_merge_tables(tables: Tables) -> Tables:
    """ Завершить обработку таблиц, объединяя, удаляя ненужные,
    и определяя тип таблиц. """
    tables = join_sample_and_results(tables)
    tables = remove_results_table(tables)
    tables = determine_names_of_tables(tables)
    return tables
