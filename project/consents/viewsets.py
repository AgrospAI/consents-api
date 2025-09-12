from django.db import transaction
from django.db.models import Q
from helpers.permissions.consent import ConsentPermissions
from helpers.permissions.consent_response import ConsentResponsePermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from consents.models import Consent, ConsentResponse
from consents.serializers import (
    CreateConsent,
    CreateConsentResponse,
    DetailConsent,
    DetailConsentResponse,
    ListConsent,
)


class ConsentsViewset(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Consent.objects.all()
    serializer_class = ListConsent
    permission_classes = (ConsentPermissions,)

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ListConsent
            case "retrieve":
                return DetailConsent
            case "create":
                return CreateConsent
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

    @action(detail=True, methods=["delete"], url_path="delete-response")
    def delete_response(self, *args, **kwargs):
        instance = self.get_object()

        query = ConsentResponse.objects.filter(consent=instance)
        if query.exists():
            query.first().delete()
            return Response(status=status.HTTP_200_OK)
        return Response("No response found", status=status.HTTP_404_NOT_FOUND)


class ConsentResponseViewset(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = ConsentResponse.objects.all()
    serializer_class = DetailConsentResponse
    permission_classes = (ConsentResponsePermissions,)

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CreateConsentResponse
        return DetailConsentResponse

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            codes = exc.get_codes().values()
            detail = exc.detail

            if "forbidden" in codes:
                return Response({"detail": detail}, status=status.HTTP_403_FORBIDDEN)

            if "already_exists" in codes:
                return Response({"detail": detail}, status=status.HTTP_409_CONFLICT)

            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

        response_serializer = ListConsent(
            instance.consent, context={"request": request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
