from rest_framework.viewsets import ReadOnlyModelViewSet

from assets.models import Asset
from assets.serializers import DetailAsset, ListAsset


class AssetsViewset(ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = ListAsset
    lookup_field = "did"
    lookup_url_kwarg = "did"

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ListAsset
            case "retrieve":
                return DetailAsset
            case _:
                return self.serializer_class
