from rest_framework import routers

from core.views import MainSectorViewSet, SubSectorViewSet

router = routers.DefaultRouter()
router.register('main-sector', MainSectorViewSet)
router.register('sub-sector', SubSectorViewSet)

urlpatterns = []

urlpatterns += router.urls
