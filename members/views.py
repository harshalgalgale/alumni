from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from members.models import PersonalProfile
from members.serializers import PersonalProfileSerializer


class PersonalProfileViewSet(ModelViewSet):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = (AllowAny,)
