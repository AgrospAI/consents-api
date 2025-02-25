from django.contrib.auth.models import AbstractUser
from django.db import models


class ConsentsUser(AbstractUser):
    class Meta:
        db_table = "users"

    address = models.CharField(max_length=80, unique=True)
