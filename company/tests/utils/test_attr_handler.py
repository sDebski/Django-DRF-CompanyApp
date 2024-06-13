from company.models import Task
from company.attr_handler import AttrHandler
from rest_framework.test import APITestCase
from unittest_parametrize import ParametrizedTestCase, parametrize
from company.exceptions import MissingArgumentException


class AttrHandlerTestCase(APITestCase, ParametrizedTestCase):
    fixtures = [
        "user.json",
        "projectcategory.json",
        "project.json",
        "label.json",
        "worker.json",
        "task.json",
    ]

    def setUp(self) -> None:
        self.task = Task.objects.get(pk=1)  # status = "Nowe"
        self.ah = AttrHandler(self.task, "status")
        return super().setUp()

    def test_init_attr_handler_with_wrong_field(self):
        with self.assertRaises(MissingArgumentException):
            AttrHandler(self.task, "non_existing_attr")

    def test_has_field_changed(self):
        self.task.status = "Zakończone"
        self.assertTrue(self.ah.has_field_changed())

    @parametrize(
        "previous_list,expected",
        [
            (["Nowe"], True),
            (["Nowe", "Zakończone"], True),
            (["Zakończone"], False),
        ],
    )
    def test_has_previous_values(self, previous_list, expected):
        self.task.status = "Zakończone"
        self.assertIs(self.ah.has_field_previous_values(*previous_list), expected)

    @parametrize(
        "current_list,expected",
        [
            (["W trakcie"], True),
            (["Nowe", "Zakończone"], False),
            (["W trakcie", "Zakończone"], True),
        ],
    )
    def test_has_current_values(self, current_list, expected):
        self.task.status = "W trakcie"
        self.assertIs(self.ah.has_field_current_values(*current_list), expected)
