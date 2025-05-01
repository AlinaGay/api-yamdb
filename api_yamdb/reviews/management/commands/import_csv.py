import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файлов в базу данных'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'static', 'data')

        def load_csv(file_name):
            path = os.path.join(data_dir, file_name)
            with open(path, newline='', encoding='utf-8') as f:
                return list(csv.DictReader(f))

        def safe_int(value, default=0):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        # Users
        for row in load_csv('users.csv'):
            try:
                User.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row.get('bio', ''),
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                    }
                )
            except IntegrityError as e:
                self.stderr.write(f"[User] Ошибка: {e}")

        # Categories
        for row in load_csv('category.csv'):
            try:
                Category.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
            except IntegrityError as e:
                self.stderr.write(f"[Category] Ошибка: {e}")

        # Genres
        for row in load_csv('genre.csv'):
            try:
                Genre.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
            except IntegrityError as e:
                self.stderr.write(f"[Genre] Ошибка: {e}")

        # Titles
        for row in load_csv('titles.csv'):
            try:
                category = Category.objects.get(id=int(row['category']))
                Title.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'year': safe_int(row['year']),
                        'category': category
                    }
                )
            except Category.DoesNotExist:
                self.stderr.write(f"[Title] Категория с id={row['category']} не найдена")
            except IntegrityError as e:
                self.stderr.write(f"[Title] Ошибка: {e}")

        # GenreTitle (M2M)
        for row in load_csv('genre_title.csv'):
            try:
                title = Title.objects.get(id=int(row['title_id']))
                genre = Genre.objects.get(id=int(row['genre_id']))
                title.genre.add(genre)
            except (Title.DoesNotExist, Genre.DoesNotExist) as e:
                self.stderr.write(f"[GenreTitle] Ошибка: {e}")

        # Reviews
        for row in load_csv('review.csv'):
            try:
                title = Title.objects.get(id=int(row['title_id']))
                author = User.objects.get(id=int(row['author']))
                Review.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'title': title,
                        'text': row['text'],
                        'author': author,
                        'score': safe_int(row['score']),
                        'pub_date': row['pub_date']
                    }
                )
            except (Title.DoesNotExist, User.DoesNotExist) as e:
                self.stderr.write(f"[Review] Ошибка: {e}")
            except IntegrityError as e:
                self.stderr.write(f"[Review] Ошибка: {e}")

        # Comments
        for row in load_csv('comments.csv'):
            try:
                review = Review.objects.get(id=int(row['review_id']))
                author = User.objects.get(id=int(row['author']))
                Comment.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'review': review,
                        'text': row['text'],
                        'author': author,
                        'pub_date': row['pub_date']
                    }
                )
            except (Review.DoesNotExist, User.DoesNotExist) as e:
                self.stderr.write(f"[Comment] Ошибка: {e}")
            except IntegrityError as e:
                self.stderr.write(f"[Comment] Ошибка: {e}")

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы.'))
