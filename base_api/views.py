from django.shortcuts import render
import requests
import json
import mysql.connector
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Prclient
from .serializers import ClientSerializer
from client_api import settings

# Create your views here.

device_id = settings.device_id
callkit_token = settings.callkit_token
apns_token = settings.apns_token
token = settings.token
x_auth_token = settings.x_auth_token

#connect to existing database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="preq",
    autocommit=True
)

#cursor for execution of sql query
cur = connection.cursor(dictionary=True)


@api_view(['GET']) #place request type here e.g GET, PUT, POST
def getRoutes(request):

    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/ :id'
    ]
    return Response(routes)

#for database table created in django
@api_view(['GET'])
def getClients(request):
    client = Prclient.objects.all()
    serializer = ClientSerializer(client, many=True)
    return Response(serializer.data)

#for database table created outside django
@api_view(['GET'])
def checkClient(request):
    unique_id = request.GET.get('unique_id', False);
    if unique_id:
        query = """SELECT * FROM Prclient WHERE CLuniqueId = %s"""
        params = (unique_id,)
        cur.execute(query, params)
        result = cur.fetchall()

        if result == []:
            return Response({"status": "error", "message": "data not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            email = result[0]['CLemail']
            #return HttpResponse(json.dumps(us_record, indent=4), content_type="application/json")
            return Response({"email": email, "device id": device_id, "message": "data found"})
    else:
        return Response({"status": "error", "message": "data incomplete"}, status=status.HTTP_404_NOT_FOUND)

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

    if username and password:

        # first API call #
        #api url
        login_url = "https://ubx.univasa.com/api/login/"

        #data to passed to url
        postData = {
            "username": username,
            "password": password,
            "device_id": device_id,
            "callkit_token": callkit_token,
            "apns_token": apns_token,
            "mobile_type": "Ios"
        }

        #info to be passed to header
        headers = {'x-auth-token': x_auth_token}

        response = requests.post(login_url, json=postData, headers=headers)
        result = response.json()

        acct_id = result['data']['accountid']
        cust_token = result['data']['token']
        cust_number = result['data']['telephone_1']

        # end of first API call #

        # second API call #
        login_url_1 = "https://ubx.univasa.com/admin/origination_rate/"

        postData_1 = {
            "id":"1",
            "token":token,
            "action":"origination_list",
            "object_where_params": {
              "pattern": cust_number,
              "country_id": "",
              "destination": "",
              "connectcost": "",
              "includedseconds": "",
              "cost": "",
              "init_inc": "",
              "inc": "",
              "reseller_id": "",
              "pricelist_id": "",
              "status": ""
            },
            "start_limit": "1",
            "end_limit": "2"
        }

        response_1 = requests.post(login_url_1, json=postData_1, headers=headers)
        result_1 = response_1.json()

        cust_rate = result_1['data'][0]['cost']

        # end of second API call #

        #return HttpResponse(json.dumps(result_1, indent=4), content_type="application/json")
        return Response({"accountid": acct_id, "customer token": cust_token, "call rate": cust_rate, "mobile number": cust_number})
    else:
        return Response({"status": "error", "message": "data incomplete"}, status=status.HTTP_404_NOT_FOUND)
