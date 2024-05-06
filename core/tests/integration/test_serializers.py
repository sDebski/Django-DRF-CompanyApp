from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from core.serializers import AuthTokenSerializer

User = get_user_model()


class AuthTokenSerializerTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test_ser", password="test_ser", email="test_ser@mail.com")
        return super().setUp()
    
    @patch("django.contrib.auth.authenticate")
    def _test_validate(self, mock_auth, data, failed):
        mock_auth.return_value = self.user
        self.user.refresh_from_db()
        
        if failed:
            with self.assertRaises(ValidationError):
                attrs = AuthTokenSerializer().validate(data)
        else:
            attrs = AuthTokenSerializer().validate(data)
            self.user.refresh_from_db()
            self.assertEqual(attrs.get("user"), self.user)

    def test_validate_ok(self):
        data = {"username": "test_ser", "password": "test_ser"}
        self._test_validate(data=data, failed=False)
        self.user.refresh_from_db()

    def test_validate_fail(self):
        data = {"username": "test_ser", "password": "failed_pass"}
        self._test_validate(data=data, failed=True)
        self.user.refresh_from_db()