from rest_framework.serializers import ModelSerializer
from .models import Prclient

'''
class ClientSerializer(ModelSerializer):
    class Meta:
        model = Prclient
        fields = '__all__'
'''

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Prclient
        fields = ('clemail', 'clpassword', 'clcompany_name', 'clphone_number', 'cluniqueid')
