from django.db import models
from typing import Type
from company.exceptions import MissingArgumentException

MyAppModel = Type[models.Model]


class AttrHandler:
    def __init__(self, obj: MyAppModel, field: str) -> None:
        self.obj = obj

        self._hasattr("tracker")
        self._hasattr(field)

        self.tracker = obj.tracker
        self.field = field

    def _hasattr(self, field):
        if not hasattr(self.obj, field):
            self._raise_missing_arg_exc(field)

    def has_field_previous_values(self, *expected_previous_values) -> bool:
        """
        Function checks if previous field's value is in expected_previous_values
        """
        return self.tracker.previous(self.field) in expected_previous_values

    def has_field_changed(self) -> bool:
        """
        Function checks if the obj's field has changed.
        """
        return self.tracker.has_changed(self.field)

    def has_field_current_values(self, *expected_current_values) -> bool:
        """
        Function checks if previous field's value is in expected_current_values
        """
        return getattr(self.obj, self.field) in expected_current_values

    def _has_field(self, field: str) -> bool:
        """
        Function checks if field is available in instance
        """
        if not hasattr(self.obj, field):
            self._raise_missing_arg_exc("field")

    def _raise_missing_arg_exc(self, field):
        """
        Function raises formatted exception
        """
        raise MissingArgumentException(f"{self.obj} has no {field} implemented.")
