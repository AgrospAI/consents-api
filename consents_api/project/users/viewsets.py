from typing import Literal
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
    serializer_class = serializers.ListUserSerializer
    lookup_field = "address"
    lookup_url_kwarg = "address"

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return serializers.DetailUserSerializer
        return serializers.ListUserSerializer

    def _actions(
        self,
        way: Literal["incoming", "outgoing", "solicited"],
        pending_only: bool = False,
    ):
        user = self.get_object()
        match way:
            case "incoming":
                consents = Consent.helper.from_dataset_owner(
                    user, pending_only=pending_only
                )
            case "outgoing":
                consents = Consent.helper.from_algorithm_owner(
                    user, pending_only=pending_only
                )
            case "solicited":
                consents = Consent.helper.from_solicitor(
                    user, pending_only=pending_only
                )

        serializer = ListConsent(consents, many=True, context={"request": self.request})
        return response.Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="pending-incoming")
    def pending_incoming(self, *args, **kwargs):
        return self._actions("incoming", pending_only=True)

    @action(detail=True, methods=["get"], url_path="pending-outgoing")
    def pending_outgoing(self, *args, **kwargs):
        return self._actions("outgoing", pending_only=True)

    @action(detail=True, methods=["get"], url_path="pending-solicited")
    def pending_solicited(self, *args, **kwargs):
        return self._actions("solicited", pending_only=True)

    @action(detail=True, methods=["get"])
    def incoming(self, *args, **kwargs):
        return self._actions("incoming")

    @action(detail=True, methods=["get"])
    def outgoing(self, *args, **kwargs):
        return self._actions("outgoing")

    @action(detail=True, methods=["get"])
    def solicited(self, *args, **kwargs):
        return self._actions("solicited")
