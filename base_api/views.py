from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
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
    try:
        Prclient.objects.get(clientid=pk)
    except Prclient.DoesNotExist:
        return Response({"status": "error", "message": "data not found"}, status=status.HTTP_404_NOT_FOUND)

    client = Prclient.objects.get(clientid=pk)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)

'''
//view specific record in table
$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.10.22:8000/client/4',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_HTTPHEADER => array(
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

curl_close($curl);

$tran = json_decode($response, true);

print "<pre>";
print_r($tran);
print "</pre>";
'''

@api_view(['POST'])
def addClient(request):

    # validating for already existing data
    if Prclient.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    client = ClientSerializer(data=request.data)

    if client.is_valid():
        client.save()
        return Response(client.data)
    else:
        return Response({"status": "error", "data": client.errors}, status=status.HTTP_400_BAD_REQUEST)

'''
//create a record in the table
$postData = [
    "clemail" => "TEST22",
    "clpassword" => "TEST22",
    "clcompany_name" => "TEST22",
    "clphone_number" => "TEST22",
    "cluniqueid" => "TEST22"
];

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.10.31:8000/create_client/',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS => json_encode($postData),
  CURLOPT_HTTPHEADER => array(
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

curl_close($curl);

$tran = json_decode($response, true);

print "<pre>";
print_r($tran);
print "</pre>";
'''

@api_view(['POST'])
def updateClient(request, pk):
    client = Prclient.objects.get(clientid=pk)
    item = ClientSerializer(client, data = request.data, partial=True)

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response({"status": "error", "data": item.errors}, status=status.HTTP_400_BAD_REQUEST)

'''
//update script. Select only the columns you need to update, append the id in the url
$postData = [
    "clemail" => "TEST22@univasa",
    "clpassword" => "TEST22",
    "cluniqueid" => "TEST54"
];

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.10.31:8000/update_client/13',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS => json_encode($postData),
  CURLOPT_HTTPHEADER => array(
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

curl_close($curl);

$tran = json_decode($response, true);

print "<pre>";
print_r($tran);
print "</pre>";
'''

@api_view(['DELETE'])
def deleteClient(request, pk=None):
    item = get_object_or_404(Prclient, clientid=pk)
    item.delete()
    return Response({"status": "success", "data": "Record Deleted"}, status=status.HTTP_202_ACCEPTED)

'''
//delete script via the id
$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.10.31:8000/delete_client/12',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'DELETE',
));

$response = curl_exec($curl);

curl_close($curl);

$tran = json_decode($response, true);

print "<pre>";
print_r($tran);
print "</pre>";
'''

#pass multiple parameters into url
@api_view()
@permission_classes([AllowAny])
def getSpClient(request):

    print(request.query_params)
    print(request.query_params['id'])

    SpClientId = request.GET.get('id', False);
    SpClientUId = request.GET.get('uid', False);

    try:
        Prclient.objects.get(clientid=SpClientId, cluniqueid=SpClientUId)
    except Prclient.DoesNotExist:
        return Response({"status": "error", "message": "data not found"}, status=status.HTTP_404_NOT_FOUND)

    client = Prclient.objects.get(clientid=SpClientId, cluniqueid=SpClientUId)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)

@api_view()
@permission_classes([AllowAny])
def login_test(request):

    #params from url
    username = request.GET.get('username', False);
    password = request.GET.get('password', False);

    #api url
    login_url = "https://ubx.univasa.com/api/login/"

    #data to passed to url
    postData = {
        "username": username,
        "password": password,
        "device_id": "645C18B55-26C-4504-AADF-034BDFE1AFEA1",
        "callkit_token": "BE6CAF775FFC2C1AAD28D9992E467156F044D68D21C59E4973C3A692DACAB03C",
        "apns_token": "63c7620a2c5ce0a1717850ecb559fb994c57bc6180f49c2e815efab09421f924",
        "mobile_type": "Ios"
    }

    #info to be passed to header
    headers = {'x-auth-token': 'mzFxYakJRhZ8e6nEqMnhvLBVsVpFVj'}

    response = requests.post(login_url, json=postData, headers=headers)
    result = response.json()

    acct_id = result['data']['accountid']
    cust_token = result['data']['token']

    #return HttpResponse(json.dumps(result), content_type="application/json")
    return Response({"accountid": acct_id, "customer token": cust_token})
