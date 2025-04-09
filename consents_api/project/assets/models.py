from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.validators.DidLengthValidator import DidLengthValidator

User = get_user_model()


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

    def __str__(self):
        return self.did
