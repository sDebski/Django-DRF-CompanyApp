from rest_framework.test import APITestCase
from django.urls import reverse


class AuthTest(APITestCase):
    def test_health_check_ok(self):
        resp = self.client.head("/core/health/")
        self.assertEqual(resp.status_code, 200)

    def test_labels_401(self):
        url = reverse("company:labels-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def test_labels_200(self):
        url = reverse("company:labels-list")

        resp = self.client.get(url, HTTP_X_API_KEY="secret")
        self.assertEqual(resp.status_code, 200)
