from assets.models import Asset
from bitfield import BitField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import constraints
from django.utils.translation import gettext_lazy as _
from helpers.bitfields import get_mask

User = get_user_model()


class Status(models.TextChoices):
    ACCEPTED = "A", _("Accepted")
    PENDING = "P", _("Pending")
    DENIED = "D", _("Denied")
    RESOLVED = "R", _("Resolved")

    @staticmethod
    def from_bitfields(original: int, permitted: int) -> "Status":
        original = int(original)
        permitted = int(permitted)

        if original == permitted:
            return Status.ACCEPTED
        elif permitted == 0:
            return Status.DENIED
        else:
            return Status.RESOLVED


class RequestFlags:
    flags = (
        ("trusted_algorithm_publisher", _("Trusted Algorithm Publisher")),
        ("trusted_algorithm", _("Trusted Algorithm")),
        ("allow_network_access", _("Allow Network Access")),
    )


class HelperConsentsManager(models.Manager):
    def get_or_create(
        self,
        dataset: Asset,
        algorithm: Asset,
        solicitor_address: str,
        **kwargs,
    ) -> "Consent":
        consent = self.filter(
            dataset=dataset,
            algorithm=algorithm,
            solicitor__address=solicitor_address,
        )

        if consent.exists():
            return consent.first()

        solicitor = User.helper.get_or_create(solicitor_address)
        return self.create(
            dataset=dataset,
            algorithm=algorithm,
            solicitor=solicitor,
            **kwargs,
        )

    def get_or_create_from_aquarius(
        self,
        dataset: str,
        algorithm: str,
        solicitor: str,
        **kwargs,
    ) -> "Consent":
        # May have multiple request for same algorithm-dataset pair ????
        consent = self.filter(
            dataset__did=dataset,
            algorithm__did=algorithm,
            solicitor__address=solicitor,
        )

        if consent.exists():
            return consent.first()

        dataset = Asset.helper.get_or_create(dataset, Asset.Types.DATASET)
        algorithm = Asset.helper.get_or_create(algorithm, Asset.Types.ALGORITHM)
        solicitor_instance = User.helper.get_or_create(solicitor)

        request = get_mask(kwargs.pop("request"), Consent)

        return self.create(
            dataset=dataset,
            algorithm=algorithm,
            solicitor=solicitor_instance,
            request=request,
            **kwargs,
        )

    def pending(self):
        return super().get_queryset().filter(response__isnull=True)

    def from_dataset_owner(self, owner: str, pending_only=False):
        queryset = self.pending() if pending_only else self.all()
        return queryset.filter(dataset__owner=owner)

    def from_algorithm_owner(self, owner: str, pending_only=False):
        queryset = self.pending() if pending_only else self.all()
        return queryset.filter(algorithm__owner=owner)

    def from_solicitor(self, solicitor: str, pending_only=False):
        queryset = self.pending() if pending_only else self.all()
        return queryset.filter(solicitor=solicitor)


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

    # === Managers ===
    objects = models.Manager()
    helper = HelperConsentsManager()
    # ================

    reason = models.TextField(blank=True)

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
        return f"{self.solicitor} -> {self.dataset} & {self.algorithm} ({self.status})"

    @property
    def timestamp(self) -> float:
        return self.created_at.timestamp()

    @property
    def status(self) -> Status:
        query = ConsentResponse.objects.filter(consent=self)

        return (
            query.first().get_status_display()
            if query.exists()
            else Status.PENDING.label
        )


class ConsentResponse(models.Model):
    class Meta:
        db_table = "consent_response"
        verbose_name_plural = "consent responses"

    consent = models.OneToOneField(
        Consent,
        on_delete=models.CASCADE,
        related_name="response",
    )

    permitted = BitField(flags=RequestFlags.flags)

    reason = models.TextField()

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
        null=False,
    )

    last_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consent} ({self.status})"

    @property
    def timestamp(self) -> float:
        return self.last_updated_at.timestamp()
