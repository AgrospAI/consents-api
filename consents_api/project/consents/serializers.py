from assets.models import Asset
from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.models.utils import get_or_create
from helpers.services.aquarius import aquarius
from helpers.validators.DidLengthValidator import DidLengthValidator
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    FloatField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer,
)
from users.serializers import UserSerializer

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
    created_at = FloatField(source="timestamp")

    class Meta:
        model = Consent
        fields = (
            "id",
            "url",
            "reason",
            "dataset",
            "algorithm",
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
    solicitor = UserSerializer()
    created_at = FloatField(source="timestamp")

    class Meta:
        model = Consent
        fields = (
            "id",
            "created_at",
            "dataset",
            "algorithm",
            "solicitor",
        )


class CreateConsent(ModelSerializer):
    dataset = CharField(validators=[DidLengthValidator()])
    algorithm = CharField(validators=[DidLengthValidator()])

    class Meta:
        model = Consent
        fields = (
            "reason",
            "dataset",
            "algorithm",
            "solicitor",
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
            {"address": self.context["request"].user.address},
            {"address": self.context["request"].user.address},
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


class UpdateConsent(ModelSerializer):
    status = ChoiceField(
        choices=Status.choices,
        source="get_status_display",
    )

    permitted = BooleanField(default=False)

    class Meta:
        model = Consent
        fields = (
            "status",
            "reason",
            "permitted",
        )

    def update(self, instance, validated_data):
        assert not instance.response, "Consent already has been response"

        ConsentResponse.objects.create(
            consent=instance,
            status=validated_data["status"],
            reason=validated_data["reason"],
        )

        print(f"Consent {instance.id} updated to {validated_data['status']}")

        return super().update(instance, validated_data)
