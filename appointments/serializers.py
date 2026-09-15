from django.utils import timezone
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

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
            "professional",
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

    def validate(self, attrs):
        request = self.context.get("request")
        scheduled_at = attrs.get("scheduled_at")

        if self.instance and scheduled_at is None:
            scheduled_at = self.instance.scheduled_at

        professional = request.user.professional_profile

        conflicting_appointments = Appointment.objects.filter(
            professional=professional,
            scheduled_at=scheduled_at,
        )

        if self.instance:
            conflicting_appointments = conflicting_appointments.exclude(
                pk=self.instance.pk
            )

        if conflicting_appointments.exists():
            raise serializers.ValidationError(
                {
                    "scheduled_at": (
                        "O profissional já possui uma consulta "
                        "agendada para este horário."
                    )
                }
            )

        return attrs
