from apps.access.models import AccessRule


class AccessService:
    @staticmethod
    def get_user_rules(user, resource_code: str):
        if not getattr(user, "id", None):
            return AccessRule.objects.none()

        return AccessRule.objects.filter(
            role__role_users__user=user,
            resource__code=resource_code,
        )

    @staticmethod
    def has_permission(user, resource_code: str, action: str, owner_id=None) -> bool:
        rules = AccessService.get_user_rules(user, resource_code)

        if action == "create":
            return any(rule.create_permission for rule in rules)

        if action == "read":
            if any(rule.read_all for rule in rules):
                return True
            return bool(owner_id and str(owner_id) == str(user.id) and any(rule.read_own for rule in rules))

        if action == "update":
            if any(rule.update_all for rule in rules):
                return True
            return bool(owner_id and str(owner_id) == str(user.id) and any(rule.update_own for rule in rules))

        if action == "delete":
            if any(rule.delete_all for rule in rules):
                return True
            return bool(owner_id and str(owner_id) == str(user.id) and any(rule.delete_own for rule in rules))

        return False
