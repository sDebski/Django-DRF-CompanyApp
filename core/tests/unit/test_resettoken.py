from django_rest_passwordreset.models import get_password_reset_token_expiry_time
from rest_framework.test import APITestCase


class ResetTokenExpiryTimeTest(APITestCase):
    def test_reset_token_expiry_time(self):
        result = get_password_reset_token_expiry_time()
        self.assertAlmostEqual(result, 0.3333333, delta=0.000001)
