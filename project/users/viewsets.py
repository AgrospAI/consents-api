import secrets
from datetime import timedelta
from typing import Literal
from urllib.parse import ParseResult, urlparse

from consents.models import Consent
from consents.serializers import ListConsent
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_checksum_address
from helpers.auth import build_siwe_message
from rest_framework import mixins, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from . import models, serializers

User = get_user_model()


class UsersViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.ConsentsUser.objects.all()
    serializer_class = serializers.ListUserSerializer
    lookup_field = "address"
    lookup_url_kwarg = "address"

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return serializers.DetailUserSerializer
        return serializers.ListUserSerializer

    @swagger_auto_schema(
        operation_summary="Get the registered users",
        operation_description="Retrieves a list of the registered users and a details URL to fetch more data about them. The registration of the user is done automatically when a consent is created",
        responses={
            "200": openapi.Response(
                description="List of user's addresses and details URL",
                examples={
                    "application/json": [
                        {
                            "url": "http://localhost:8050/api/users/admin@admin/",
                            "address": "admin@admin",
                        },
                        {
                            "url": "http://localhost:8050/api/users/0xDf7a37EA1f42588Ea219Ec19328757F67BaBCeCD/",
                            "address": "0xDf7a37EA1f42588Ea219Ec19328757F67BaBCeCD",
                        },
                    ]
                },
            ),
        },
        tags=["User"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get the details of a user",
        operation_description="Retrieves a list of the registered users and a details URL to fetch more data about them.  The registration of the user is done automatically when a consent is created",
        responses={
            "200": openapi.Response(
                description="List of user's addresses and details URL",
                schema=serializers.ListUserSerializer,
                examples={
                    "application/json": {
                        "address": "0x1234567890abcdef1234567890abcdef12345678",
                        "assets": [
                            "http://localhost:8050/api/assets/did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a/"
                        ],
                        "incoming_pending_consents": "0",
                        "outgoing_pending_consents": "1",
                    }
                },
            ),
            "400": openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "No ConsentsUser matches the given query"
                    }
                },
            ),
        },
        tags=["User"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _actions(
        self,
        way: Literal["incoming", "outgoing"],
        pending_only: bool = False,
    ):
        user = self.get_object()
        match way:
            case "incoming":
                consents = Consent.helper.from_dataset_owner(
                    user, pending_only=pending_only
                )
            case "outgoing":
                consents = Consent.helper.from_solicitor(
                    user, pending_only=pending_only
                )

        serializer = ListConsent(
            consents, many=True, context={"request": self.request, "direction": way}
        )
        return response.Response(serializer.data)

    @swagger_auto_schema(
        method="get",
        operation_summary="Get user's incoming pending consent requests",
        operation_description="Gets the filtered user's incoming pending consent requests",
        manual_parameters=[
            openapi.Parameter(
                "address",
                openapi.IN_PATH,
                description="Ethereum wallet address (hex, 0x...)",
                type=openapi.TYPE_STRING,
                required=True,
                example="0x1234567890abcdef1234567890abcdef12345678",
            ),
        ],
        responses={
            "200": openapi.Response(
                description="User details",
                schema=ListConsent,
                examples={
                    "application/json": [
                        {
                            "url": "http://localhost:8050/api/consents/1/",
                            "id": 1,
                            "created_at": 1758271130,
                            "dataset": "http://localhost:8050/api/assets/did:op:75afadb65591ca977344fa598c2b42c0ca5c7e8620b7c8bf47533e8f222d7997/",
                            "algorithm": "http://localhost:8050/api/assets/did:op:b533c6703cd099cfc228e1f6587c4049bc1f445b2bd0da24f5321a13fd9f1c8a/",
                            "solicitor": {
                                "url": "http://localhost:8050/api/users/0xD999bAaE98AC5246568FD726be8832c49626867D/",
                                "address": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                            },
                            "reason": "Provided reason",
                            "request": {"trusted_algorithm": True},
                            "response": None,
                            "status": "Pending",
                            "direction": "Incoming",
                        }
                    ]
                },
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "No ConsentsUser matches the given query"
                    },
                },
            ),
        },
        tags=["User"],
    )
    @action(detail=True, methods=["get"])
    def incoming(self, *args, **kwargs):
        return self._actions("incoming")

    @swagger_auto_schema(
        method="get",
        operation_summary="Get user's outgoing consent requests",
        operation_description="Gets the filtered user's outgoing consent requests",
        manual_parameters=[
            openapi.Parameter(
                "address",
                openapi.IN_PATH,
                description="Ethereum wallet address (hex, 0x...)",
                type=openapi.TYPE_STRING,
                required=True,
                example="0x1234567890abcdef1234567890abcdef12345678",
            ),
        ],
        responses={
            "200": openapi.Response(
                description="List of outgoing consents",
                schema=ListConsent,
                examples={
                    "application/json": [
                        {
                            "url": "..",
                            "id": 1,
                            "created_at": 1758271130,
                            "dataset": "..",
                            "algorithm": "..",
                            "solicitor": {
                                "url": "..",
                                "address": "0xD999bAaE98AC5246568FD726be8832c49626867D",
                            },
                            "reason": "Provided reason",
                            "request": {"trusted_algorithm": True},
                            "response": None,
                            "status": "Pending",
                            "direction": "Outgoing",
                        }
                    ]
                },
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "No ConsentsUser matches the given query"
                    }
                },
            ),
        },
        tags=["User"],
    )
    @action(detail=True, methods=["get"])
    def outgoing(self, *args, **kwargs):
        return self._actions("outgoing")


