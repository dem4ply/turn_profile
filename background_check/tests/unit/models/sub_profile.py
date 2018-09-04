import unittest
from unittest.mock import patch
from background_check.models import Sub_profile as Sub_profile_model
from background_check.factories import Sub_profile as Sub_profile_factories
from datetime import datetime


class Test_sub_profile_model( unittest.TestCase ):

    @patch( 'elasticsearch_dsl.Document.save' )
    def test_save_should_set_created_at( self, save ):
        sub_profile = Sub_profile_factories.build()
        self.assertIsNone( sub_profile.created_at )
        sub_profile.save()
        self.assertIsInstance( sub_profile.created_at, datetime )


class Test_sub_profile_model_encode( unittest.TestCase ):
    def test_encode_obj_dict_should_return_a_str( self ):
        obj = { 'int': 1, 'str': 'str', 'float': 1.0 }
        result = Sub_profile_model._encode_obj( obj )
        self.assertIsInstance( result, str )
        self.assertTrue( result )
        return result

    def test_decode_string_obj_str_was_a_dict_should_return_a_dict( self ):
        obj_str = self.test_encode_obj_dict_should_return_a_str()
        result = Sub_profile_model._decode_obj( obj_str )
        self.assertIsInstance( result, dict )
        self.assertTrue( result )

    def test_encode_obj_list_should_return_a_str( self ):
        obj = [ 'sdf', 1, 4.95, datetime.utcnow() ]
        result = Sub_profile_model._encode_obj( obj )
        self.assertIsInstance( result, str )
        self.assertTrue( result )
        return result

    def test_decode_string_obj_str_was_a_list_should_return_a_list( self ):
        obj_str = self.test_encode_obj_list_should_return_a_str()
        result = Sub_profile_model._decode_obj( obj_str )
        self.assertIsInstance( result, list )
        self.assertTrue( result )

    def test_encode_none_should_return_a_none( self ):
        obj = None
        result = Sub_profile_model._encode_obj( obj )
        self.assertIsNone( result )
        return result

    def test_decode_none_should_return_none( self ):
        obj_str = self.test_encode_none_should_return_a_none()
        result = Sub_profile_model._decode_obj( obj_str )
        self.assertIsNone( result )
