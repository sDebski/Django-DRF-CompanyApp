from knox.auth import AuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase

from core.models import User
from company_app.auth import TokenAuthentication


class TokenAuthenticationTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="test_auth", password="test_auth", email="test_auth@mail.com"
        )
        cls.token, _ = AuthToken.objects.create(user=cls.user)
        return super().setUpTestData()

    def modify_user(self, is_active, is_deleted):
        self.user.is_active = is_active
        self.user.is_deleted = is_deleted
        self.user.save()

    def test_active_not_deleted(self):
        self.modify_user(is_active=True, is_deleted=False)
        user, token = TokenAuthentication().validate_user(self.token)
        self.assertEqual(user, self.user)
        self.assertEqual(token, self.token)

    def test_active_deleted(self):
        self.modify_user(is_active=True, is_deleted=True)
        with self.assertRaises(AuthenticationFailed):
            TokenAuthentication().validate_user(self.token)

    def test_not_active_not_deleted(self):
        self.modify_user(is_active=False, is_deleted=False)
        with self.assertRaises(AuthenticationFailed):
            TokenAuthentication().validate_user(self.token)

    def test_not_active_deleted(self):
        self.modify_user(is_active=False, is_deleted=True)
        with self.assertRaises(AuthenticationFailed):
            TokenAuthentication().validate_user(self.token)
