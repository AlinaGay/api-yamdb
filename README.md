# api_yamdb
api_yamdb

Проект YaMDb собирает отзывы пользователей на произведения искусства: книги, фильмы и музыку.

## Описание

API YaMDb позволяет:

- Получать список произведений, жанров и категорий
- Смотреть рейтинги и отзывы других пользователей
- Писать отзывы и ставить оценки
- Комментировать отзывы
- Ограничивать права пользователей по ролям: пользователь, модератор, администратор

## Технологии

- Python 3.12
- Django 3.2+
- Django REST Framework
- SQLite (по умолчанию)
- JWT аутентификация

## Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/AlinaGay/api-final-yatube.git
```
```bash
cd yatube_api
```

2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env
source env/bin/activate
```
3. Установите зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Выполните миграции и запустите сервер:
```bash
python manage.py migrate
python manage.py runserver
```

5. (Опционально) Импортируйте тестовые данные:
```bash
python manage.py import_csv
```

6. Структура проекта
/api_yamdb/ — конфигурация Django
/api/ - роутеры, вью, сериалайзеры
/reviews/ — основное приложение с моделями и API
/static/data/ — CSV-файлы для загрузки в базу

7. Автор

| [Alina Opolskaia](https://github.com/AlinaGay/) |
| Backend Developer • Python Engineer 
