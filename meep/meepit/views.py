from http.client import ACCEPTED
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import UserModel, Meep
from .serializers import FollowerSerializer, UserSerializer, MeepSerializer, MeepFeedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
import json

from meepit import serializers

# Create your views here.
@api_view(['POST',])
@permission_classes((AllowAny,))
def SignUp(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "User registration successful"
            data['email'] = user.email
            data['uname'] = user.uname
            token = Token.objects.get(user=user).key
            data['token'] = token
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def CreateMeep(request):

    if request.method == 'POST':
        user = request.user
        serializer = MeepSerializer(data = request.data,context={'userid': user.id})
        data = {}
        if serializer.is_valid():
            meep = serializer.save()
            data['response'] = "Meep successfully created"
            data['meeptext'] = meep.meeptext
            data['user'] = str(user)
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def FollowPerson(request,uname):
    
    if request.method == 'POST':
        user = request.user
        serializer = FollowerSerializer(data = request.data,context={'userid':user.id,'person':uname})
        data = {}
        if serializer.is_valid():
            follower = serializer.save()
            data['response'] = "Follow successful"
            data['Follower'] = str(follower.follower)
            data['Followed Person'] = str(follower.person)
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def LoadMeeps(request):
    if request.method == 'GET':
        user = request.user
        meeps = MeepFeedSerializer(data=request.data,context={'userid':user.id})
        meepit = meeps.save()
        l = []
        if meeps.is_valid():
            for i in meepit:
                l.append(str(i.userid)+": "+str(i.meeptext))
            return JsonResponse(l,safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(meeps.errors, status=status.HTTP_400_BAD_REQUEST)
