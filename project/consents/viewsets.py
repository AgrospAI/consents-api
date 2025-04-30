from django.db.models import Q
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
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

    def perform_create(self, serializer):
        # Check if the consent already has been responded to

        assert True
        return super().perform_create(serializer)
        # serializer

        # try:
        #     # Weird thing to do
        #     instance.response
        #     raise ValueError("Consent already has been responded to")
        # # except Asset.RelatedObjectDoesNotExist:
        # except Exception:
        #     pass

        # ConsentResponse.objects.create(
        #     consent=instance,
        #     status=validated_data["status"],
        #     permitted=validated_data["permitted"],
        #     reason=validated_data.get("reason", None),
        # )

        # print(f"Consent {instance.id} updated to {validated_data['status']}")

        # return super().update(instance, validated_data)

    # @action(detail=True, methods=["post"])
    # def respond(self, *args, **kwargs):
    #     """
    #     Respond to a consent request. This action is only available for the user that created the consent.
    #     """

    #     instance = self.get_object()

    #     # Check if the consent already has been responded to
    #     try:
    #         instance.response
    #         raise ValueError("Consent already has been responded to")
    #     except Consent.RelatedObjectDoesNotExist:
    #         pass

    #     serializer = self.get_serializer(instance, data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return self.get_response(serializer.data)


class ConsentResponseViewset(
    CreateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = ConsentResponse.objects.all()
    serializer_class = DetailConsentResponse

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CreateConsentResponse
        return DetailConsentResponse
