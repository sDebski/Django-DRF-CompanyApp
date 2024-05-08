from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class LabelViewSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = ["user.json", "label.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    @parametrize(
        "payload,status_",
        [
            ({"name": "Label_1"}, status.HTTP_201_CREATED),
            ({"name": "Label 1"}, status.HTTP_201_CREATED),
            ({"name": 1234}, status.HTTP_201_CREATED),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_label_create(self, payload, status_):
        url = reverse("company:labels-list")
        response = self.client.post(url, data=payload)

        if status_ == status.HTTP_201_CREATED:
            label = models.Label.objects.filter(name=payload["name"]).first()
            self.assertEqual(label.name, str(payload["name"]))
        else:
            self.assertEqual(response.status_code, status_)

    def test_label_list(self):
        url = reverse("company:labels-list")
        response = self.client.get(url)
        labels = models.Label.objects.all()
        self.assertEqual(len(response.data), labels.count())
        serializer = serializers.LabelReadSerializer(labels, many=True)
        labels_data = serializer.data

        for response_label, db_label in zip(labels_data, response.data):
            with self.subTest(msg="test each label"):
                self.assertDictEqual(response_label, db_label)

    @parametrize(
        "payload,status_",
        [
            ({"name": "Label_1"}, status.HTTP_200_OK),
            ({"name": "Label 1"}, status.HTTP_200_OK),
            ({"name": 1234}, status.HTTP_200_OK),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_label_update(self, payload, status_):
        label_pk = 1
        url = reverse("company:labels-detail", kwargs={"pk": label_pk})
        response = self.client.put(url, data=payload)

        if status_ == status.HTTP_200_OK:
            label = models.Label.objects.filter(name=payload["name"]).first()
            self.assertEqual(label.name, str(payload["name"]))
            self.assertEqual(label.pk, label_pk)
        else:
            self.assertEqual(response.status_code, status_)
