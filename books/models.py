from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        SOFT = "1", "SOFT"
        HARD = "2", "HARD"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(choices=Cover.choices, max_length=2)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"
