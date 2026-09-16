import factory

from users.factories import UserFactory

from .models import Professional


class ProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Professional

    user = factory.SubFactory(UserFactory)
    social_name = factory.Sequence(lambda n: f"Profissional {n}")
    profession = "Psicologia"
    address = "Rua de Teste, 123"
    contact = "11999998888"
