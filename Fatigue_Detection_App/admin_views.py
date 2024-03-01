from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer

from Fatigue_Detection_App.models import CustomUser, Admin, Worker, Fatigue_State
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from Fatigue_Detection_App.EmailBackEnd import EmailBackEnd
import requests
# settings 
from django.conf import settings

from pytz import timezone as tz

import random

#email
from django.core.mail import send_mail

# Admin Home Dashboard
class Admin_home(APIView):

    def get(self, request):
        if request.user.user_type == '1':
            # calculate number of Workers
            workers = Worker.objects.all()

            context = {
                'workers': workers,
            }

            return render(request, 'admin/admin_home.html', context)
        else:
            return redirect('login')


# View Worker
class View_worker(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, worker_uuid):
        if request.user.user_type == '1':
            worker = Worker.objects.get(worker_uuid=worker_uuid)
            worker_custom_user = CustomUser.objects.get(id=worker.user_id)
            
            # fatigue_levels = ["No Fatigue", "Low Fatigue", "Medium Fatigue"]
            # rand_idx = random.randint(1, len(fatigue_levels)-1)
            # current_fatigue = fatigue_levels[rand_idx]
            # print(worker_custom_user.last_login)
        
            # print(type(worker_custom_user.last_login))
            # print(datetime.now().replace(tzinfo=tz('Asia/Kolkata'))-worker_custom_user.last_login)
            # #dateA = dateA.replace(tzinfo=tz('UTC'))
            # if worker.last_fatigue_state == None:
            #     worker.last_fatigue_state = worker_custom_user.last_login
            #     worker.save()
                
            # diff=datetime.now().replace(tzinfo=tz('Asia/Kolkata'))-worker.last_fatigue_state
            
            # if diff.total_seconds()/60 > 15.0: 
            #     fatigue_state= Fatigue_State.objects.create(fatigue_state_worker=worker,fatigue_state=current_fatigue)
            #     worker.last_fatigue_state=datetime.now().replace(tzinfo=tz('Asia/Kolkata'))
            #     worker.save()

            # # sending mail to admin
            # if current_fatigue == "Medium Fatigue" or current_fatigue == "High Fatigue"
            #     subject = f'{current_fatigue} Detected for {worker_custom_user.first_name} {worker_custom_user.last_name}'
            #     message = f'Dear Admin, {current_fatigue} Detected for {worker_custom_user.first_name} {worker_custom_user.last_name} at {worker.last_fatigue_state}.'
            #     email_from = settings.EMAIL_HOST_USER
            #     recipient_list = ["	parijatgd@gmail.com","roybiparnak@gmail.com" ]
            #     send_mail( subject, message, email_from, recipient_list )
            #     # sending mail to admin
            #     if current_fatigue == "Medium Fatigue" or current_fatigue == "High Fatigue":
            #         subject = f'{current_fatigue} Detected for {worker_custom_user.first_name} {worker_custom_user.last_name}'
            #         message = f'Dear Admin, {current_fatigue} Detected for {worker_custom_user.first_name} {worker_custom_user.last_name} at {worker.last_fatigue_state.replace(tzinfo=tz("Asia/Kolkata"))}.'
            #         email_from = settings.EMAIL_HOST_USER
            #         recipient_list = ["	parijatgd@gmail.com","roybiparnak@gmail.com" ]
            #         send_mail( subject, message, email_from, recipient_list )



            fatigue_states = Fatigue_State.objects.filter(fatigue_state_worker=worker).order_by('-fatigue_state_created_at')
            context = {
                'worker': worker_custom_user,
                "fatigue_states" : fatigue_states
            }
            return render(request, 'admin/admin_view_worker.html', context)
        else:
            return redirect('login')

