from assets.models import Asset
from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.fields.BitField import BitFieldSerializer
from helpers.models.utils import get_or_create
from helpers.services.aquarius import aquarius
from helpers.validators.DidLengthValidator import DidLengthValidator
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    FloatField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer,
)

from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
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

    class Meta:
        model = Consent
        fields = (
            "url",
            "reason",
            "dataset",
            "algorithm",
            "solicitor",
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
    created_at = FloatField(source="timestamp")
    request = BitFieldSerializer()
    response = NestedHyperlinkedRelatedField(
        view_name="consent-responses-detail",
        parent_lookup_kwargs={
            "consent_pk": "pk",
        },
        read_only=True,
    )

    class Meta:
        model = Consent
        fields = (
            "id",
            "created_at",
            "dataset",
            "algorithm",
            "solicitor",
            "request",
            "response",
        )


class CreateConsent(ModelSerializer):
    dataset = CharField(validators=[DidLengthValidator()])
    algorithm = CharField(validators=[DidLengthValidator()])
    request = BitFieldSerializer()

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
        """
        Create the instances of the given asset, owner and solicitor if they do not exist.
        """

        dataset_did = validated_data.pop("dataset")
        algorithm_did = validated_data.pop("algorithm")
        solicitor = validated_data.pop("solicitor")

        # Retrieve dataset owner and algorithm owner from the blockchain
        data_owner_address = aquarius.get_asset_owner(dataset_did)
        algo_owner_address = aquarius.get_asset_owner(algorithm_did)

        # Get/Create the owner and solicitor instances
        dataset_owner_instance = get_or_create(
            User,
            {"address": data_owner_address},
            {"address": data_owner_address, "username": f"user_{data_owner_address}"},
        )
        algorithm_owner_instance = get_or_create(
            User,
            {"address": algo_owner_address},
            {"address": algo_owner_address, "username": f"user_{algo_owner_address}"},
        )
        solicitor_instance = get_or_create(
            User,
            {"address": solicitor},
            {"address": solicitor, "username": f"user_{solicitor}"},
        )

        data_instance = get_or_create(
            Asset,
            {"did": dataset_did},
            {
                "did": dataset_did,
                "owner": dataset_owner_instance,
                "type": Asset.Types.DATASET,
            },
        )

        algo_instance = get_or_create(
            Asset,
            {"did": algorithm_did},
            {
                "did": algorithm_did,
                "owner": algorithm_owner_instance,
                "type": Asset.Types.ALGORITHM,
            },
        )

        # TODO: Before creating the consent, check if the permissions asked for already exist
        # Get/Create the consent instance
        consent_instance = get_or_create(
            Consent,
            {
                "dataset": data_instance,
                "algorithm": algo_instance,
                "solicitor": solicitor_instance,
            },
            {
                "dataset": data_instance,
                "algorithm": algo_instance,
                "solicitor": solicitor_instance,
                **validated_data,
            },
        )

        return consent_instance


class DetailConsentResponse(ModelSerializer):
    consent = HyperlinkedRelatedField(
        view_name="consents-detail",
        lookup_field="pk",
        read_only=True,
    )

    status = CharField(source="get_status_display")

    permitted = BitFieldSerializer()

    last_updated_at = FloatField(source="timestamp")

    class Meta:
        model = ConsentResponse
        fields = (
            "consent",
            "status",
            "reason",
            "permitted",
            "last_updated_at",
        )


class CreateConsentResponse(NestedHyperlinkedModelSerializer):
    status = ChoiceField(choices=Status.choices)

    permitted = BitFieldSerializer()

    reason = CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = ConsentResponse
        fields = (
            "status",
            "reason",
            "permitted",
        )

    def save(self, *args, **kwargs):
        consent_pk = self.context["view"].kwargs["consent_pk"]
        kwargs["consent"] = Consent.objects.get(pk=consent_pk)
        return super().save(*args, **kwargs)
