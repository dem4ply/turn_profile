from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()

router.register( r'partners', views.Partner, base_name='partners' )


urlpatterns = router.urls
