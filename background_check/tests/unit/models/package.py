import unittest
from background_check.models import Background_check, Package
from background_check.factories import BGC__us_one_validate
from background_check.adapter.bgc.us_one_validate import (
    Adapter as BGC_us_one_validate_adapter
)


class Test_background_check_get_adapter( unittest.TestCase ):
    def test_bgc_us_one_validate( self ):
        background_check = BGC__us_one_validate.build()
        adapter = background_check.get_adapter()
        self.assertIsInstance( adapter, BGC_us_one_validate_adapter )
