from unittest import mock
from django.core.cache import cache
from rest_framework import test, status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class CacheViewTestCase(test.APITestCase):
    fixtures = ["user.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    @test.override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    @mock.patch("company.utils.calculate_value")
    def test_cache(self, mocked_calculate_value):
        """
        Check if response is cached
        """
        mocked_calculate_value.return_value = 10
        url = reverse("company:cache") + "?value=5"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], 10)

        mocked_calculate_value.return_value = 50

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], 10)

        cache.clear()
