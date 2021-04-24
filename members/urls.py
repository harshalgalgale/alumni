from rest_framework import routers

from members.views import PersonalProfileViewSet

router = routers.DefaultRouter()
router.register('profile', PersonalProfileViewSet)

urlpatterns = []

urlpatterns += router.urls
