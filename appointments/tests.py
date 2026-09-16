from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from professionals.factories import ProfessionalFactory

from .factories import AppointmentFactory


class AppointmentAPITestCase(APITestCase):
    def setUp(self):
        self.professional = ProfessionalFactory()
        self.user = self.professional.user

        self.other_professional = ProfessionalFactory()

        self.appointment = AppointmentFactory(
            professional=self.professional,
        )

        self.list_url = "/api/v1/appointments/"
        self.detail_url = f"/api/v1/appointments/{self.appointment.id}/"

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.user)

        scheduled_at = timezone.now() + timedelta(days=5)

        response = self.client.post(
            self.list_url,
            {"scheduled_at": scheduled_at.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["professional"],
            self.professional.id,
        )

    def test_unauthenticated_user_cannot_create_appointment(self):
        scheduled_at = timezone.now() + timedelta(days=5)

        response = self.client.post(
            self.list_url,
            {"scheduled_at": scheduled_at.isoformat()},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_without_professional_profile_cannot_create_appointment(self):
        from users.factories import UserFactory

        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.list_url,
            {"scheduled_at": (timezone.now() + timedelta(days=5)).isoformat()},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_only_own_appointments(self):
        AppointmentFactory(
            professional=self.other_professional,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["professional"],
            self.professional.id,
        )

    def test_retrieve_own_appointment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.appointment.id)

    def test_cannot_retrieve_other_professional_appointment(self):
        other_appointment = AppointmentFactory(
            professional=self.other_professional,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/v1/appointments/{other_appointment.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_owner_can_update_appointment(self):
        self.client.force_authenticate(user=self.user)

        new_date = timezone.now() + timedelta(days=10)

        response = self.client.patch(
            self.detail_url,
            {"scheduled_at": new_date.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_appointment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_past_appointment_returns_400(self):
        self.client.force_authenticate(user=self.user)

        past_date = timezone.now() - timedelta(days=1)

        response = self.client.post(
            self.list_url,
            {"scheduled_at": past_date.isoformat()},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_appointment_time_returns_400(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.list_url,
            {"scheduled_at": (self.appointment.scheduled_at.isoformat())},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_filter_appointments_by_professional(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.list_url,
            {"professional": self.professional.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["professional"],
            self.professional.id,
        )

    def test_filter_other_professional_returns_empty_list(self):
        AppointmentFactory(
            professional=self.other_professional,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.list_url,
            {"professional": self.other_professional.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
