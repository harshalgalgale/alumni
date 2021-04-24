from rest_framework import routers

from students.views import StudentViewSet

router = routers.DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = []

urlpatterns += router.urls
