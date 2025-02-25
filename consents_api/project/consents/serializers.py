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
    state = serializers.SerializerMethodField()

    class Meta:
        model = models.Consent
        fields = ("id", "reason", "state", "asset", "owner", "solicitor")

    def get_state(self, obj):
        return obj.get_state_display()


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

        def get_or_create(cls, get_kwargs, create_kwargs=None):
            try:
                return cls.objects.get(**get_kwargs)
            except cls.DoesNotExist:
                kwargs = create_kwargs if create_kwargs else get_kwargs
                return cls.objects.create(**kwargs)

        owner_address = validated_data.pop("owner")
        solicitor_address = validated_data.pop("solicitor")

        # Get/Create the owner and solicitor instances
        owner_instance = get_or_create(
            User,
            {"address": owner_address},
            {"address": owner_address, "username": f"user_{owner_address}"},
        )
        solicitor_instance = get_or_create(
            User,
            {"address": solicitor_address},
            {"address": solicitor_address, "username": f"user_{solicitor_address}"},
        )

        # TODO: Remove owner from the fields list, since the asset should be linked to the user
        #       And it should be retrieved from the blockchain
        # Get/Create the asset instance (Temporal solution)
        asset_did = validated_data.pop("asset")
        asset_instance = get_or_create(
            models.Asset,
            {"did": asset_did},
            {"did": asset_did, "owner": owner_instance},
        )

        # Get/Create the consent instance
        consent_instance = get_or_create(
            models.Consent,
            {
                "asset": asset_instance,
                "owner": owner_instance,
                "solicitor": solicitor_instance,
            },
            {
                "asset": asset_instance,
                "owner": owner_instance,
                "solicitor": solicitor_instance,
                **validated_data,
            },
        )

        return consent_instance


class UpdateConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consent
        fields = ("state",)
