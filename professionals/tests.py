from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ProfessionalFactory


class ProfessionalAPITestCase(APITestCase):
    def setUp(self):
        self.professional = ProfessionalFactory()
        self.user = self.professional.user

        self.other_professional = ProfessionalFactory()

        self.list_url = "/api/v1/professionals/"
        self.detail_url = f"/api/v1/professionals/{self.professional.id}/"

    def test_create_professional(self):
        data = {
            "user": {
                "username": "mariana",
                "email": "mariana@example.com",
                "password": "TestPassword123!",
            },
            "social_name": "Mariana Oliveira",
            "profession": "Psicologia",
            "address": "Rua das Flores, 123",
            "contact": "11999998888",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["social_name"], "Mariana Oliveira")

    def test_list_professionals(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_professional(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["social_name"],
            self.professional.social_name,
        )

    def test_owner_can_update_professional(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.detail_url,
            {"profession": "Psiquiatria"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profession"], "Psiquiatria")

    def test_other_user_cannot_update_professional(self):
        self.client.force_authenticate(
            user=self.other_professional.user,
        )

        response = self.client.patch(
            self.detail_url,
            {"profession": "Psiquiatria"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_professional(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_create_professional_with_missing_data_returns_400(self):
        data = {
            "user": {
                "username": "incomplete",
                "email": "incomplete@example.com",
                "password": "TestPassword123!",
            },
            "social_name": "Mariana",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_professional_with_invalid_contact_returns_400(self):
        data = {
            "user": {
                "username": "invalidcontact",
                "email": "invalid@example.com",
                "password": "TestPassword123!",
            },
            "social_name": "Mariana",
            "profession": "Psicologia",
            "address": "Rua das Flores, 123",
            "contact": "telefone-invalido",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
