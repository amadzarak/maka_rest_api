# apis/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('getuser/<str:uid>', getUser),
    path('getprofile/<str:uid>', getFullProfile)
]