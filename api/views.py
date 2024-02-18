from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from django.core import serializers
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer

from Fatigue_Detection_App.models import CustomUser, Admin, Worker
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from Fatigue_Detection_App.EmailBackEnd import EmailBackEnd
import requests
# settings 
from django.conf import settings
from django.middleware.csrf import *

from rest_framework_simplejwt.tokens import RefreshToken 




# Create your views here.
@csrf_exempt
def persistent_login(request):
    if request.method == 'POST':
        _request = json.loads(request.body)
        print(_request)
        username = _request['username']
        device_token = _request['deviceToken']

        user=CustomUser.objects.filter(email=username)[0]
        print(user)
        if user is not None:
            login(request,user)
            jwt_token = RefreshToken.for_user(user)
            actual_data={
                    "body":{
                        "user": {
                            "firstName" : user.first_name,
                            "lastName" : user.last_name,
                            "email" : user.email,
                            "userName" : user.username,
                            "password" : user.password,
                            "reportingAuthEmail" : user.worker.supervisor_email,
                            "deviceToken" : device_token,
                        },
                        "jwt" : str(jwt_token.access_token)
                    },
                    "status": "success",
                    "timeStamp" : str(datetime.timestamp)
     
                }
            return HttpResponse(json.dumps(actual_data)) 
        else:
            return HttpResponse("ERROR:-Credentials are Incorrect")
    else:
        HttpResponse("ERROR")


@csrf_exempt
def Login(request):
    if request.method == 'POST':
        _request = json.loads(request.body)
        email = _request['email']
        device_token = _request['deviceToken']
        password = _request['password']
        user=EmailBackEnd.authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            jwt_token = RefreshToken.for_user(user)
            actual_data={
                    "body":{
                        "user": {
                            "firstName" : user.first_name,
                            "lastName" : user.last_name,
                            "email" : user.email,
                            "userName" : user.username,
                            "password" : user.password,
                            "reportingAuthEmail" : user.worker.supervisor_email,
                            "deviceToken" : device_token,
                        },
                        "jwt" : str(jwt_token.access_token)
                    },
                    "status": "success",
                    "timeStamp" : str(datetime.timestamp)
     
                }
            return HttpResponse(json.dumps(actual_data)) 
        else:
            return HttpResponse("ERROR:-Credentials are Incorrect")
    else:
        HttpResponse("ERROR")

@csrf_exempt
def Signgup(request):
    '''
    {"firstName":"Biparnak ","lastName":"Roy","userName":"biparnak","reportingAuthEmail":"admin@admin.com","picture":"imgurl","email":"roybiparnak@gmail.com","password":"d033e22ae348aeb5660fc2140aec35850c4da997","deviceToken":"ffr5Ejv3Sw6CNSToyP4rjx:APA91bGW4aEYj15tiESCXogVkdi3rA9VEmN1lUmYFNf7ZHH4pgExpNtIdnVCVO-QhHf_8QhAn0peEJ9AQJV5WdfOIAVC7sa5i5jTxq6IgU_kpG7K5cjngR3Fpgi5QCW0p6D-7wyqCugx","roles":"USER"}
    '''
    request = json.loads(request.body)
    first_name = request['firstName']
    last_name = request['lastName']
    email = request['email']
    username = request['userName']
    supervisor_email = request['reportingAuthEmail']
    device_token = request['deviceToken']
    password = request['password']

    user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
    user.worker.supervisor_email=supervisor_email
    user.worker.device_token = device_token
    #user.worker.jwt = str(uuid.uuid4())
    user.last_login = datetime.now()
    user.save()
    jwt_token = RefreshToken.for_user(user)
    actual_data={
        "body":{
            "firstName" : user.first_name,
            "lastName" : user.last_name,
            "email" : user.email,
            "userName" : user.username,
            "password" : user.password,
            "reportingAuthEmail" : user.worker.supervisor_email,
            "deviceToken" : user.worker.device_token,
            "jwt" : str(jwt_token.access_token)
        },
        "status": "success",
        "timeStamp" : str(datetime.timestamp)
     
    }

    return HttpResponse(json.dumps(actual_data)) 

@csrf_exempt
def display(request):
    if request.method == 'GET':
        user    = CustomUser.objects.filter(pk = request.user.pk)[0]
        profile = Worker.objects.filter(user = request.user.pk)[0]
        return HttpResponse(serializers.serialize('json',[user,profile])) 

@csrf_exempt
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return HttpResponse("ERROR:-Error Logging Out")



