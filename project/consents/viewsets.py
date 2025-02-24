from rest_framework import mixins, viewsets

from consents import models, serializers


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

    def perform_create(self, serializer):
        serializer.save(solicitor=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateConsentSerializer

        if self.action in ["update", "partial_update"]:
            return serializers.UpdateConsentSerializer

        return serializers.ConsentSerializer
