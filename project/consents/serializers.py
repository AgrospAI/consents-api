from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.bitfields import get_mask
from helpers.fields.BitField import BitFieldSerializer
from helpers.validators.BitFieldMarked import BitFieldMarked
from helpers.validators.DidLengthValidator import DidLengthValidator
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
)
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from users.serializers import ListUserSerializer

from consents.models import Consent, ConsentResponse, Status

User = get_user_model()


class DetailConsentResponse(ModelSerializer):
    consent = HyperlinkedRelatedField(
        view_name="consents-detail",
        lookup_field="pk",
        read_only=True,
    )

    status = CharField(source="get_status_display")

    permitted = BitFieldSerializer()

    status = CharField(source="get_status_display")

    last_updated_at = IntegerField(source="timestamp")

    class Meta:
        model = ConsentResponse
        fields = (
            "consent",
            "status",
            "reason",
            "permitted",
            "status",
            "last_updated_at",
        )


class ListConsent(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="consents-detail")
    dataset = HyperlinkedRelatedField(
        view_name="assets-detail",
        lookup_field="did",
        read_only=True,
    )
    algorithm = HyperlinkedRelatedField(
        view_name="assets-detail",
        lookup_field="did",
        read_only=True,
    )
    solicitor = ListUserSerializer()
    created_at = IntegerField(source="timestamp")
    request = BitFieldSerializer()
    response = DetailConsentResponse()
    status = CharField()
    direction = SerializerMethodField()

    class Meta:
        model = Consent
        fields = (
            "url",
            "id",
            "created_at",
            "dataset",
            "algorithm",
            "solicitor",
            "reason",
            "request",
            "response",
            "status",
            "direction",
        )

    def get_direction(self, obj) -> str:
        if "direction" in self.context:
            return str(self.context.get("direction")).capitalize()
        return "-"


class DetailConsent(ModelSerializer):
    dataset = HyperlinkedRelatedField(
        view_name="assets-detail",
        lookup_field="did",
        read_only=True,
    )
    algorithm = HyperlinkedRelatedField(
        view_name="assets-detail",
        lookup_field="did",
        read_only=True,
    )
    solicitor = ListUserSerializer()
    created_at = IntegerField(source="timestamp")
    request = BitFieldSerializer()
    response = NestedHyperlinkedRelatedField(
        view_name="consent-response-detail",
        parent_lookup_kwargs={
            "consent_pk": "consent__pk",
        },
        read_only=True,
    )
    status = CharField(source="response.get_status_display")

    class Meta:
        model = Consent
        fields = (
            "id",
            "created_at",
            "dataset",
            "algorithm",
            "solicitor",
            "reason",
            "request",
            "response",
            "status",
        )


class CreateConsent(ModelSerializer):
    dataset = CharField(validators=[DidLengthValidator()])
    algorithm = CharField(validators=[DidLengthValidator()])
    request = BitFieldSerializer()
    reason = CharField(required=False)

    class Meta:
        model = Consent
        fields = (
            "reason",
            "dataset",
            "algorithm",
            "request",
        )

    def to_representation(self, instance):
        representation = DetailConsent(
            instance,
            context={"request": self.context.get("request")},
        ).data
        return representation

    @transaction.atomic  # Ensure that the whole DB transaction is atomic. If any operation fails ROLLBACK.
    def create(self, validated_data):
        # TODO: Before creating the consent, check if the permissions asked for is already granted in aquarius.
        solicitor = self.context["request"].user.address
        return Consent.helper.get_or_create_from_aquarius(
            dataset=validated_data.pop("dataset"),
            algorithm=validated_data.pop("algorithm"),
            solicitor=solicitor,
            **validated_data,
        )


class CreateConsentResponse(NestedHyperlinkedModelSerializer):
    permitted = BitFieldSerializer()
    reason = CharField(required=False, allow_blank=True)

    class Meta:
        model = ConsentResponse
        fields = (
            "reason",
            "permitted",
        )

    def create(self, validated_data):
        # Get the consent instance from the context
        consent_pk = self.context["view"].kwargs["consent_pk"]
        consent_instance = Consent.objects.select_related(
            "dataset", "dataset__owner"
        ).get(pk=consent_pk)

        # Ownership check
        request_user = self.context["request"].user
        if consent_instance.dataset.owner != request_user:
            raise ValidationError(
                "You are not the owner of the dataset",
                code="forbidden",
            )

        # Already responded check
        if hasattr(consent_instance, "response"):
            raise ValidationError(
                "Consent already has been responded to",
                code="already_exists",
            )

        # Validate that the permitted field response has been requested
        permitted_mask = get_mask(validated_data["permitted"], Consent)
        BitFieldMarked(consent_instance.request)(permitted_mask)

        validated_data["permitted"] = permitted_mask
        validated_data["status"] = Status.from_bitfields(
            get_mask(consent_instance.request, Consent),
            get_mask(permitted_mask, Consent),
        )

        # Attach the consent instance
        validated_data["consent"] = consent_instance

        return super().create(validated_data)
