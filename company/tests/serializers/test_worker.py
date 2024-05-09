from company import serializers, models
from django.test import TestCase
from company.tests.mocks.mock_request import MockRequest
from unittest_parametrize import ParametrizedTestCase, parametrize
from rest_framework.exceptions import ValidationError


class WorkerSerializerTestCase(TestCase, ParametrizedTestCase):
    fixtures = ["worker.json"]

    def test_read_serializer(self):
        worker = models.Worker.objects.get(pk=1)

        data = serializers.WorkerReadSerializer(worker).data
        self.assertEqual(data["username"], worker.username)
        self.assertEqual(data["email"], worker.email)

    @parametrize(
        "data,failed",
        (
            ({"username": "updated_worker_username"}, True),
            (
                {
                    "username": "updated_worker_username",
                    "email": "updated.email@example.com",
                },
                False,
            ),
            ({"email": "updated.email@example.com"}, True),
            (
                {
                    "username": "updated_worker_username",
                    "email": "anna.nowak@example.com",
                },
                True,
            ),
        ),
    )
    def test_write_serializer_create(self, data, failed):
        request = MockRequest(method="POST")

        serializer = serializers.WorkerWriteSerializer(
            data=data, context={"request": request}
        )
        if failed:
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            worker = models.Worker.objects.filter(email=data["email"]).first()

            for data_k, data_v in data.items():
                worker_v = getattr(worker, data_k)
                self.assertEqual(worker_v, data_v)
