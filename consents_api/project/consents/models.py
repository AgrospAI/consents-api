from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints

User = get_user_model()


class Consent(models.Model):
    class States(models.TextChoices):
        ACTIVE = "A", "Active"
        PENDING = "P", "Pending"
        INACTIVE = "I", "Inactive"
        REJECTED = "R", "Rejected"
        DELETED = "D", "Deleted"

    class Meta:
        db_table = "consent"
        constraints = [
            constraints.UniqueConstraint(
                fields=["solicitor", "asset_did"],
                name="unique_consent",
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]

    asset_did = models.CharField(max_length=255)
    reason = models.TextField()
    state = models.CharField(
        max_length=1,
        choices=States.choices,
        default=States.PENDING,
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
