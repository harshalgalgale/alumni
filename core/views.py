from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from core.models import MainSector, SubSector
from core.serializers import MainSectorSerializer, SubSectorSerializer


class MainSectorViewSet(ModelViewSet):
    queryset = MainSector.objects.all()
    serializer_class = MainSectorSerializer
    permission_classes = (AllowAny,)


class SubSectorViewSet(ModelViewSet):
    queryset = SubSector.objects.all()
    serializer_class = SubSectorSerializer
    permission_classes = (AllowAny,)
