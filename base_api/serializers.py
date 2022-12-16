from rest_framework.serializers import ModelSerializer
from .models import Prclient

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Prclient
        fields = '__all__'
