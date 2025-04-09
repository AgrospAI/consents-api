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

from assets.models import Asset
from consents.models import Consent, Status
from helpers.validators.DidLengthValidator import DidLengthValidator

User = get_user_model()


class ListConsent(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="consents-detail")

    dataset = HyperlinkedIdentityField(
        view_name="assets-detail",
        lookup_field="did",
        source="dataset.did",
    )
    algorithm = HyperlinkedIdentityField(
        view_name="assets-detail",
        lookup_field="did",
        source="algorithm.did",
    )
    status = CharField(source="get_status_display")
    created_at = FloatField(source="timestamp")

    class Meta:
        model = Consent
        fields = (
            "id",
            "url",
            "status",
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
        representation = ListConsent(
            instance, context={"request": self.context.get("request")}
        ).data
        return representation

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
    status = ChoiceField(
        choices=Status.choices,
        source="get_status_display",
    )

    class Meta:
        model = Consent
        fields = ("status",)

    def update(self, instance, validated_data):
        # Create a new ConsentHistory instance with the changes
        # ConsentHistory.objects.create(
        #     consent=instance,
        #     status=validated_data["status"],
        # )

        print(f"Consent {instance.id} updated to {validated_data['status']}")

        return super().update(instance, validated_data)


class DetailConsent(ModelSerializer):
    class Meta:
        model = Consent
        fields = "__all__"
