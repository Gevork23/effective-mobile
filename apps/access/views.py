from rest_framework import generics
from rest_framework.permissions import BasePermission

from apps.access.models import AccessRule, Resource, Role
from apps.access.serializers import AccessRuleSerializer, ResourceSerializer, RoleSerializer


class IsAdminCustom(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        return request.user.user_roles.filter(role__code="admin").exists()


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminCustom]


class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminCustom]


class AccessRuleListCreateView(generics.ListCreateAPIView):
    queryset = AccessRule.objects.select_related("role", "resource").all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminCustom]


class AccessRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessRule.objects.select_related("role", "resource").all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminCustom]
