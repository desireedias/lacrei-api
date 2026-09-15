from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Professional
from .serializers import (
    ProfessionalRegistrationSerializer,
    ProfessionalSerializer,
)


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.select_related("user").all()

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return ProfessionalRegistrationSerializer

        return ProfessionalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        professional = serializer.save()

        read_serializer = ProfessionalSerializer(
            professional,
            context={"request": request},
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_201_CREATED,
        )