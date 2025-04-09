from consents.models import Consent
from consents.serializers import ListConsent
from django.contrib.auth import get_user_model
from rest_framework import mixins, response, viewsets
from rest_framework.decorators import action

from . import models, serializers

User = get_user_model()


class UsersViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.ConsentsUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "address"

    @action(detail=True, methods=["get"])
    def incoming(self, *args, **kwargs):
        user = self.get_object()
        consents = Consent.pending.from_dataset_owner(user)

        serializer = ListConsent(consents, many=True, context={"request": self.request})
        return response.Response(serializer.data)

    @action(detail=True, methods=["get"])
    def outgoing(self, *args, **kwargs):
        user = self.get_object()
        consents = Consent.pending.from_algorithm_owner(user)

        serializer = ListConsent(consents, many=True, context={"request": self.request})
        return response.Response(serializer.data)
