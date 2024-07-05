from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
    APITestCase,
)
from rest_framework.request import Request
from company import models
from company.viewsets import TaskViewSet
from company.permissions import TaskOwnerEditPermission
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskEditPermissionTestCase(APITestCase):
    fixtures = [
        "user.json",
        "projectcategory.json",
        "project.json",
        "label.json",
        "worker.json",
        "task.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        out = super().setUpTestData()
        return out

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.get(pk=1)

        worker = models.Worker.objects.get(pk=1)
        self.user.worker = worker
        self.user.save()

        self.task = models.Task.objects.get(pk=1)

        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def get_request(self, auth, query_params):
        request = self.factory.get("/", data=query_params)
        if auth:
            force_authenticate(request, user=self.user)
        return Request(request)

    def _test_has_task_obj_owner_permission(self, **kwargs):
        request = self.get_request(kwargs["auth"], kwargs["query_params"])
        view = kwargs["view_cls"](
            request=request, action=kwargs["action"], kwargs=kwargs["query_params"]
        )
        res = TaskOwnerEditPermission().has_object_permission(request, view, self.task)

        self.assertEqual(res, kwargs["expected"])

    def _test_for_action(self, action_expected: list[tuple[str, str]], test_kwargs):
        for action, expected in action_expected:
            test_kwargs.update(
                {
                    "action": action,
                    "expected": expected,
                }
            )
            self._test_has_task_obj_owner_permission(**test_kwargs)

    def test_permission_no_user(self):
        test_kwargs = {
            "auth": False,
            "view_cls": TaskViewSet,
            "query_params": {},
        }

        self._test_for_action(
            [("retrieve", False), ("update", False)],
            test_kwargs,
        )

    def test_permission_edit_success(self):
        test_kwargs = {
            "auth": True,
            "view_cls": TaskViewSet,
            "query_params": {},
        }

        self._test_for_action(
            [("retrieve", True), ("update", True)],
            test_kwargs,
        )

    def test_permission_edit_fail(self):
        test_kwargs = {
            "auth": True,
            "view_cls": TaskViewSet,
            "query_params": {},
        }

        self.user.worker = None
        self.user.save()

        self._test_for_action(
            [("retrieve", True), ("update", False)],
            test_kwargs,
        )
