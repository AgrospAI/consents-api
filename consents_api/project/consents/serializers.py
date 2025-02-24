from rest_framework import serializers

from consents.models import Consent


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = "__all__"


class CreateConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = ["asset_did", "reason", "state", "owner"]

    # TODO: Remove owner from the fields list, since the asset_did should be linked to the user


class UpdateConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = ["state"]
