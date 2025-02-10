from rest_framework import serializers

from . import models

class Web3UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Web3User
        fields = "__all__"
