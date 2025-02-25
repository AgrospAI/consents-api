from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    incoming_consents = serializers.SerializerMethodField()
    outgoing_consents = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "address",
            "incoming_consents",
            "outgoing_consents",
        )

    def get_incoming_consents(self, obj):
        return obj.incoming_consents.count()

    def get_outgoing_consents(self, obj):
        return obj.outgoing_consents.count()


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("address",)

    def create(self, validated_data):
        instance, _ = User.objects.get_or_create(**validated_data)
        return instance
