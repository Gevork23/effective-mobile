from rest_framework import serializers

from apps.accounts.models import User


class RegisterSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    middle_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_repeat = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Пароли не совпадают")

        email = attrs["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        attrs["email"] = email
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UpdateProfileSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    middle_name = serializers.CharField(max_length=150, required=False, allow_blank=True)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        )
