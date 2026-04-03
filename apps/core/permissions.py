from rest_framework.permissions import BasePermission

from apps.access.services import AccessService


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "is_authenticated", False))


class HasResourcePermission(BasePermission):
    resource_code = ""
    action = ""

    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        return AccessService.has_permission(request.user, self.resource_code, self.action)
