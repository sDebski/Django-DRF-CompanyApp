from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class LabelFilterSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = ["user.json", "label.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    @parametrize(
        "filter_,status_,amount",
        [
            ("name=ow", status.HTTP_200_OK, 2),
            ("name=a", status.HTTP_200_OK, 2),
            ("name=", status.HTTP_200_OK, 4),
            ("", status.HTTP_200_OK, 4),
        ],
    )
    def test_label_filterset(self, filter_, status_, amount):
        url = reverse("company:labels-list")
        response = self.client.get(f"{url}?{filter_}")

        if status_ == status.HTTP_200_OK:
            self.assertEqual(len(response.data), amount)
        else:
            self.assertEqual(response.status_code, status_)
