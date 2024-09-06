# Используем базовый образ Python
FROM python:3

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл зависимостей в контейнер
COPY ./requirements.txt /code/

# Устанавливаем зависимости проекта
RUN pip install -r requirements.txt

# Копируем все остальные файлы проекта
COPY . .
