from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from consents.models import Asset, Consent
from consents.serializers import (
    AssetSerializer,
    ConsentSerializer,
    GetOrCreateConsentSerializer,
    OverallConsentHistorySerializer,
    UpdateConsentSerializer,
)


class AssetsViewset(ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    lookup_field = "did"


class ConsentsViewset(ModelViewSet):
    queryset = Consent.objects.all()
    serializer_class = ConsentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return GetOrCreateConsentSerializer

        if self.action in ["update", "partial_update"]:
            return UpdateConsentSerializer

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

    @action(detail=True, methods=["get"])
    def history(self, *args, **kwargs):
        consent = self.get_object()

        history = consent.history.all().order_by("-updated_at")
        serializer = OverallConsentHistorySerializer(history, many=True)
        return Response(serializer.data)
