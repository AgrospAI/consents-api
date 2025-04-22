from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.validators.DidLengthValidator import DidLengthValidator

User = get_user_model()


class AssetManager(models.Manager):
    def get_pending_consents(self, asset) -> int:
        match asset.type:
            case Asset.Types.DATASET:
                return Asset.objects.get(id=asset.id).incoming_consents.count()
            case Asset.Types.ALGORITHM:
                return Asset.objects.get(id=asset.id).outgoing_consents.count()
        return -1

    def get_or_create(self, did: str, type: str) -> "Asset":
        asset = self.filter(did=did)
        if asset.exists():
            asset = asset.first()
            if asset.type != type:
                raise ValueError(
                    f"Asset with DID {did} already exists with type {asset.type}, expected {type}."
                )
            return asset

        # Create the owner instance
        owner = User.helper.get_or_create_from_aquarius(did)
        return self.create(did=did, owner=owner, type=type)


class Asset(models.Model):
    class Types(models.TextChoices):
        DATASET = "D", _("Dataset")
        ALGORITHM = "A", _("Algorithm")

    class Meta:
        db_table = "asset"
        indexes = [
            models.Index(fields=["did", "owner"]),
        ]

    did = models.CharField(
        max_length=255,
        unique=True,
        validators=[DidLengthValidator()],
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assets",
    )
    type = models.CharField(
        max_length=1,
        choices=Types.choices,
        default=Types.DATASET,
    )

    objects = models.Manager()
    helper = AssetManager()

    def __str__(self):
        return self.did
