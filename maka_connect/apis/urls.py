# apis/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('getuser/<str:uid>', getUser),
    path('getprofile/<str:uid>', getFullProfile),
    path('matches/<str:uid>/', getUserMatches),
    path('sentlikes/<str:uid>/', getUsersLikeSent),
    path('recievedlikes/<str:uid>/', getUsersLikeRecieved),
    path('checkin/<str:eid>', getGuestsInEvent),
    path('checkin/', checkInEvent),
    path('checkinstatus/', checkInStatus),
    path('events/', EventList.as_view()),
    path('events/<int:pk>/', EventDetail.as_view()),
    path('venues/', VenueList.as_view()),
    path('address/<int:id>/', getAddress),
    path('venues/<int:pk>/', VenueDetail.as_view()),
    path('likeuser/', likeUser),
    path('unlikeuser/', unlikeUser),
    path('keypersons/', KeyPersons.as_view()),
    path('interactionstatus/', checkUserInteractionExists),
    path('matchstatus/', checkMatchStatus),
    path('createprofile/', createProfileV1),
    path('createprofile/', send_user_alerts),
]

