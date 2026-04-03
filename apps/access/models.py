from django.db import models

from apps.accounts.models import User


class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "roles"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_users")

    class Meta:
        db_table = "user_roles"
        unique_together = ("user", "role")


class Resource(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "resources"


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="rules")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="rules")
    read_own = models.BooleanField(default=False)
    read_all = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_own = models.BooleanField(default=False)
    update_all = models.BooleanField(default=False)
    delete_own = models.BooleanField(default=False)
    delete_all = models.BooleanField(default=False)

    class Meta:
        db_table = "access_rules"
        unique_together = ("role", "resource")
