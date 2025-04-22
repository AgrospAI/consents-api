from django.contrib.auth.models import AbstractUser
from django.db import models
from helpers.services.aquarius import aquarius


class ConsentsUserManager(models.Manager):
    def get_or_create(self, address: str) -> "ConsentsUser":
        user = self.filter(address=address)
        if user.exists():
            return user.first()
        else:
            return self.create(address=address, username=f"user_{address}")

    def get_or_create_from_aquarius(self, did: str) -> "ConsentsUser":
        address = aquarius.get_asset_owner(did)
        return self.get_or_create(address=address)


class ConsentsUser(AbstractUser):
    class Meta:
        db_table = "users"

    address = models.CharField(max_length=80, unique=True)

    objects = models.Manager()
    helper = ConsentsUserManager()
