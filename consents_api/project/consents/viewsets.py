from django.db.models import Q
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)

from consents.models import Consent
from consents.serializers import (
    CreateConsent,
    DetailConsent,
    ListConsent,
    UpdateConsent,
)


class ConsentsViewset(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Consent.objects.all()
    serializer_class = ListConsent

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ListConsent
            case "retrieve":
                return DetailConsent
            case "create":
                return CreateConsent
            case "update" | "partial_update":
                return UpdateConsent
            case _:
                return self.serializer_class

    def get_queryset(self):
        query_params = self.request.query_params

        special = {
            "dataset": "dataset__owner__address",
            "algorithm": "algorithm__owner__address",
        }

        query = Q()
        for param, value in query_params.items():
            if param in special:
                query |= Q(**{special[param]: value})
            else:
                query |= Q(**{param: value})

        return self.queryset.filter(query).order_by("-created_at")
