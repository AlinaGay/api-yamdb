from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_year

MAX_LENGTH_50 = 50
MAX_LENGTH_256 = 256
MIN_VALUE_1 = 1
MAX_VALUE_10 = 10


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
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class NamedSlugModel(models.Model):
    name = models.CharField(verbose_name='Наименование',
                            max_length=MAX_LENGTH_256)
    slug = models.CharField(verbose_name='URL slug',
                            unique=True, max_length=MAX_LENGTH_50)

    class Meta:
        abstract = True
        ordering = ['name', 'slug']

    def __str__(self):
        return self.name


class Category(NamedSlugModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NamedSlugModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(verbose_name='Наименование',
                            max_length=MAX_LENGTH_256)
    year = models.SmallIntegerField(verbose_name='Год',
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
        ordering = ['-year']


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              blank=True, null=True)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(MIN_VALUE_1),
        MaxValueValidator(MAX_VALUE_10)
    ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('-pub_date', '-score')
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_per_title_and_author'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комметарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
