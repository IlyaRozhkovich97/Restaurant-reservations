import random

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*!&$#?=@'
"""
Константа `CHARS` содержит набор символов, которые могут использоваться для генерации случайных токенов и паролей.

Символы включают:
- Нижний регистр: a-z
- Верхний регистр: A-Z
- Цифры: 0-9
- Специальные символы: +-* ! & $ # ? = @
"""


def generate_token(length=10):
    """
    Генерирует случайный токен заданной длины.

    Параметры:
    - length (int, optional): Длина токена. Значение по умолчанию - 10.

    Возвращает:
    - str: Случайный токен, состоящий из символов, указанных в `CHARS`.

    Примеры:
    >>> generate_token()
    'aB3cD5eF7g'

    >>> generate_token(15)
    'a1b2C3d4E5f6G7h8I9j0'
    """
    return ''.join(random.choice(CHARS) for _ in range(length))


def generate_password(length=10):
    """
    Генерирует случайный пароль заданной длины.

    Параметры:
    - length (int, optional): Длина пароля. Значение по умолчанию - 10.

    Возвращает:
    - str: Случайный пароль, состоящий из символов, указанных в `CHARS`.

    Примеры:
    >>> generate_password()
    'aB3cD5eF7g'

    >>> generate_password(12)
    '1A2b3C4d5E6f7G8h'
    """
    return ''.join(random.choice(CHARS) for _ in range(length))
