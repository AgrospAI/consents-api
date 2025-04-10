from assets.models import Asset
from bitfield import BitField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Status(models.TextChoices):
    ACCEPTED = "A", _("Accepted")
    PENDING = "P", _("Pending")
    DENIED = "D", _("Denied")
    RESOLVED = "R", _("Resolved")


class RequestFlags:
    flags = (
        ("trusted_algorithm_publisher", _("Trusted Algorithm Publisher")),
        ("trusted_algorithm", _("Trusted Algorithm")),
        ("trusted_credential_address", _("Trusted Credential Address")),
        ("allow_network_access", _("Allow Network Access")),
    )


class PendingConsentsManager(models.Manager):
    def pending(self):
        return super().get_queryset().filter(response__isnull=False)

    def from_dataset_owner(self, owner):
        return self.pending().filter(dataset__owner=owner)

    def from_algorithm_owner(self, owner: str):
        return self.pending().filter(algorithm__owner=owner)


class Consent(models.Model):
    class Meta:
        db_table = "consent"
        constraints = [
            constraints.UniqueConstraint(
                fields=["algorithm", "dataset"],
                name="unique_algorithm_dataset",
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]

    objects = models.Manager()
    pending = PendingConsentsManager()

    reason = models.TextField()

    dataset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="incoming_consents",
    )

    algorithm = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="outgoing_consents",
    )

    solicitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="consents",
    )

    request = BitField(flags=RequestFlags.flags)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.solicitor} -> {self.dataset} & {self.algorithm} ({self.get_status_display})"

    @property
    def timestamp(self) -> float:
        return self.created_at.timestamp()

    @property
    def status(self) -> Status:
        query = ConsentResponse.objects.filter(consent=self)

        return query.first().status if query.exists() else Status.PENDING

    @property
    def get_status_display(self) -> str:
        return self.status.label


class ConsentResponse(models.Model):
    class Meta:
        db_table = "consent_response"
        verbose_name_plural = "consent responses"

    consent = models.OneToOneField(
        Consent,
        on_delete=models.CASCADE,
        related_name="response",
    )

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
    )

    permitted = BitField(flags=RequestFlags.flags)

    last_updated_at = models.DateTimeField(auto_now_add=True)

    reason = models.TextField()

    def __str__(self):
        return f"{self.consent} ({self.status})"

    @property
    def timestamp(self) -> float:
        return self.last_updated_at.timestamp()
