from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_description="List the registered assets.",
        operation_summary="List the registered assets. The registration process is automatic upon consent creation.",
        responses={
            200: openapi.Response(
                description="List of assets",
                schema=ListAsset(),
                examples={
                    "application/json": [
                        {
                            "url": "http://localhost:8050/api/assets/did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997/",
                            "did": "did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997",
                            "owner": "0xDf7a37EA1f42588Ea219Ec19328757F67BaBCeCD",
                            "type": "Dataset",
                            "chain_id": 32457,
                        },
                        {
                            "url": "http://localhost:8050/api/assets/did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a/",
                            "did": "did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a",
                            "owner": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                            "type": "Algorithm",
                            "chain_id": 32457,
                        },
                    ]
                },
            )
        },
        tags=["Asset"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List the registered assets.",
        operation_summary="List the registered assets. The registration process is automatic upon consent creation.",
        responses={
            200: openapi.Response(
                description="List of assets",
                schema=DetailAsset(),
                examples={
                    "application/json": {
                        "did": "did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997",
                        "owner": "0xDf7a37EA1f42588Ea219Ec19328757F67BaBCeCD",
                        "type": "Dataset",
                        "pending_consents": 1,
                        "chain_id": 32457,
                    }
                },
            ),
            404: openapi.Response(
                description="Detailed asset",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {"detail": "No Asset matches the given query."}
                },
            ),
        },
        tags=["Asset"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
