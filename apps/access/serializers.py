from rest_framework import serializers

from apps.access.models import AccessRule, Resource, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class AccessRuleSerializer(serializers.ModelSerializer):
    role_code = serializers.CharField(source="role.code", read_only=True)
    resource_code = serializers.CharField(source="resource.code", read_only=True)

    class Meta:
        model = AccessRule
        fields = (
            "id",
            "role",
            "resource",
            "role_code",
            "resource_code",
            "read_own",
            "read_all",
            "create_permission",
            "update_own",
            "update_all",
            "delete_own",
            "delete_all",
        )
