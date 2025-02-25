from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from . import models, serializers

User = get_user_model()


class UsersViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.ConsentsUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreationSerializer

        return self.serializer_class
