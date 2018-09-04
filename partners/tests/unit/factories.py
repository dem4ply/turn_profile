import unittest
from partners.factories import Partner as Partner_factory
from partners.models import Partner as Partner_model


class Test_Partner_factories( unittest.TestCase ):
    def test_should_work( self ):
        partner = Partner_factory.build()
        self.assertIsInstance( partner, Partner_model )
