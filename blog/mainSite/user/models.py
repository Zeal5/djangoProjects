from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Type(models.TextChoices):
        MODERATOR = "MD", "Mod"
        WRITER = "WR", "Writer"

    role = models.CharField(max_length=2, choices=Type.choices, default=Type.WRITER)
