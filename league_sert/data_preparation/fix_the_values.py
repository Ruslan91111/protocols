import re


def process_value(value):
    # Исправить неточности, допущенные при конвертировании файла
    value = value.strip('. \t')
    # Replace common misinterpretations
    replacements = [
        (r'l', '1'),
        (r'[хx]Ю', 'х10'),
        (r"[OО][']", '0'),
        (r'\d+б|б.\d+', '6'),
        (r'I.O', '1.0'),
        (r'lO|1O', '10'),

        (r'\bн[сc]\b', 'не '),

        (r'\b[нпли][ес] более', 'не более'),
        (r'\b[нпли][ес] допускаю\s*[тг]\s*[се]я', 'не допускаются'),
        (r'([нлпияВ][есо]|tie) обнару(ж|ок)[ес]н[оы]', 'не обнаружено'),

        (r'^о\s*[тг]\s*сутствие$', 'отсутствие'),
        (r'^[“\s]*[-—]\s*$|^[•\*]\s*$|^$', '-'),
        (r'з\s*а\s*п\s*а\s*х\s*', 'запах'),
        (r'в\s*к\s*у\s*с', 'вкус'),
        (r'не более 0.0\$', 'не более 0.03'),
        (r'не менее 0.0\$', 'не менее 0.03'),
        (r'\s{2,}', ' ')
    ]

    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement,  value, flags=re.IGNORECASE)

    # Handle specific character replacements
    if re.search(r'\d\s?[•■*xх]\s?\d', value, flags=re.IGNORECASE):
        value = re.sub(r'[•■xх]', 'x', value, flags=re.IGNORECASE)
    return value

