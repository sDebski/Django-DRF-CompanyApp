from rest_framework.test import APITestCase, override_settings
from django.urls import reverse
from django.conf import settings


class AuthTest(APITestCase):
    def test_health_check_ok(self):
        resp = self.client.head("/core/health/")
        self.assertEqual(resp.status_code, 200)

    def test_labels_401(self):
        url = reverse("company:labels-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    @override_settings(X_API_KEY="abc")
    def test_labels_200(self):
        print("X_API_KEY przed: ", settings.X_API_KEY)
        url = reverse(
            "company:labels-list",
        )
        print("X_API_KEY po: ", settings.X_API_KEY)

        resp = self.client.get(url, HTTP_X_API_KEY="abc")
        self.assertEqual(resp.status_code, 200)
