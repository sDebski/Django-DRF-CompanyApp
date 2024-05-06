from rest_framework.test import APITestCase

from core.models import User

from knox.serializers import UserSerializer

class MeTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user("me", "me", email="me@mail.com")
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_me(self):
        resp = self.client.get("/core/me/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["first_name"], "")

    def test_patch_me(self):
        payload = {
            "first_name": "first_name",
        }
        resp = self.client.patch("/core/me/", data=payload, format="json")
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "first_name")
