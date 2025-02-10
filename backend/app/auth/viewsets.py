import utils
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet

from . import serializers, models


class LoginViewset(CreateModelMixin, GenericViewSet):
    queryset = models.Web3User.objects.all()
    serializer_class = serializers.Web3UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):

        # Web3 login logic here

        username = request.data.get("username")
        # password = request.data.get("password")
        public_key = request.data.get("public_key")

        return models.Web3User.objects.filter(username=username, public_key=public_key).first()


class AuthenticateViewset(CreateModelMixin, GenericViewSet):

    @csrf_exempt
    def create(self, request, *args, **kwargs):

        address = request.data.get("address")
        signature = request.data.get("signature")
        message = request.data.get("message")

        # Verify the signature
        if utils.verify_signature(address, signature, message):
            # If the signature is valid, log in the user
            user, is_created = models.Web3User.objects.get_or_create(address=address)
            login(user)
            return Response(
                {"message": f"Authenticated as {user.address}"},
                status=HTTP_201_CREATED if is_created else HTTP_200_OK,
            )

        return Response({"message": "Invalid signature"}, status=HTTP_400_BAD_REQUEST)
