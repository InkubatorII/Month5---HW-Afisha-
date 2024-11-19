from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class User(AbstractUser):
    is_active = models.BooleanField(default=False)  # По умолчанию пользователь неактивен

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6, unique=True)

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999)}"

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

STARS = ((i, '* ' * i) for i in range(1, 6))

class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return f'Review for {self.movie.title}'
