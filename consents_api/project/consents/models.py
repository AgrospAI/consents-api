from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints

from consents.validators import DidLengthValidator

User = get_user_model()


class Asset(models.Model):
    class Types(models.TextChoices):
        DATASET = "D", "Dataset"
        ALGORITHM = "A", "Algorithm"

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


class Consent(models.Model):
    class States(models.TextChoices):
        ACCEPTED = "A", "Accepted"
        PENDING = "P", "Pending"
        REJECTED = "R", "Rejected"
        DELETED = "D", "Deleted"

    class Meta:
        db_table = "consent"
        constraints = [
            constraints.UniqueConstraint(
                fields=["algorithm", "dataset"],
                name="unique_algorithm_dataset",
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]

    reason = models.TextField()
    dataset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="incoming_consents",
        validators=[DidLengthValidator()],
    )
    algorithm = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="outgoing_consents",
        validators=[DidLengthValidator()],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=1,
        choices=States.choices,
        default=States.PENDING,
    )

    def __str__(self):
        return f"{self.solicitor} -> {self.asset} ({self.state})"

    @property
    def timestamp(self) -> float:
        return self.created_at.timestamp()


class ConsentHistory(models.Model):
    class Meta:
        db_table = "consents_history"
        verbose_name_plural = "consents history"

    consent = models.ForeignKey(
        Consent,
        on_delete=models.CASCADE,
        related_name="history",
    )
    state = models.CharField(
        max_length=1,
        choices=Consent.States.choices,
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consent} ({self.state})"

    @property
    def timestamp(self) -> float:
        return self.updated_at.timestamp()
