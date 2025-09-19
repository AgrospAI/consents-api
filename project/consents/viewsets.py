from django.db import transaction
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ConsentPermissions,
    )

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
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()

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

    @swagger_auto_schema(
        operation_summary="Lists the Consents",
        operation_description="List of Constents",
        responses={
            "200": openapi.Response(
                description="List of consents",
                schema=ListConsent,
                examples={
                    "application/json": {
                        "url": "http://localhost:8050/api/consents/1/",
                        "id": 1,
                        "created_at": 1758271130,
                        "dataset": "http://localhost:8050/api/assets/did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997/",
                        "algorithm": "http://localhost:8050/api/assets/did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a/",
                        "solicitor": {
                            "url": "http://localhost:8050/api/users/0xD999bAaE98AC5246568FD726be8832c49626867D/",
                            "address": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                        },
                        "reason": "nkjhk",
                        "request": {"trusted_algorithm": "true"},
                        "response": {
                            "consent": "http://localhost:8050/api/consents/1/",
                            "status": "Denied",
                            "reason": "asdsad",
                            "permitted": {},
                            "last_updated_at": 1758288980,
                        },
                        "status": "Denied",
                        "direction": "-",
                    }
                },
            ),
        },
        tags=["Consent Petition"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Consent by id",
        operation_description="Retrieve Consent by id",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                description="Consent ID",
                required=True,
                example=1,
            )
        ],
        responses={
            "200": openapi.Response(
                description="Detailed consent",
                schema=DetailConsent,
                examples={
                    "application/json": {
                        "id": 1,
                        "created_at": 1758271130,
                        "dataset": "http://localhost:8050/api/assets/did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997/",
                        "algorithm": "http://localhost:8050/api/assets/did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a/",
                        "solicitor": {
                            "url": "http://localhost:8050/api/users/0xD999bAaE98AC5246568FD726be8832c49626867D/",
                            "address": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                        },
                        "reason": "nkjhk",
                        "request": {"trusted_algorithm": "true"},
                        "response": "null",
                        "status": "null",
                    }
                },
            )
        },
        tags=["Consent Petition"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a Consent Petition instance",
        operation_description="Deletes a Consent Petition, requires being the solicitor.",
        responses={
            "201": openapi.Response(
                description="Created successfully",
                schema=DetailConsentResponse,
                examples={
                    "application/json": {
                        "id": 3,
                        "created_at": 1758291529,
                        "dataset": "http://localhost:8050/api/assets/did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997/",
                        "algorithm": "http://localhost:8050/api/assets/did:op:f0f0e7de07529aac4907a619c53dc6884ccb01cadd2666174216cd1a3f94f426/",
                        "solicitor": {
                            "url": "http://localhost:8050/api/users/0xD999bAaE98AC5246568FD726be8832c49626867D/",
                            "address": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                        },
                        "reason": "asdasd",
                        "request": {"trusted_algorithm": "true"},
                        "response": "null",
                        "status": "null",
                    }
                },
            ),
            "401": openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided"
                    }
                },
            ),
        },
        tags=["Consent Petition"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a Consent Petition",
        operation_description="Delete a Consent Petition. Must be authenticated and be the solicitor of the Consent Petition.",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                description="Consent's primary key",
                required=True,
                example=1,
            )
        ],
        responses={
            "204": openapi.Response(
                description="Consent Petititon deleted",
            ),
            "401": openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided",
                    }
                },
            ),
            "403": openapi.Response(
                description="Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "You can not perform this action",
                    }
                },
            ),
            "404": openapi.Response(
                description="Consent Petition not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Not Found",
                    }
                },
            ),
        },
        tags=["Consent Petition"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method="delete",
        operation_summary="Delete a consent petition response",
        operation_description="Delete a consent petition response. Must be authenticated and be the owner of the consent petition dataset",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Consent id",
                type=openapi.TYPE_NUMBER,
                required=True,
                example="1",
            ),
        ],
        responses={
            "204": openapi.Response(description="Deleted successfully"),
            "401": openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided"
                    }
                },
            ),
            "403": openapi.Response(
                description="Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "You do not have permissions to perform this action"
                    }
                },
            ),
            "404": openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "No ConsentResponse found for the given Consent id"
                    }
                },
            ),
        },
        tags=["Consent Petition Response"],
    )
    @action(detail=True, methods=["delete"], url_path="delete-response")
    def delete_response(self, *args, **kwargs):
        instance = self.get_object()

        query = ConsentResponse.objects.filter(consent=instance)
        if query.exists():
            query.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "No ConsentResponse found for the given Consent"},
            status=status.HTTP_404_NOT_FOUND,
        )


class ConsentResponseViewset(
    CreateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = ConsentResponse.objects.all()
    serializer_class = DetailConsentResponse
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ConsentResponsePermissions,
    )

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CreateConsentResponse
        return DetailConsentResponse

    @swagger_auto_schema(
        operation_summary="Retrieves a Consent Petition Response",
        operation_description="Gets the details of a Consent Petition Response",
        manual_parameters=[
            openapi.Parameter(
                "consent_pk",
                openapi.IN_PATH,
                description="The base consent primary key (id)",
                type=openapi.TYPE_NUMBER,
                required=True,
                example=1,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="The id of the Consent Petition object",
                type=openapi.TYPE_NUMBER,
                required=True,
                example=1,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="",
                schema=DetailConsentResponse,
                examples={
                    "application/json": {
                        "consent": "http://localhost:8050/api/consents/1/",
                        "status": "Denied",
                        "reason": "asdsad",
                        "permitted": {},
                        "last_updated_at": 1758288980,
                    }
                },
            ),
            "400": openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Bad request",
                    }
                },
            ),
            "404": openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
        tags=["Consent Petition Response"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Responds to a Consent Petition",
        operation_description="Creates a Consent Petition Response from the given consent_pk",
        manual_parameters=[
            openapi.Parameter(
                "consent_pk",
                openapi.IN_PATH,
                description="Primary key of the Consent Petition that we want to respond to",
                type=openapi.TYPE_NUMBER,
                required=True,
                example=1,
            ),
        ],
        request_body=CreateConsentResponse,
        responses={
            "203": openapi.Response(
                description="",
                schema=ListConsent,
            ),
            "400": openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Bad Request",
                    },
                },
            ),
            "401": openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided",
                    },
                },
            ),
            "403": openapi.Response(
                description="Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "You are not the owner of the dataset",
                    },
                },
            ),
            "409": openapi.Response(
                description="Consent has already been responded to",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "The consent has already been responded to",
                    },
                },
            ),
        },
        tags=["Consent Petition Response"],
    )
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
            instance.consent,
            context={"request": request},
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
