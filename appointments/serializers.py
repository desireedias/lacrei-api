from datetime import timezone

from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    professional_name = serializers.CharField(
        source="professional.social_name",
        read_only=True,
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "professional",
            "professional_name",
            "scheduled_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "professional_name",
            "created_at",
            "updated_at",
        ]

    def validate_scheduled_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "A consulta deve ser agendada para uma data futura."
            )
        return value