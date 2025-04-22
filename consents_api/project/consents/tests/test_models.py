from django.test import TestCase
from django.urls import reverse
from consents.models import Consent


class ConsentTest(TestCase):
    def create_consent(
        self,
        reason="Test reason",
        dataset="dataset DID",
        algorithm="algorithm DID",
        solicitor="solicitor address",
        request=0,
    ):
        return Consent.helper.get_or_create_from_aquarius(
            reason=reason,
            dataset=dataset,
            algorithm=algorithm,
            solicitor=solicitor,
            request=request,
        )

    def test_consent_creation(self):
        c = self.create_consent()

        self.assertTrue(isinstance(c, Consent))

    def test_consent_list_view(self):
        c = self.create_consent()

        url = reverse("consents-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c.reason)

    def test_consent_detail_view(self):
        c = self.create_consent()

        url = reverse("consents-detail", args=[c.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c.reason)
