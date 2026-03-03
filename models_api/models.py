from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ModelAuthor(models.Model):
    id: int
    name = models.CharField(max_length=200)
    bio = models.TextField()
    contact_info = models.EmailField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self) -> str:
        return self.name
