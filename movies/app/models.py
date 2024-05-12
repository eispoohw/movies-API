from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Movie(models.Model):
    """Кинофильм"""

    id = models.IntegerField(primary_key=True)
    title = models.CharField(
        verbose_name="Название кинофильма", max_length=100, null=False, blank=False
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=False,
        blank=False,
    )
    director = models.CharField(
        verbose_name="ФИО режиссера", max_length=100, null=False, blank=False
    )
    length = models.CharField(
        verbose_name="Продолжительность фильма",
        max_length=8,
        null=False,
        blank=False,
        validators=[RegexValidator(regex=r"[0-9]{2}:[0-9]{2}:[0-9]{2}")],
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг фильма",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.title} ({self.year})"
