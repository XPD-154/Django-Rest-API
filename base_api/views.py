from django.shortcuts import render
import requests
import json
import mysql.connector
from mysql.connector import Error
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Prclient, PrclientAPIKey
from .serializers import ClientSerializer
from client_api import settings
import xml.etree.ElementTree as ET
from .permissions import HasPrclientAPIKey

#needed variables
device_id = settings.device_id
callkit_token = settings.callkit_token
apns_token = settings.apns_token
token = settings.token
x_auth_token = settings.x_auth_token

host = settings.host
user = settings.user
password = settings.password
database = settings.database

'''
#connect to existing database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    autocommit=True
)

#cursor for execution of sql query
cur = connection.cursor(dictionary=True)

'''

# Create your views here.

#create custom api key django
@api_view()
@permission_classes([AllowAny])
def createClientApiKey(request,cid):
    #client_data = Prclient.objects.get(cluniqueid=request.data['clientid'])
    try:
        client_data = Prclient.objects.get(cluniqueid=cid)
    except Prclient.DoesNotExist:
        return Response({"status": "error", "message": "invalid client id"}, status=status.HTTP_404_NOT_FOUND)

    #api_key, key = PrclientAPIKey.objects.create_key(Prclient=client_data, cluniqueid=request.data['clientid'])
    api_key, key = PrclientAPIKey.objects.create_key(client_key=client_data, name=cid)
    return Response({'name':str(api_key), 'key': str(key)}, status=status.HTTP_201_CREATED)


@api_view(['GET']) #place request type here e.g GET, PUT, POST
def getRoutes(request):

    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/ :id'
    ]
    return Response(routes)

#for database table created in django and with api protection
@api_view(['GET'])
@permission_classes([HasPrclientAPIKey])
def getClients(request):
    client = Prclient.objects.all()
    serializer = ClientSerializer(client, many=True)
    return Response(serializer.data)

'''
example of api call for the above thats working
$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://127.0.0.1:8000/clients/',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_HTTPHEADER => array(
    'Authorization: Api-Key 05MwJyao.tBijLXQwmk7b39Uc3ZOLXrXmlPTM4YUx'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;

'''

#for database table created outside django (XML version)
@api_view(['GET'])
def checkClientXl(request):

    try:
      connection = mysql.connector.connect(
          host=host,
          user=user,
          password=password,
          database=database,
          autocommit=True
      )
      cur = connection.cursor(dictionary=True)

      unique_id = request.GET.get('unique_id', False);

      if unique_id:
          query = """SELECT * FROM Prclient WHERE CLuniqueId = %s"""
          params = (unique_id,)
          cur.execute(query, params)
          result = cur.fetchall()

          if result == []:
              data = f'<account><status>error</status><message>data not found</message></account>'
              element = ET.XML(data)
              ET.indent(element)
              params = ET.tostring(element, encoding='unicode')

              return HttpResponse(params, content_type="application/xml")
          else:
              email = result[0]['CLemail']
              name = result[0]['CLcompany_name']
              phone = result[0]['CLphone_number']

              data = f'<account><name>{name}</name><phone>{phone}</phone><email>{email}</email></account>'
              element = ET.XML(data)
              ET.indent(element)
              params = ET.tostring(element, encoding='unicode')

              return HttpResponse(params, content_type="application/xml")
      else:
          data = f'<account><status>error</status><message>incomplete data</message></account>'
          element = ET.XML(data)
          ET.indent(element)
          params = ET.tostring(element, encoding='unicode')

          return HttpResponse(params, content_type="application/xml")

    except Error as e:
        error_result = str(e)
        return Response({"status": "error", "message": error_result}, status=status.HTTP_404_NOT_FOUND)

#for database table created outside django (JSON version)
@api_view(['GET'])
def checkClientJs(request):

    try:
      connection = mysql.connector.connect(
          host=host,
          user=user,
          password=password,
          database=database,
          autocommit=True
      )
      cur = connection.cursor(dictionary=True)

      unique_id = request.GET.get('unique_id', False);

      if unique_id:
          query = """SELECT * FROM Prclient WHERE CLuniqueId = %s"""
          params = (unique_id,)
          cur.execute(query, params)
          result = cur.fetchall()

          if result == []:
              return Response({"status": "error", "message": "data not found"}, status=status.HTTP_404_NOT_FOUND)
          else:
              #email = result[0]['CLemail']
              #return Response({"email": email, "message": "data found"})
              return HttpResponse(json.dumps(result, indent=4), content_type="application/json")

      else:
          return Response({"status": "error", "message": "data incomplete"}, status=status.HTTP_404_NOT_FOUND)

    except Error as e:
        error_result = str(e)
        return Response({"status": "error", "message": error_result}, status=status.HTTP_404_NOT_FOUND)



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
#http://127.0.0.1:8000/specific_client/?id=9&uid=cl009
@api_view()
@permission_classes([AllowAny])
def getSpClient(request):

    #print(request.query_params)
    #print(request.query_params['id'])

    SpClientId = request.GET.get('id', False);
    SpClientUId = request.GET.get('uid', False);

    if SpClientId and SpClientUId:
      try:
          Prclient.objects.get(clientid=SpClientId, cluniqueid=SpClientUId)
      except Prclient.DoesNotExist:
          return Response({"status": "error", "message": "data not found"}, status=status.HTTP_404_NOT_FOUND)

      client = Prclient.objects.get(clientid=SpClientId, cluniqueid=SpClientUId)
      serializer = ClientSerializer(client, many=False)
      return Response(serializer.data)
    else:
      return Response({"status": "error", "message": "incomplete data"}, status=status.HTTP_404_NOT_FOUND)

#call API inside API
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
