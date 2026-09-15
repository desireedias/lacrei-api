from django.db import models

from core import settings


class Professional(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile",
    )
    social_name = models.CharField(max_length=150)
    profession = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Meta:
    ordering = ["social_name"]


def __str__(self):
    return f"{self.social_name} ({self.profession})"
