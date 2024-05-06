# apis/views.py
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers as core_serializers
from maka.models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

import geocoder
import dateparser

import datetime
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
            print(n.id)
            EventDate.objects.create(event=n, **data['event_date'])
            for x in data['event_user']:
                EventUser.objects.create(event=n, **x)
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

class VenueDetail(APIView):
    """
    Requests pertaining to a specific Event that exists on database
    """    
    def get_venue(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except:
            return Http404
    
    def get(self, request, pk, format=None):
        venue = self.get_venue(pk)
        venue_serializer = VenueSerializer(venue)
        return Response(venue_serializer.data)
    
    def put(self, request, pk, format=None):
        venue = self.get_venue(pk)
        venue_serializer = VenueSerializer(venue, data=request.data)
        if venue_serializer.is_valid():
            venue_serializer.save()
            return Response(venue_serializer.data)
        return Response(venue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        venue = self.get_venue(pk)
        venue.delete()
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
def getAddress(request, id):
    address = Address.objects.get(id=id)
    serializer = AddressSerializer(address, many=False)
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


@api_view(['GET'])
def getGuestsInEvent(request, eid):
    event = Event.objects.get(pk=eid)
    event_check_ins = event.eventcheckins.all()
    qs_json = EventCheckInSerializer(event_check_ins, many=True)
    return Response(qs_json.data)

@api_view(['POST'])
def checkInStatus(request):
    event = Event.objects.get(pk=request.data['event_id'])
    try:
        check_in_object = EventCheckIn.objects.get(event=event, guest_type="guest", **request.data)
    except EventCheckIn.DoesNotExist:
        return Response({"message": "Not Checked In", "status": False}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"message": "Already checked in", "status": True}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def checkInEvent(request):
    event = Event.objects.get(pk=request.data['event_id'])
    try:
        check_in_object = EventCheckIn.objects.get(event=event, guest_type="guest", **request.data)
    except EventCheckIn.DoesNotExist:
        check_in_object = EventCheckIn.objects.create(check_in_time=datetime.datetime.now(), guest_type="guest", is_host=False, **request.data)
    else:
        return Response({"message": "Already checked in"}, status=status.HTTP_400_BAD_REQUEST)
        
    check_in_serializer = EventCheckInSerializer(check_in_object)
    return Response(check_in_serializer.data)


@api_view(['POST'])
def checkUserInteractionExists(request):
    try:
        current_interaction_object = UserInteraction.objects.get(interaction_type='UserInteractionType.like', actor=request.data['actor'], target=request.data['target'], current_interaction=True)
        user_interaction_serializer = UserInteractionSerializer(current_interaction_object)
        return Response(user_interaction_serializer.data)
    except:
        return Response({"message": "A current interaction between the two users could not be found"})

@api_view(['GET'])
def getUsersLikeSent(request, uid):
    # I suppose their could be an option as to whether or not to return inactive ones too, or just the active ones. I think ill do just
    # active for now.
    likes = UserInteraction.objects.all().filter(interaction_type='UserInteractionType.like', actor=uid, current_interaction=True)
    print(likes)
    like_serializer = UserInteractionSerializer(likes, many=True)
    return Response(like_serializer.data)

@api_view(['GET'])
def getUserMatches(request, uid):    
    matches = Matches.objects.filter(Q(user1_id=uid) | Q(user2_id=uid), active=True)
    match_serializer = MatchSerializer(matches, many=True, context={'user_id': uid})
    return Response(match_serializer.data)

@api_view(['GET'])
def getUsersLikeRecieved(request, uid):
    # I suppose their could be an option as to whether or not to return inactive ones too, or just the active ones. I think ill do just
    # active for now.
    likes = UserInteraction.objects.all().filter(interaction_type='UserInteractionType.like', target=uid, current_interaction=True)
    print(likes)
    like_serializer = UserInteractionSerializer(likes, many=True)
    return Response(like_serializer.data)

@api_view(['POST'])
def likeUser(request):

    if (request.data['target'] == request.data['actor']):
        print('Entry not recorded. A UserInteraction object cannot be created for a single user')
        return Response({"message": "A UserInteraction object cannot be created for a single user"})    
    try:
        user_interaction_object = UserInteraction.objects.get(target=request.data['target'], actor=request.data['actor'], current_interaction=True)
    except UserInteraction.DoesNotExist:
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
                                                        target=request.data['actor'], 
                                                        current_interaction=True)
            except UserInteraction.DoesNotExist:
                print('An inverse of the UserIteraction Does Not Exist. This is currently single sided interaction.')
                pass
            else:
                print('A Match instance was created.')
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
    else:
        print('Existing UserInteraction. Did not create new entry')
        return Response({"message": "This UserInteraction has already been recorded"})


@api_view(['POST'])
def unlikeUser(request):
    return NotImplemented()

@api_view(['PATCH'])
def unmatchUser(request):
    return NotImplemented()



@api_view(['POST'])
def register_ticket(request, uid, event_id):
    return NotImplemented()
