import uuid

import factory

from .models import PhoneNumber as PhoneNumberModel


class PhoneNumberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneNumberModel

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker('name')
    number = factory.Faker('phone_number')
