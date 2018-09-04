from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()

router.register( r'packages', views.Package, base_name='packages' )
router.register( r'profiles', views.Profile, base_name='profiles' )

check_router = routers.NestedSimpleRouter(
    router, r'packages', lookup='package' )
check_router.register( r'check', views.Check, base_name='check' )

urlpatterns = router.urls + check_router.urls
