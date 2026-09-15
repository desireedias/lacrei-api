from rest_framework import permissions, serializers, viewsets

from .models import Appointment
from .permissions import IsAppointmentOwner
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAppointmentOwner,
    ]

    def get_queryset(self):
        queryset = Appointment.objects.select_related(
            "professional",
            "professional__user",
        )

        user = self.request.user

        if user.is_staff:
            return queryset

        return queryset.filter(professional__user=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "professional_profile"):
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Apenas usuários com perfil profissional "
                        "podem criar agendamentos."
                    )
                }
            )

        serializer.save(
            professional=user.professional_profile,
        )