# Settings
SIWE_VERSION = getattr(settings, "SIWE_VERSION", "1")
NONCE_EXP_MINUTES = getattr(settings, "NONCE_EXP_MINUTES", 15)
ACCESS_TOKEN_LIFETIME_MINUTES = getattr(settings, "WALLET_ACCESS_TOKEN_MINUTES", None)


class WalletAuthViewset(viewsets.ViewSet):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        method="get",
        operation_summary="Get SIWE nonce message",
        operation_description="Issues a SIWE-style message with a one-time nonce for the provided wallet address and chain ID. The frontend should ask the wallet to sign this message",
        manual_parameters=[
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Ethereum wallet address (hex, 0x...)",
                type=openapi.TYPE_STRING,
                required=True,
                example="0x1234567890abcdef1234567890abcdef12345678",
            ),
            openapi.Parameter(
                "chain_id",
                openapi.IN_QUERY,
                description="Ethereum chain ID (integer, e.g. 1 for mainnet)",
                type=openapi.TYPE_INTEGER,
                required=True,
                example=1,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="SIWE message and nonce issued",
                example={
                    "address": "0x1234567890abcdef1234567890abcdef12345678",
                    "chainId": 1,
                    "nonce": "abc123..",
                    "issuedAt": "2024-06-01T12:00:00Z",
                    "expirationTime": "2024-06-01T12:15:00Z",
                    "message": "..",
                },
            ),
            "400": openapi.Response(
                description="Invalid input or error retrieving origin",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Invalid input, nonce not found, or expired",
                    },
                },
            ),
        },
        tags=["Wallet Authentication"],
    )
    @action(detail=False, methods=["get"])
    def nonce(self, request):
        q = serializers.NonceQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        address = q.validated_data["address"].strip()
        chain_id = q.validated_data["chain_id"]

        origin = request.headers.get("Origin") or request.headers.get("Referer")
        if origin:
            if isinstance(origin, bytes):
                origin = origin.decode("utf-8", errors="ignore")
            elif isinstance(origin, ParseResult):
                origin = origin.geturl()
            else:
                origin = str(origin)
            try:
                parsed = urlparse(origin)
                domain = parsed.hostname
                scheme = parsed.scheme
                netloc = parsed.netloc
                uri = f"{scheme}://{netloc}"
            except Exception as e:
                return response.Response(
                    {"error": f"Error retrieving origin from headers: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            domain = request.get_host().split(":")[0]
            uri = request.build_absolute_uri("/")

        try:
            checksum_addr = to_checksum_address(address)
        except Exception:
            return response.Response(
                {"error": "Invalid wallet address"}, status=status.HTTP_400_BAD_REQUEST
            )

        issued_at = timezone.now()
        expires_at = issued_at + timedelta(minutes=NONCE_EXP_MINUTES)
        nonce = get_random_string(length=20) + secrets.token_hex(4)

        statement = "Sign in to this application to authenticate your wallet"
        message = build_siwe_message(
            domain=domain,
            address=checksum_addr,
            statement=statement,
            uri=uri,
            version=SIWE_VERSION,
            chain_id=chain_id,
            nonce=nonce,
            issued_at_iso=(
                issued_at.isoformat().replace("+00:00", "Z")
                if issued_at.tzinfo and issued_at.utcoffset() == timedelta(0)
                else issued_at.isoformat()
            ),
            expires_at_iso=(
                expires_at.isoformat().replace("+00:00", "Z")
                if expires_at.tzinfo and expires_at.utcoffset() == timedelta(0)
                else expires_at.isoformat()
            ),
        )

        models.WalletNonce.objects.update_or_create(
            address=checksum_addr,
            defaults={
                "nonce": nonce,
                "chain_id": chain_id,
                "domain": domain,
                "uri": uri,
                "issued_at": issued_at,
                "expires_at": expires_at,
            },
        )

        return response.Response(
            {
                "address": checksum_addr,
                "chainId": chain_id,
                "nonce": nonce,
                "issuedAt": issued_at.isoformat(),
                "expirationTime": expires_at.isoformat(),
                "message": message,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        method="post",
        operation_summary="Verify SIWE signature",
        operation_description="Verifies the signature of the SIWE message generated by the backend. On success, issues a JWT for the wallet address",
        request_body=serializers.NonceVerifySerializer,
        responses={
            "200": openapi.Response(
                description="JWT issued for wallet authentication",
                examples={
                    "application/json": {
                        "access": "<JWT>",
                        "walletAddress": "0x1234567890abcdef1234567890abcdef12345678",
                        "chainId": 1,
                        "expiresIn": 900,
                    }
                },
            ),
            "400": openapi.Response(
                description="Invalid input, nonce not found, or expired",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Invalid input, nonce not found, or expired"
                    },
                },
            ),
            "401": openapi.Response(
                description="Signature does not match the provided address",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
                examples={
                    "application/json": {
                        "detail": "Signature does not match the provided address"
                    },
                },
            ),
        },
        tags=["Wallet Authentication"],
    )
    @action(detail=False, methods=["post"])
    def verify(self, request):
        # ... (implementation unchanged)
        s = serializers.NonceVerifySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        address = s.validated_data["address"].strip()
        signature = s.validated_data["signature"].strip()

        try:
            checksum_addr = to_checksum_address(address)
        except Exception:
            return response.Response(
                {"error": "Invalid wallet address"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rec = models.WalletNonce.objects.get(address=checksum_addr)
        except models.WalletNonce.DoesNotExist:
            return response.Response(
                {"error": "Nonce not found. Request a new nonce"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rec.is_expired():
            rec.delete()
            return response.Response(
                {"error": "Nonce expired. Request a new nonce"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        issued_at_iso = (
            rec.issued_at.isoformat().replace("+00:00", "Z")
            if rec.issued_at.tzinfo and rec.issued_at.utcoffset() == timedelta(0)
            else rec.issued_at.isoformat()
        )
        expires_at_iso = (
            rec.expires_at.isoformat().replace("+00:00", "Z")
            if rec.expires_at.tzinfo and rec.expires_at.utcoffset() == timedelta(0)
            else rec.expires_at.isoformat()
        )

        message = build_siwe_message(
            domain=rec.domain,
            address=checksum_addr,
            statement="Sign in to this application to authenticate your wallet",
            uri=rec.uri,
            version=SIWE_VERSION,
            chain_id=rec.chain_id,
            nonce=rec.nonce,
            issued_at_iso=issued_at_iso,
            expires_at_iso=expires_at_iso,
        )

        encoded = encode_defunct(text=message)

        try:
            recovered = Account.recover_message(encoded, signature=signature)
            recovered_checksum = to_checksum_address(recovered)
        except Exception:
            return response.Response(
                {"error": "Invalid signature format or recovery failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if recovered_checksum != checksum_addr:
            return response.Response(
                {"error": "Signature does not match the provided address"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        rec.delete()

        user, _ = models.ConsentsUser.objects.get_or_create(
            address=recovered_checksum,
            defaults={"username": recovered_checksum},
        )

        token = AccessToken.for_user(user)
        token["wallet_address"] = recovered_checksum
        token["chain_id"] = rec.chain_id
        token["scope"] = "wallet_auth"

        if ACCESS_TOKEN_LIFETIME_MINUTES:
            token.set_exp(lifetime=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))

        exp_seconds = None
        if "exp" in token.payload:
            exp_ts = int(token["exp"])
            exp_seconds = max(0, exp_ts - int(timezone.now().timestamp()))

        return response.Response(
            {
                "access": str(token),
                "walletAddress": recovered_checksum,
                "chainId": rec.chain_id,
                "expiresIn": exp_seconds,
            },
            status=status.HTTP_200_OK,
        )
