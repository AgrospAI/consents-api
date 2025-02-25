from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from consents.models import Consent


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = "__all__"


class CreateConsentSerializer(WritableNestedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Consent
        fields = ["asset_did", "reason", "state", "owner"]

    # TODO: Remove owner from the fields list, since the asset_did should be linked to the user
    # TODO: Create asset model on consent creation
    # TODO: Create ALL needed user models on consent creation


class UpdateConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = ["state"]
