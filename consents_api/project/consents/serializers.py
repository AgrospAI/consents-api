from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from . import models

User = get_user_model()


class AssetSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.address")

    class Meta:
        model = models.Asset
        fields = ("did", "owner")


class ConsentSerializer(serializers.ModelSerializer):
    asset = serializers.CharField(source="asset.did")
    owner = serializers.CharField(source="owner.address")
    solicitor = serializers.CharField(source="solicitor.address")

    class Meta:
        model = models.Consent
        fields = ("reason", "state", "asset", "owner", "solicitor")


class GetOrCreateConsentSerializer(serializers.ModelSerializer):
    # Identifiable attributes to retrieve/create the instances
    asset = serializers.CharField()
    solicitor = serializers.CharField()
    owner = serializers.CharField()

    class Meta:
        model = models.Consent
        fields = ("asset", "reason", "solicitor", "owner")

    @transaction.atomic  # Ensure that the whole DB transaction is atomic. If any operation fails ROLLBACK.
    def create(self, validated_data):
        """
        Create the instances of the given asset, owner and solicitor if they do not exist.
        """

        # Get/Create the owner and solicitor instances
        owner_instance, _ = User.objects.get_or_create(
            address=validated_data.pop("owner"),
        )
        solicitor_instance, _ = User.objects.get_or_create(
            address=validated_data.pop("solicitor"),
        )

        # TODO: Remove owner from the fields list, since the asset should be linked to the user
        #       And it should be retrieved from the blockchain
        # Get/Create the asset instance (Temporal solution)
        asset_did = validated_data.pop("asset")
        try:
            asset_instance = models.Asset.objects.get(did=asset_did)
        except models.Asset.DoesNotExist:
            asset_instance = models.Asset.objects.create(
                did=asset_did,
                owner=owner_instance,
            )

        return models.Consent.objects.create(
            asset=asset_instance,
            owner=owner_instance,
            solicitor=solicitor_instance,
            **validated_data,
        )


class UpdateConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consent
        fields = ("state",)
