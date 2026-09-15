from django.db import models

from professionals.models import Professional


class Appointment(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    scheduled_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_at", "id"]

        constraints = [
            models.UniqueConstraint(
                fields=["professional", "scheduled_at"],
                name="unique_professional_appointment_time",
            ),
        ]

        indexes = [
            models.Index(
                fields=["professional", "scheduled_at"],
                name="appointment_prof_date_idx",
            ),
        ]

    def __str__(self):
        return f"{self.professional.social_name} - {self.scheduled_at}"
