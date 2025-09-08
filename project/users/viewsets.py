import secrets
from datetime import timedelta
from typing import Literal

from consents.models import Consent
from consents.serializers import ListConsent
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
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
    mixins.DestroyModelMixin,
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
                consents = Consent.helper.from_algorithm_owner(
                    user, pending_only=pending_only
                )

        serializer = ListConsent(
            consents, many=True, context={"request": self.request, "direction": way}
        )
        return response.Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="pending-incoming")
    def pending_incoming(self, *args, **kwargs):
        return self._actions("incoming", pending_only=True)

    @action(detail=True, methods=["get"], url_path="pending-outgoing")
    def pending_outgoing(self, *args, **kwargs):
        return self._actions("outgoing", pending_only=True)

    @action(detail=True, methods=["get"])
    def incoming(self, *args, **kwargs):
        return self._actions("incoming")

    @action(detail=True, methods=["get"])
    def outgoing(self, *args, **kwargs):
        return self._actions("outgoing")


# Settings
SIWE_VERSION = getattr(settings, "SIWE_VERSION", "1")
NONCE_EXP_MINUTES = getattr(settings, "NONCE_EXP_MINUTES", 15)
ACCESS_TOKEN_LIFETIME_MINUTES = getattr(settings, "WALLET_ACCESS_TOKEN_MINUTES", None)
PIN_DOMAIN = getattr(settings, "SIWE_DOMAIN", None)  # e.g., "api.example.com"
PIN_URI = getattr(settings, "SIWE_URI", None)  # e.g., "https://api.example.com/"


class WalletAuthViewset(viewsets.ViewSet):

    permission_classes = [AllowAny]

    """
    Wallet-based auth ViewSet for Django REST Framework:
        - GET  /auth/wallet/nonce/   -> issues a SIWE-style message with a one-time nonce
        - POST /auth/wallet/verify/  -> verifies signature, returns a JWT

    Key ideas:
        - The backend dictates the exact message to sign.
        - We store nonce + metadata (domain, uri, chain_id, issued/expires) so we can deterministically
        reconstruct the *exact* message later during verification.
        - On success we delete the nonce (one-time use) and issue a short-lived JWT that carries the
        wallet address in the claims. This keeps subsequent requests simple (Authorization: Bearer ...).
    """

    @action(detail=False, methods=["get"])
    def nonce(self, request):
        """
        Generate and persist a nonce + SIWE-style message bound to:
          - the requesting domain (or PIN_DOMAIN),
          - the service URI (or PIN_URI),
          - the provided wallet address and chain_id,
          - timestamps (IssuedAt/ExpirationTime).
        Return the message the frontend should ask the wallet to sign.
        """
        q = serializers.NonceQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        address = q.validated_data["address"].strip()
        chain_id = q.validated_data["chain_id"]

        # Derive domain & uri: use pinned values if configured, else from request.
        domain = PIN_DOMAIN or request.get_host().split(":")[0]
        uri = PIN_URI or request.build_absolute_uri("/")

        # Normalize address to checksum for display; we store original case-insensitively.
        try:
            checksum_addr = to_checksum_address(address)
        except Exception:
            return response.Response(
                {"error": "Invalid wallet address"}, status=status.HTTP_400_BAD_REQUEST
            )

        issued_at = timezone.now()
        expires_at = issued_at + timedelta(minutes=NONCE_EXP_MINUTES)
        nonce = get_random_string(length=20) + secrets.token_hex(4)

        statement = "Sign in to this application to authenticate your wallet."
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

        # Upsert: one active nonce per address; overwrite if one exists
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
                "message": message,  # <-- SIGN THIS EXACT MESSAGE
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify(self, request):
        """
        Verify the signature of the message *we generated*.
        Steps:
          1) Load stored record by address; ensure nonce not expired.
          2) Reconstruct the SIWE-style message *exactly* as delivered in GET /nonce.
          3) Recover address from signature (EIP-191) and compare.
          4) Delete nonce (one-time use) and issue a JWT with wallet claims.

        Returns:
          {
            "access": "<JWT>",
            "walletAddress": "0x…",
            "chainId": 1,
            "expiresIn": <seconds>   # optional convenience
          }
        """
        s = serializers.NonceVerifySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        address = s.validated_data["address"].strip()
        signature = s.validated_data["signature"].strip()

        # Normalize and fetch stored entry
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
                {"error": "Nonce not found. Request a new nonce."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Expiry check (server-side, independent of any client-provided timestamps)
        if rec.is_expired():
            rec.delete()  # clean up
            return response.Response(
                {"error": "Nonce expired. Request a new nonce."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Rebuild the *exact* message we asked the user to sign.
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
            statement="Sign in to this application to authenticate your wallet.",
            uri=rec.uri,
            version=SIWE_VERSION,
            chain_id=rec.chain_id,
            nonce=rec.nonce,
            issued_at_iso=issued_at_iso,
            expires_at_iso=expires_at_iso,
        )

        # EIP-191 personal_sign semantics (eth_account handles the prefixing).
        encoded = encode_defunct(text=message)

        try:
            recovered = Account.recover_message(encoded, signature=signature)
            recovered_checksum = to_checksum_address(recovered)
        except Exception:
            return response.Response(
                {"error": "Invalid signature format or recovery failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if recovered_checksum != checksum_addr:
            # Mismatch → either wrong address or signature not for our message.
            return response.Response(
                {"error": "Signature does not match the provided address."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Success → one-time use: delete the nonce to prevent replay.
        rec.delete()

        # Fetch user
        user, _ = models.ConsentsUser.objects.get_or_create(
            address=recovered_checksum,
            defaults={"username": recovered_checksum},
        )

        # Issue a JWT. We don't require a Django User; we embed wallet claims directly.
        token = AccessToken.for_user(user)
        token["wallet_address"] = recovered_checksum
        token["chain_id"] = rec.chain_id
        token["scope"] = "wallet_auth"

        # Optionally override lifetime per token
        if ACCESS_TOKEN_LIFETIME_MINUTES:
            token.set_exp(lifetime=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))

        # Convenience for frontend: seconds until JWT expiry
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
