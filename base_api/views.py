from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prclient
from .serializers import ClientSerializer

# Create your views here.
@api_view(['GET']) #place request type here e.g GET, PUT, POST
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/ :id'
    ]
    return Response(routes)

@api_view(['GET'])
def getClients(request):
    client = Prclient.objects.all()
    serializer = ClientSerializer(client, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getClient(request, pk):
    client = Prclient.objects.get(clientid=pk)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)
