from faker import Factory as Faker_factory
from .models import Partner as Partner_model
from turn_users.factories import User
import factory


faker = Faker_factory.create()


class Partner( factory.DjangoModelFactory ):
    name = factory.lazy_attribute( lambda x: faker.company() )
    user = factory.SubFactory( User )

    class Meta:
        model = Partner_model
