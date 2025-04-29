from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.fields.BitField import BitFieldSerializer
from helpers.validators.BitFieldMarked import BitFieldMarked
from helpers.validators.DidLengthValidator import DidLengthValidator
from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    IntegerField,
    ModelSerializer,
)
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from users.serializers import ListUserSerializer

from consents.models import Consent, ConsentResponse, Status

User = get_user_model()


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
    solicitor = CharField(
        source="solicitor.address",
    )
    request = BitFieldSerializer()
    created_at = IntegerField(source="timestamp")
    status = CharField(source="response.get_status_display")

    class Meta:
        model = Consent
        fields = (
            "url",
            "reason",
            "dataset",
            "algorithm",
            "solicitor",
            "request",
            "status",
            "created_at",
        )


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
            "consent_pk": "pk",
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
    solicitor = CharField()

    class Meta:
        model = Consent
        fields = (
            "reason",
            "dataset",
            "algorithm",
            "solicitor",
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
        return Consent.helper.get_or_create_from_aquarius(
            dataset=validated_data.pop("dataset"),
            algorithm=validated_data.pop("algorithm"),
            solicitor=validated_data.pop("solicitor"),
            **validated_data,
        )


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


class CreateConsentResponse(NestedHyperlinkedModelSerializer):
    # TODO: Only allow the asset owner to create a response

    permitted = BitFieldSerializer()

    reason = CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = ConsentResponse
        fields = (
            "reason",
            "permitted",
        )

    def save(self, *args, **kwargs):
        consent_pk = self.context["view"].kwargs["consent_pk"]
        kwargs["consent"] = Consent.objects.get(pk=consent_pk)
        return super().save(*args, **kwargs)

    def create(self, validated_data):
        # Get the consent instance from the context
        consent_pk = self.context["view"].kwargs["consent_pk"]
        consent_instance = Consent.objects.get(pk=consent_pk)

        # Check if the consent already has been responded to
        assert not hasattr(consent_instance, "response"), (
            "Consent already has been responded to"
        )

        # Validate that the permitted field response has been requested
        BitFieldMarked(consent_instance.request)(validated_data["permitted"])

        validated_data["status"] = Status.from_bitfields(
            int(consent_instance.request),
            int(validated_data["permitted"]),
        )

        return super().create(validated_data)
