from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints

User = get_user_model()


class Asset(models.Model):
    class Meta:
        db_table = "asset"
        indexes = [
            models.Index(fields=["did", "owner"]),
        ]

    did = models.CharField(
        max_length=255,
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assets",
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
                fields=["solicitor", "asset"],
                name="unique_consent",
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]

    reason = models.TextField()
    state = models.CharField(
        max_length=1,
        choices=States.choices,
        default=States.PENDING,
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="consents",
    )
    solicitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="outgoing_consents",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incoming_consents",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.solicitor} -> {self.asset} ({self.state})"


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
