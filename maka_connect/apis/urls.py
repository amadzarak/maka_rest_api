# apis/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('getuser/<str:uid>', getUser),
    path('getprofile/<str:uid>', getFullProfile),
    path('sentlikes/<str:uid>/', getUsersLikeSent),
    path('checkin/<str:eid>', getGuestsInEvent),
    path('checkin/', checkInEvent),
    path('checkinstatus/', checkInStatus),
    path('events/', EventList.as_view()),
    path('events/<int:pk>/', EventDetail.as_view()),
    path('venues/', VenueList.as_view()),
    path('address/<int:id>/', getAddress),
    path('venues/<int:pk>/', VenueDetail.as_view()),
    path('likeuser/', likeUser),
    path('keypersons/', KeyPersons.as_view())
]

