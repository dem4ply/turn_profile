import unittest
from unittest.mock import patch, Mock, ANY
from tetrapod.bgc.factories.us_one_validate import (
    Us_one_trace as Us_one_trace_factory,
)
from background_check.models import Sub_profile
from background_check.adapter.bgc.us_one_trace import Adapter
from rest_framework.exceptions import ValidationError
from vcr_unittest import VCRTestCase


class Test_run( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.adapter = Adapter()
        self.factory = 'default'

    def test_when_run_the_instance_should_call_funtion_run( self ):
        self.adapter.run = Mock()
        self.adapter( 'a', asdf='q' )
        self.adapter.run.assert_called_with( 'a', asdf='q' )

    def test_run_should_return_a_sub_profile( self ):
        result = self.adapter(
            ssn='123456789', first_name='jonh', last_name='doe',
            _use_factory=self.factory )
        self.assertIsInstance( result, Sub_profile )

    def test_the_result_should_have_the_source( self ):
        result = self.adapter(
            ssn='123456789', first_name='jonh', last_name='doe',
            _use_factory=self.factory )
        self.assertEqual( result.source, self.adapter.source )
