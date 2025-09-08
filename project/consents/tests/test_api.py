from assets.models import Asset
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from eth_account import Account
from eth_account.messages import encode_defunct
from helpers.config import config
from rest_framework import status
from rest_framework.test import APITestCase

from consents.models import Consent

User = get_user_model()

wallet_address: str | None


class ConsentTest(APITestCase):
    def authenticate(self, private_key: str):
        self.client.credentials()

        # Random test account
        account = Account.from_key(private_key)

        global wallet_address
        wallet_address = account.address

        # 1. Get nonce
        nonce_url = reverse("auth-nonce")
        res = self.client.get(nonce_url, {"address": wallet_address})
        assert res.status_code == 200
        message = res.data["message"]

        # 2. Sign message
        signed = Account.sign_message(encode_defunct(text=message), account.key)

        # 3. Verify signature to get JWT
        verify_url = reverse("auth-verify")
        res = self.client.post(
            verify_url,
            {"address": wallet_address, "signature": signed.signature.hex()},
            format="json",
        )
        assert res.status_code == 200, f"Verification failed: {res.data}"

        # 4. Attach to client for requests
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        return account

    def create_consent(
        self, reason="Test reason", request="0", authenticate=True
    ) -> HttpResponse:
        if authenticate:
            self.authenticate(config.TEST_PRIVATE_KEY)

        response = self.client.post(
            reverse("consents-list"),
            {
                "reason": reason,
                "dataset": config.TEST_DATASET_DID,
                "algorithm": config.TEST_ALGORITHM_DID,
                "request": request,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        ), "Failed to create consent:", response.data
        self.assertIsNotNone(response.data)

        # Return the data into an instance of the Consent model
        return Consent.objects.filter().first()

    def create_consent_response(self, consent_id: int, permitted: str) -> HttpResponse:
        url = reverse("consent-response-list", args=[consent_id])
        response = self.client.post(
            url,
            {"reason": "Test reason", "permitted": permitted},
            format="json",
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("consents-detail", args=[consent_id])
        return self.client.get(url)

    def test_consent_creation_creates_assets(self):
        _ = self.create_consent()

        assets_url = reverse("assets-list")
        response = self.client.get(assets_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asset.objects.count(), 2)

    def test_consent_creation_creates_users(self):
        _ = self.create_consent()

        users_url = reverse("users-list")
        response = self.client.get(users_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Creates user for
        # 1. Dataset owner & Algorithm owner & Requester (all same in this case)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn(wallet_address, str(response.data))

    def test_consent_list_view(self):
        c = self.create_consent()

        url = reverse("consents-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, c.reason)
        self.assertEqual(len(response.data), 1)

    def test_consent_detail_view(self):
        c = self.create_consent()

        url = reverse("consents-detail", args=[c.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, c.reason)

    def test_consent_user_has_pending(self):
        _ = self.create_consent()

        url = reverse("users-detail", args=[wallet_address])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["incoming_pending_consents"], 1)
        self.assertEqual(response.data["outgoing_pending_consents"], 1)

    def test_consent_response_accepted(self):
        c = self.create_consent(request="3")
        cr = self.create_consent_response(c.pk, "3")

        self.assertEqual(cr.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cr.data)
        self.assertEqual("Accepted", cr.data["status"])

    def test_consent_response_resolved(self):
        c = self.create_consent(request="3")
        cr = self.create_consent_response(c.pk, "1")

        self.assertEqual(cr.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cr.data)
        self.assertEqual("Resolved", cr.data["status"])

    def test_consent_response_denied(self):
        c = self.create_consent(request="3")
        cr = self.create_consent_response(c.pk, "0")

        self.assertEqual(cr.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cr.data)
        self.assertEqual("Denied", cr.data["status"])

    def test_create_consent_unauthenticated(self):
        with self.assertRaises(AssertionError):
            self.create_consent(request="3", authenticate=False)

    def test_respond_consent_unauthorized(self):
        with self.assertRaises(AssertionError):
            c = self.create_consent(request="3")

            self.client.credentials(HTTP_AUTHORIZATION=None)
            self.create_consent_response(c.pk, "0")
