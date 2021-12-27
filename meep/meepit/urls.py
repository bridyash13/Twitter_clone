from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup',views.SignUp,name='Signup'),
    path('login',obtain_auth_token,name='Login'),
    path('meep',views.CreateMeep, name='Meep'),
    path('follow/<str:uname>',views.FollowPerson,name='Follow'),
    path('feed',views.LoadMeeps,name='Feed')
]