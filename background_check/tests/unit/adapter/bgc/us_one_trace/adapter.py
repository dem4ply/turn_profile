
import unittest
from unittest.mock import patch, Mock, ANY
from tetrapod.bgc.factories.us_one_validate import (
    Us_one_trace as Us_one_trace_factory,
)
from background_check.models import Sub_profile
from background_check.adapter.bgc.us_one_trace import Adapter
from rest_framework.exceptions import ValidationError
from vcr_unittest import VCRTestCase


class Test_validate( unittest.TestCase ):
    def setUp( self ):
        self.adapter = Adapter()

    def test_should_no_accept_less_to_9_chars( self ):
        with self.assertRaises( ValidationError ):
            self.adapter.validate(
                ssn='12345678', first_name='jonh', last_name='doe' )

    def test_should_no_accept_less_to_9_chars_asdf( self ):
        with self.assertRaises( ValidationError ):
            self.adapter.validate(
                ssn='12345678', first_name='jonh', last_name='doe' )

    def test_if_send_more_data_not_care( self ):
        result = self.adapter.validate(
                ssn='123456789', first_name='jonh', last_name='doe',
                asdf = 'asdf' )
        self.assertDictEqual(
            result,
            { 'ssn': '123456789', 'first_name': 'jonh', 'last_name': 'doe' } )

    def test_if_raise_exception_is_false_should_return_all_errors( self ):
        errors = self.adapter.validate(
            ssn='1234567890', raise_exception=False )
        self.assertEqual(
            errors[ 'ssn' ][0],
            'Ensure this field has no more than 9 characters.' )
