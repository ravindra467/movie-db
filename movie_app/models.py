from enum import unique
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    year_published = models.IntegerField()
    imdbId = models.CharField(max_length=100, unique=True)
    imdbRating = models.DecimalField(max_digits= 10, decimal_places = 2)
