from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import PasswordService, SessionService, UserService
from apps.core.permissions import IsAuthenticatedCustom


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            middle_name=serializer.validated_data.get("middle_name"),
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower().strip()
        raw_password = serializer.validated_data["password"]
        user = User.objects.filter(email=email).first()

        if not user or not PasswordService.verify_password(raw_password, user.password_hash):
            return Response({"detail": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active or user.is_deleted:
            return Response({"detail": "Учетная запись деактивирована"}, status=status.HTTP_403_FORBIDDEN)

        session = SessionService.create_session(
            user=user,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        response = Response({"detail": "Успешный вход"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=settings.SESSION_MAX_AGE_SECONDS,
        )
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        if request.session_obj:
            SessionService.logout(request.session_obj)

        response = Response({"detail": "Выход выполнен"}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        return Response(UserResponseSerializer(request.user).data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(request.user, field, value)
        request.user.save()
        return Response(UserResponseSerializer(request.user).data)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def delete(self, request):
        UserService.soft_delete(request.user)
        response = Response({"detail": "Аккаунт деактивирован"}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return response
