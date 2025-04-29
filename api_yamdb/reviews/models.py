from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True)


class Category(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=256)
    slug = models.CharField(verbose_name='URL slug', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=256)
    slug = models.CharField(verbose_name='URL slug', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=256)
    year = models.PositiveSmallIntegerField(verbose_name='Год',
                                            validators=[validate_year],
                                            db_index=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   through_fields=('title', 'genre'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='titles')
    description = models.TextField(verbose_name='Описание', blank=True,
                                   null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              blank=True, null=True)
