from assets.models import Asset
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from helpers.services.aquarius import aquarius
from rest_framework import status
from rest_framework.test import APITestCase

from consents.models import Consent

User = get_user_model()


class ConsentTest(APITestCase):
    def create_consent(
        self,
        reason="Test reason",
        dataset="did:op:8f0d80e898aef506dd87d17dc3d01cb89e61c33bab9618817394c7ad2fd725f0",
        algorithm="did:op:4845638ac968b7929f91cfedfea1f7f87ebb08ee21f18dfc480289cbb6ceeb83",
        solicitor="solicitor address",
        request="0",
    ) -> HttpResponse:
        response = self.client.post(
            reverse("consents-list"),
            {
                "reason": reason,
                "dataset": dataset,
                "algorithm": algorithm,
                "solicitor": solicitor,
                "request": request,
            },
            format="json",
        )

        if response.status_code != status.HTTP_201_CREATED:
            print("Failed to create consent:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)

        # Return the data into an instance of the Consent model
        return Consent.objects.filter().first()

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
        self.assertEqual(User.objects.count(), 2)
        self.assertIn("solicitor address", str(response.data))
        self.assertIn(aquarius.mock_address, str(response.data))

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

        url = reverse("users-detail", args=[aquarius.mock_address])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["incoming_pending_consents"], 1)
        self.assertEqual(response.data["outgoing_pending_consents"], 1)

    def test_consent_response(self):
        c = self.create_consent(request="3")

        url = reverse("consent-response-list", args=[c.pk])
        response = self.client.post(
            url,
            {"status": "A", "reason": "Test reason", "permitted": "3"},
            format="json",
        )

        print("Response:", response.data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNotNone(response.data)
        self.assertEqual(c.reason, response.data["reason"])
        self.assertEqual("A", response.data["status"])
