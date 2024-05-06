from rest_framework.test import APITestCase

from core.models import User


class UserManagerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_deleted = cls.create_user("1", is_deleted=True)
        cls.user = cls.create_user("2")
        return super().setUpTestData()

    @staticmethod
    def create_user(name_part, **kwargs):
        username = f"manager_{name_part}"
        email = f"{username}@mail.com"
        return User.objects.create_user(
            username=username, password=username, email=email, **kwargs
        )

    def test_get_by_natural_key_ok(self):
        obj = User.objects.get_by_natural_key("manager_2")
        self.assertEqual(obj, self.user)
        self.assertEqual(obj.pk, self.user.pk)

    def test_get_by_natural_key_not_found(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_natural_key("manager_1")
