from consents.models import Consent
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ListUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="users-detail",
        lookup_field="address",
    )

    address = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "url",
            "address",
        )


class DetailUserSerializer(serializers.ModelSerializer):
    incoming_pending_consents = serializers.SerializerMethodField()
    outgoing_pending_consents = serializers.SerializerMethodField()
    assets = serializers.HyperlinkedIdentityField(
        view_name="assets-detail",
        lookup_field="did",
        many=True,
    )

    class Meta:
        model = User
        fields = (
            "address",
            "assets",
            "incoming_pending_consents",
            "outgoing_pending_consents",
        )

    # Retrieve incoming/pending consents according to the user ownership of the asset
    def get_incoming_pending_consents(self, obj):
        return Consent.helper.from_dataset_owner(obj, pending_only=True).count()

    def get_outgoing_pending_consents(self, obj):
        return Consent.helper.from_algorithm_owner(obj, pending_only=True).count()
