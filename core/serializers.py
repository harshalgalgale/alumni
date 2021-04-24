from rest_framework.serializers import ModelSerializer

from core.models import MainSector, SubSector


class MainSectorSerializer(ModelSerializer):
    class Meta:
        model = MainSector
        fields = '__all__'


class SubSectorSerializer(ModelSerializer):
    class Meta:
        model = SubSector
        fields = '__all__'
