# apis/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from maka.models import *
from .serializers import *


@api_view(['GET'])
def getUser(request, uid):
    users = User.objects.get(pk=uid)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getFullProfile(request, uid):
    user = User.objects.get(pk=uid)
    profile = Profile.objects.get(user=uid)
    conversation_topics = ConversationStarters.objects.filter(user=uid)
    return Response({"user": UserSerializer(user, many=False).data, 
                     "profile": ProfileSerializer(profile, many=False).data, 
                     "conversation_starters": ConversationStarterSerializer(conversation_topics, many=True).data})

@api_view(['POST'])
def checkInEvent(request, uid, event_id):
    event = Event.objects.get(pk=event_id)

    if (event.is_ticketed is True):
        ticket = Ticket.objects.get(user=uid, event=event_id)
        if ticket.is_valid():
            return Response({"Error": "Ticket not Found"})
        else:
            return Response({"Status": "Ticket Verified"})
        
        