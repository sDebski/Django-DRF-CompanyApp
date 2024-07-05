from rest_framework.permissions import BasePermission
from company.models import Task


class ObjBasePermission(BasePermission):
    """
    Permission to object based on checking if
    an authenticated user has access to different action
    on object.

    One needs to extend this class and define:
    actions_to_check = ex. ["list", "retrieve"]
    owner_param = ex. "assigned_to"

    For Task object it checks if the user is an owner to perform editting.
    """

    actions_to_check = None
    owner_param = None

    def has_object_permission(self, request, view, obj):
        if not getattr(request.user, "is_authenticated"):
            return False
        if view.action not in self.actions_to_check:
            return True
        return self._has_object_permission(request.user, obj)

    def _has_object_permission(self, user, obj):
        return getattr(obj, self.owner_param) == user.worker


class TaskOwnerEditPermission(ObjBasePermission):
    actions_to_check = ["destroy", "update", "partial_update"]
    owner_param = "assigned_to"
