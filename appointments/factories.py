from datetime import timedelta

import factory
from django.utils import timezone

from professionals.factories import ProfessionalFactory

from .models import Appointment


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    professional = factory.SubFactory(ProfessionalFactory)
    scheduled_at = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1))
