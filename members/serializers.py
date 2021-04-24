from rest_framework.serializers import ModelSerializer

from members.models import PersonalProfile


class PersonalProfileSerializer(ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = '__all__'
