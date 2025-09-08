from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.bitfields import get_mask
from helpers.fields.BitField import BitFieldSerializer
from helpers.validators.BitFieldMarked import BitFieldMarked
from helpers.validators.DidLengthValidator import DidLengthValidator
from rest_framework import status
from rest_framework.serializers import (
    SerializerMethodField,
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    IntegerField,
    ModelSerializer,
)
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.exceptions import ValidationError
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
    # response = NestedHyperlinkedRelatedField(
    #     view_name="consent-response-detail",
    #     parent_lookup_kwargs={
    #         "consent_pk": "consent__pk",
    #     },
    #     read_only=True,
    # )
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

    def save(self, *args, **kwargs):
        consent_pk = self.context["view"].kwargs["consent_pk"]
        kwargs["consent"] = Consent.objects.get(pk=consent_pk)
        return super().save(*args, **kwargs)

    def create(self, validated_data):
        # Get the consent instance from the context
        consent_pk = self.context["view"].kwargs["consent_pk"]
        consent_instance = Consent.objects.get(pk=consent_pk)

        request_address = self.context["request"].user.address
        dataset_owner_address = consent_instance.dataset.owner.address
        if str(request_address) != str(dataset_owner_address):
            raise ValidationError(
                f"Unauthorized: wallet {request_address} is not owner of dataset {dataset_owner_address}",
                status.HTTP_403_FORBIDDEN,
            )

        # Check if the consent already has been responded to
        if hasattr(consent_instance, "response"):
            raise ValidationError(
                "Consent already has been responded to", status.HTTP_400_BAD_REQUEST
            )

        permitted_mask = get_mask(validated_data["permitted"], Consent)

        # Validate that the permitted field response has been requested
        BitFieldMarked(consent_instance.request)(permitted_mask)

        validated_data["permitted"] = permitted_mask
        validated_data["status"] = Status.from_bitfields(
            get_mask(consent_instance.request, Consent),
            get_mask(permitted_mask, Consent),
        )

        return super().create(validated_data)
