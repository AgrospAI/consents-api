from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "signature",
#             "address",
#         ]

#     signature = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
