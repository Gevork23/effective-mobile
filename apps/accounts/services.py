import bcrypt
from django.utils import timezone

from apps.accounts.models import Session, User
from apps.access.models import Role, UserRole


class PasswordService:
    @staticmethod
    def hash_password(raw_password: str) -> str:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
        return password_hash.decode("utf-8")

    @staticmethod
    def verify_password(raw_password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(raw_password.encode("utf-8"), password_hash.encode("utf-8"))


class SessionService:
    @staticmethod
    def create_session(user: User, ip_address: str | None, user_agent: str | None) -> Session:
        return Session.objects.create(
            user=user,
            session_key=Session.generate_key(),
            expires_at=Session.default_expiry(),
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def logout(session: Session) -> None:
        session.is_active = False
        session.save(update_fields=["is_active"])

    @staticmethod
    def logout_all_for_user(user: User) -> None:
        Session.objects.filter(user=user, is_active=True).update(is_active=False)


class UserService:
    @staticmethod
    def create_user(first_name: str, last_name: str, middle_name: str | None, email: str, password: str) -> User:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name or None,
            email=email,
            password_hash=PasswordService.hash_password(password),
            is_active=True,
            is_deleted=False,
        )
        default_role = Role.objects.get(code="user")
        UserRole.objects.create(user=user, role=default_role)
        return user

    @staticmethod
    def soft_delete(user: User) -> None:
        user.is_active = False
        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.save(update_fields=["is_active", "is_deleted", "deleted_at"])
        SessionService.logout_all_for_user(user)
