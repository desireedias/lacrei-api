from rest_framework import permissions, serializers, viewsets

from professionals.models import Professional

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

        if not user.is_staff:
            queryset = queryset.filter(professional__user=user)

        professional_id = self.request.query_params.get("professional")

        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)

        return queryset

    def perform_create(self, serializer):
        professional = Professional.objects.filter(user=self.request.user).first()

        if professional is None:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Apenas usuários com perfil profissional "
                        "podem criar agendamentos."
                    )
                }
            )

        serializer.save(professional=professional)
