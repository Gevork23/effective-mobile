from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.accounts.services import PasswordService
from apps.access.models import AccessRule, Resource, Role, UserRole


class Command(BaseCommand):
    help = "Seed roles, resources, rules and demo users"

    def handle(self, *args, **options):
        roles = {
            "admin": "Administrator",
            "manager": "Manager",
            "user": "Regular User",
            "guest": "Guest",
        }
        role_objs = {}
        for code, name in roles.items():
            role, _ = Role.objects.get_or_create(code=code, defaults={"name": name})
            role_objs[code] = role

        resources = {
            "users": "Users",
            "products": "Products",
            "orders": "Orders",
            "access_rules": "Access rules",
        }
        resource_objs = {}
        for code, name in resources.items():
            resource, _ = Resource.objects.get_or_create(code=code, defaults={"name": name})
            resource_objs[code] = resource

        matrix = {
            "admin": dict(read_own=True, read_all=True, create_permission=True, update_own=True, update_all=True, delete_own=True, delete_all=True),
            "manager": dict(read_own=True, read_all=True, create_permission=True, update_own=True, update_all=True, delete_own=False, delete_all=False),
            "user": dict(read_own=True, read_all=False, create_permission=True, update_own=True, update_all=False, delete_own=True, delete_all=False),
            "guest": dict(read_own=False, read_all=False, create_permission=False, update_own=False, update_all=False, delete_own=False, delete_all=False),
        }

        for role_code, perms in matrix.items():
            for resource in resource_objs.values():
                AccessRule.objects.get_or_create(role=role_objs[role_code], resource=resource, defaults=perms)

        admin_user, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "last_name": "Adminov",
                "first_name": "System",
                "password_hash": PasswordService.hash_password("Admin12345!"),
            },
        )
        user_user, _ = User.objects.get_or_create(
            email="user@example.com",
            defaults={
                "last_name": "Petrov",
                "first_name": "Ivan",
                "middle_name": "Ivanovich",
                "password_hash": PasswordService.hash_password("User12345!"),
            },
        )

        UserRole.objects.get_or_create(user=admin_user, role=role_objs["admin"])
        UserRole.objects.get_or_create(user=user_user, role=role_objs["user"])

        self.stdout.write(self.style.SUCCESS("Seed completed"))
