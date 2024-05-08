from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ProjectCategoryViewSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = ["user.json", "projectcategory.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    @parametrize(
        "payload,status_",
        [
            ({"name": "ProjectCategory_1"}, status.HTTP_201_CREATED),
            ({"name": "ProjectCategory 1"}, status.HTTP_201_CREATED),
            ({"name": 1234}, status.HTTP_201_CREATED),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_projectcategory_create(self, payload, status_):
        url = reverse("company:projectcategories-list")
        response = self.client.post(url, data=payload)

        if status_ == status.HTTP_201_CREATED:
            projectcategory = models.ProjectCategory.objects.filter(name=payload["name"]).first()
            self.assertEqual(projectcategory.name, str(payload["name"]))
        else:
            self.assertEqual(response.status_code, status_)

    def test_projectcategory_list(self):
        url = reverse("company:projectcategories-list")
        response = self.client.get(url)
        projectcategories = models.ProjectCategory.objects.all()
        self.assertEqual(len(response.data), projectcategories.count())
        serializer = serializers.ProjectCategoryReadSerializer(projectcategories, many=True)
        projectcategories_data = serializer.data

        for response_projectcategory, db_projectcategory in zip(projectcategories_data, response.data):
            with self.subTest(msg="test each projectcategory"):
                self.assertDictEqual(response_projectcategory, db_projectcategory)

    @parametrize(
        "payload,status_",
        [
            ({"name": "projectcategory_1"}, status.HTTP_200_OK),
            ({"name": "projectcategory 1"}, status.HTTP_200_OK),
            ({"name": 1234}, status.HTTP_200_OK),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_projectcategory_update(self, payload, status_):
        projectcategory_pk = 1
        url = reverse("company:projectcategories-detail", kwargs={"pk": projectcategory_pk})
        response = self.client.put(url, data=payload)

        if status_ == status.HTTP_200_OK:
            projectcategory = models.ProjectCategory.objects.filter(name=payload["name"]).first()
            self.assertEqual(projectcategory.name, str(payload["name"]))
            self.assertEqual(projectcategory.pk, projectcategory_pk)
        else:
            self.assertEqual(response.status_code, status_)
