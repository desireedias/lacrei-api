import re

from psycopg import transaction
from rest_framework import serializers

from users.models import User
from users.serializers import UserRegistrationSerializer

from .models import Professional


class ProfessionalValidationMixin:
    def validate_social_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome social deve ter pelo menos 2 caracteres."
            )

        return value

    def validate_professional(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "A profissão deve ter pelo menos 2 caracteres."
            )

        return value

    def validate_contact(self, value):
        value = value.strip()

        if re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError(
                "O contato telefônico não deve conter letras."
            )

        digits_only = re.sub(r"\D", "", value)

        if len(digits_only) not in (10, 11):
            raise serializers.ValidationError(
                "Informe um telefone válido com DDD "
                "(ex: 11999998888 ou (11) 99999-8888)."
            )

        return value


class ProfessionalSerializer(
    ProfessionalValidationMixin,
    serializers.ModelSerializer,
):
    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    email = serializers.EmailField(
            source="user.email",
            read_only=True,
        )

    class Meta:
        model = Professional
        fields = [
            "id",
            "username",
            "email",
            "social_name",
            "profession",
            "address",
            "contact",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "created_at",
            "updated_at",
        ]

class ProfessionalRegistrationSerializer(
    ProfessionalValidationMixin,
    serializers.ModelSerializer,
):
    user = UserRegistrationSerializer()

    class Meta:
        model = Professional
        fields = [
            "id",
            "user",
            "social_name",
            "profession",
            "address",
            "contact",
        ]
        read_only_fields = ["id"]

        @transaction.atomic
        def create(self, validated_data):
            user_data = validated_data.pop("user")

            user = User.objects.create_user(**user_data)

            return Professional.objects.create(
                user=user,
                **validated_data,
            )
