from django.urls import path, include
from rest_framework import routers

from accounts.views import UserViewSet, RegisterView

router = routers.DefaultRouter()
router.register('users', UserViewSet)
# router.register('register', RegisterView.as_view())

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path('confirm-email/<str:user_id>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_email')
]

urlpatterns += router.urls
