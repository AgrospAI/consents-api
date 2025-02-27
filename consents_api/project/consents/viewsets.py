from rest_framework import mixins, viewsets
from django.db.models import Q

from . import models, serializers


class AssetsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializer


class ConsentsViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Consent.objects.all()
    serializer_class = serializers.ConsentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.GetOrCreateConsentSerializer

        if self.action in ["update", "partial_update"]:
            return serializers.UpdateConsentSerializer

        return self.serializer_class

    def get_queryset(self):
        query_params = self.request.query_params

        special = {
            "asset": "asset__did",
            "owner": "owner__address",
            "solicitor": "solicitor__address",
        }

        query = Q()
        for param, value in query_params.items():
            if param in special:
                query |= Q(**{special[param]: value})
            else:
                query |= Q(**{param: value})

        return self.queryset.filter(query).order_by("-created_at")

    # TODO: Make an instance of the consent history
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)
