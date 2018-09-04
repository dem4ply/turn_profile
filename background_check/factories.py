from nucling.snippet import madness
from faker import Factory as Faker_factory
from .models import (
    Sub_profile as Sub_profile_model,
    Profile as Profile_model,
    Package as Package_model,
    Background_check as Background_check_model,
)
from partners.factories import Partner
import factory


faker = Faker_factory.create()


class Profile( factory.Factory ):
    meta = factory.Dict(
        { 'id': factory.lazy_attribute(
            lambda x: madness.generate_b64_unsecure() ) } )

    class Meta:
        model = Profile_model


class Sub_profile( factory.Factory ):
    response = factory.lazy_attribute( lambda x: faker.pydict() )
    raw_response = factory.lazy_attribute( lambda x: faker.pydict() )
    source = factory.lazy_attribute( lambda x: ".".join( faker.words() ) )

    class Meta:
        model = Sub_profile_model


class Sub_profile_empty( Sub_profile ):
    response = None
    raw_response = None


class Sub_profile_with_list( Sub_profile ):
    response = factory.lazy_attribute( lambda x: faker.pylist() )
    raw_response = factory.lazy_attribute( lambda x: faker.pylist() )


class Background_check( factory.DjangoModelFactory ):
    name = factory.lazy_attribute(
        lambda x: faker.sentence(
            nb_words=5, variable_nb_words=True, ext_word_list=None ) )
    adapter = 'bgc'

    class Meta:
        model = Background_check_model


class Package( factory.DjangoModelFactory ):
    name = factory.lazy_attribute(
        lambda x: faker.sentence(
            nb_words=5, variable_nb_words=True, ext_word_list=None ) )
    partner = factory.SubFactory( Partner )

    class Meta:
        model = Package_model


class BGC__us_one_validate( Background_check ):
    adapter = 'bgc.us_one_validate'

class BGC__us_one_trace( Background_check ):
    adapter = 'bgc.us_one_trace'
