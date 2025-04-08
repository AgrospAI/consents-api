from django.contrib.auth import get_user_model
from django.db import transaction
from helpers.services.aquarius import aquarius
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    FloatField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from consents.models import Asset, Consent, ConsentHistory
from consents.validators import DidLengthValidator

User = get_user_model()


class ListAsset(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="assets-detail")

    class Meta:
        model = Asset
        fields = ("url",)


class DetailAsset(ModelSerializer):
    owner = CharField(source="owner.address")

    class Meta:
        model = Asset
        fields = (
            "did",
            "owner",
        )


class ListConsentHistory(ModelSerializer):
    state = CharField(source="get_state_display")
    updated_at = FloatField(source="timestamp")

    class Meta:
        model = ConsentHistory
        fields = (
            "state",
            "updated_at",
        )


class ListConsent(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="consents-detail")

    dataset = DetailAsset()
    algorithm = DetailAsset()
    state = CharField(source="get_state_display")
    created_at = FloatField(source="timestamp")

    class Meta:
        model = Consent
        fields = (
            "id",
            "url",
            "state",
            "reason",
            "dataset",
            "algorithm",
            "created_at",
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
        )

    def to_representation(self, instance):
        return ListConsent(instance).data

    @transaction.atomic  # Ensure that the whole DB transaction is atomic. If any operation fails ROLLBACK.
    def create(self, validated_data):
        """
        Create the instances of the given asset, owner and solicitor if they do not exist.
        """

        def get_or_create(cls, get_kwargs, create_kwargs=None):
            try:
                return cls.objects.get(**get_kwargs)
            except cls.DoesNotExist:
                kwargs = create_kwargs if create_kwargs else get_kwargs
                return cls.objects.create(**kwargs)

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

        # Get/Create the consent instance
        consent_instance = get_or_create(
            Consent,
            {
                "dataset": data_instance,
                "algorithm": algo_instance,
            },
            {
                "dataset": data_instance,
                "algorithm": algo_instance,
                **validated_data,
            },
        )

        return consent_instance


class UpdateConsent(ModelSerializer):
    state = ChoiceField(
        choices=Consent.States.choices,
        source="get_state_display",
    )

    class Meta:
        model = Consent
        fields = ("state",)

    def update(self, instance, validated_data):
        # Create a new ConsentHistory instance with the changes
        ConsentHistory.objects.create(
            consent=instance,
            state=validated_data["state"],
        )

        print(f"Consent {instance.id} updated to {validated_data['state']}")

        return super().update(instance, validated_data)
