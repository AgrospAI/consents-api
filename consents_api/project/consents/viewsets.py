from rest_framework import mixins, viewsets

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

    # TODO: Make an instance of the consent history
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)
