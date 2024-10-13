from random import choice, randint

from settings import LENGTH_SHORT, STRING_CHARACTERS

from .models import URLMap


def get_sort_substring(min_length_short=LENGTH_SHORT,
                       max_length_short=LENGTH_SHORT,
                       string_characters=STRING_CHARACTERS):
    """Генератор случайный подстроки.

    Принимает три аргумента: целые числа минимальной и максимальной
    длины генерируемой подстроки, а также строку используемых символов.
    """
    if max_length_short < min_length_short:
        min_length_short, max_length_short = max_length_short, min_length_short
    length_short = randint(min_length_short, max_length_short)
    pass_list = [choice(string_characters) for _ in range(length_short)]
    return ''.join(pass_list)


def get_sort_link():
    """Генератор id короткой ссылки."""
    while True:
        short = get_sort_substring()
        if URLMap.filter_short(short) is None:
            break
    return short
