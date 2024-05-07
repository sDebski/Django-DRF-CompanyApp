from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from core.models import User


class PermissionSettingsTest(APITestCase):
    def test_permission_settings(self):
        self.assertCountEqual(
            api_settings.DEFAULT_PERMISSION_CLASSES, [IsAuthenticated]
        )


class PermissionAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="test_permission",
            password="test_permission",
            email="test_permission@mail.com",
        )
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_should_not_suspend(self):
        resp = self.client.get("/core/me/")
        self.assertEqual(resp.status_code, 200)
