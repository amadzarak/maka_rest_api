# apis/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from maka.models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

import geocoder
import dateparser
###
#    CLASS BASED VIEWS
###

class EventList(APIView):
    """
    List all Events, or create a new Event
    """
    def get(self, request, format=None):
        events = Event.objects.all()
        event_serializer = EventSerializer(events, many=True)
        return Response(event_serializer.data)
    
    def post(self, request, format=None):
        print(request.data)
        data = request.data
        event_serializer = EventSerializer(data=data)
        try:
            event_type = EventType.objects.get(name=data['event_type']['name'])
        except ObjectDoesNotExist:
            newEventType = EventType.objects.create(**data['event_type'])
            print(newEventType.id)
            data['event_type'] = newEventType.id
        else:
            data['event_type'] = event_type.id

        if (event_serializer.is_valid()):
            n = event_serializer.save()
            EventDate.objects.create(event_id=n.id, **data['event_date'])
            EventUser.objects.create(event_id=n.id, **data['event_user'])
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KeyPersons(APIView):
    def post(self, request, format=None):
        print(request.data)
        data = request.data
        key_person_serializer = KeyPersonSerializer(data=data)
        try:
            key_person = KeyPerson.objects.get(phone=data['phone'])
        except ObjectDoesNotExist:
            KeyPerson.objects.create(**data)
        else:
            return Response(key_person_serializer.data, status=200)
        
        if (key_person_serializer.is_valid()):
            key_person_serializer.save()
            return Response(key_person_serializer.data, status=status.HTTP_201_CREATED)




class VenueList(APIView):
    def get(self, request, format=None):
        venues = Venue.objects.all()
        venue_serializer = VenueSerializer(venues, many=True)
        return Response(venue_serializer.data)

    def post(self, request, format=None):
        print(request.data)
        data = request.data
        venue_serializer = VenueSerializer(data=data)

        address_serializer = AddressSerializer(data=data['address'])

        try:
            address = Address.objects.get(address_line_1=data['address']['address_line_1'],
            address_line_2= data['address']['address_line_2'] if data['address']['address_line_2'] is not None else "",
            city=data['address']['city'],
            state=data['address']['state'],
            zip=data['address']['zip'],
            )
        except ObjectDoesNotExist:
            #calculateCoordinates(data['address'].values())
            Address.objects.create(**data['address'])
            
        else:
            data['address'] = address.id

        

        # Here is need to search all the individuals that are in the KeyPersons list, and check if they exist or not.

        if (venue_serializer.is_valid()):
            n = venue_serializer.save()
            
            return Response(venue_serializer.data, status=status.HTTP_201_CREATED)
        return Response(venue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(APIView):
    """
    Requests pertaining to a specific Event that exists on database
    """    
    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except:
            return Http404
    
    def get(self, request, pk, format=None):
        event = self.get_event(pk)
        event_serializer = EventSerializer(event)
        return Response(event_serializer.data)
    
    def put(self, request, pk, format=None):
        event = self.get_event(pk)
        event_serializer = EventSerializer(event, data=request.data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        event = self.get_event(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###
#    FUNCTION BASED VIEWS
###

def calculateCoordinates(address):
    addy = ', '.join(address)
    result = geocoder.arcgis(location=addy)
    if result.ok:
        lat, lon = result.latlng
        print(lat)
        print(lon)
    else:
        raise Exception("I have gotten a bad result :-(")
    

@api_view(['GET'])
def getUser(request, uid):
    users = User.objects.get(pk=uid)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getProfile(request, uid):
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

@api_view(['POST'])
def likeUser(request):
    user_interaction_serializer = UserInteractionSerializer(data=request.data)
    if user_interaction_serializer.is_valid():
        target_user = User.objects.get(uid=request.data['target'])
        actor_user = User.objects.get(uid=request.data['actor'])
        try:
            event_object = Event.objects.get(id=request.data['event'])
        except Event.DoesNotExist:
            event_object = None

        
        try:
            mutual_like = UserInteraction.objects.get(actor=request.data['target'], 
                                                    target=request.data['actor'])
        except UserInteraction.DoesNotExist:
            pass
        else:
            print('create a match')
            users = [request.data['actor'], request.data['target']]
            users.sort()
            # Need to stuff proper serialization and object cration. This is quite difficult.
            match_object = MatchSerializer({"user1":users[0], "user2":users[1], "active":True})
            MatchSerializer.create(match_object, validated_data={"active": True, 
                                                                "user1": User.objects.get(uid=users[0]), 
                                                                "user2": User.objects.get(uid=users[1])})

        interaction = UserInteraction.objects.create(
            target=target_user,
            actor=actor_user,
            event=event_object,
            interaction_type=request.data['interaction_type'],
        )
        interaction_serializer = UserInteractionSerializer(interaction)
        return Response(interaction_serializer.data)
    return Response(user_interaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unlikeUser(request):
    return NotImplemented()

@api_view(['PATCH'])
def unmatchUser(request):
    return NotImplemented()



@api_view(['POST'])
def register_ticket(request, uid, event_id):
    return NotImplemented()