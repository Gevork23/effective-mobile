from django.utils import timezone

from apps.accounts.models import Session


class AnonymousUser:
    id = None
    email = None
    is_active = False
    is_authenticated = False


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = AnonymousUser()
        request.session_obj = None

        session_key = request.COOKIES.get("session_id")
        if session_key:
            session = (
                Session.objects.select_related("user")
                .filter(
                    session_key=session_key,
                    is_active=True,
                    user__is_active=True,
                    user__is_deleted=False,
                )
                .first()
            )
            if session:
                if session.expires_at > timezone.now():
                    session.user.is_authenticated = True
                    request.user = session.user
                    request.session_obj = session
                else:
                    session.is_active = False
                    session.save(update_fields=["is_active"])

        return self.get_response(request)
