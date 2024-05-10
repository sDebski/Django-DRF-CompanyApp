from knox.models import AuthToken
from rest_framework.test import APIRequestFactory, APITestCase

from core.models import User
from core.views import LoginView, UserView


class UserDeletedTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = APIRequestFactory()
        cls.user = User.objects.create_user(
            username="user_del",
            password="user_del",
            email="user_del@mail.com",
            is_deleted=True,
        )
        cls.token, _ = AuthToken.objects.create(user=cls.user)
        cls.headers = {"Authorization": f"Token {cls.token.digest}"}
        return super().setUpTestData()

    def test_login_failed(self):
        payload = {
            "username": "user_del",
            "password": "user_del",
        }
        request = self.factory.post("/core/login/", data=payload, format="json")
        resp = LoginView.as_view()(request)
        self.assertEqual(resp.status_code, 401)

    def test_get_me(self):
        request = self.factory.get("/core/me/", headers=self.headers)
        resp = UserView.as_view()(request)
        self.assertEqual(resp.status_code, 401)

    def test_update_me(self):
        payload = {"email": "qweqwe@mail.com"}
        request = self.factory.patch(
            "/core/me/", data=payload, headers=self.headers, format="json"
        )
        resp = UserView.as_view()(request)
        self.assertEqual(resp.status_code, 401)
