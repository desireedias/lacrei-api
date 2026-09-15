from rest_framework import permissions


class IsAppointmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.professional.user == request.user or request.user.is_staff
