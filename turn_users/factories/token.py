from factory import fuzzy
from faker import Factory as Faker_factory
from turn_users.models import Token as Token_model
from datetime import date
import factory

from nucling.snippet.madness import generate_token


faker = Faker_factory.create()
start_date = date( 2016, 1, 1 )


class Token( factory.DjangoModelFactory ):
    user = factory.SubFactory( 'turn_users.factories.User' )
    key = factory.lazy_attribute( lambda x: generate_token( 20 ) )
    create_at = fuzzy.FuzzyDate( start_date )

    class Meta:
        model = Token_model
