from datetime import timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from helpers.services.aquarius import aquarius
from django.utils import timezone


class ConsentsUserManager(UserManager):
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

    objects = UserManager()
    helper = ConsentsUserManager()


class WalletNonce(models.Model):
    """Stores one active nonce per wallet address. Also store the metadata required to reconstruct the SIWE-style message"""

    class Meta:
        db_table = "wallet_nonces"
        indexes = [models.Index(fields=["expires_at"])]

    address = models.CharField(max_length=255, unique=True, db_index=True)
    nonce = models.CharField(max_length=255)
    chain_id = models.PositiveIntegerField(default=1)
    domain = models.CharField(max_length=255)
    uri = models.TextField()
    issued_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at
