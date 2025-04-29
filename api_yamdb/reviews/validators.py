import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError('Год должен быть меньше или равен текущему')
