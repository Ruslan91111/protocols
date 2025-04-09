class MissedTableError(Exception):
    def __init__(self, table_numb, prev_table_name):
        table_numb += 1
        self.msg = (f'Не определен тип таблицы. Проверьте в таблице №{table_numb},'
                    f' после таблицы с <{prev_table_name}>. '
                    f'Проверьте написание Группы продукции или Объект исследования.')

        super().__init__(self.msg)


class MissedKeyCreateInstError(Exception):
    def __init__(self, cls_obj, key):
        self.msg = (f'В таблице с {cls_obj}'
                    f' отсутствует ключ <{key}>. '
                    f'Проверьте написание ключа в таблице в word файле.')
        super().__init__(self.msg)
