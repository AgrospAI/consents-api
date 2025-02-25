from consents.models import Consent
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    incoming_pending_consents = serializers.SerializerMethodField()
    outgoing_pending_consents = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("address", "incoming_pending_consents", "outgoing_pending_consents")

    def get_incoming_pending_consents(self, obj):
        return obj.incoming_consents.filter(state=Consent.States.PENDING).count()

    def get_outgoing_pending_consents(self, obj):
        return obj.outgoing_consents.filter(state=Consent.States.PENDING).count()
