# api_yamdb
api_yamdb

The **YaMDb** project collects user reviews on works of art: books, movies, and music.

## Description

The **YaMDb API** allows you to:

- Retrieve lists of works, genres, and categories
- View ratings and reviews from other users
- Write reviews and give ratings
- Comment on reviews
- Restrict user permissions by roles: user, moderator, administrator

## Technologies

- Python 3.12
- Django 3.2+
- Django REST Framework
- SQLite (default)
- JWT authentication

## Project Launch

1. Clone the repository and navigate to it in the command line:
```bash
git clone https://github.com/AlinaGay/api-final-yatube.git
cd yatube_api
```
2. Create and activate a virtual environment:
```
python3 -m venv env
source env/bin/activate
```
3. Install dependencies:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Apply migrations and start the server:
```
python manage.py migrate
python manage.py runserver
```
5. (Optional) Import test data:
```
python manage.py import_csv

```
6. Project Structure:

- /api_yamdb/ — Django configuration
- /api/ — routers, views, serializers
- /reviews/ — main application with models and API
- /static/data/ — CSV files for database import

Author

[AlinaGay](https://github.com/AlinaGay)
| Backend Developer • Python Engineer |
