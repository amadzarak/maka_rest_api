from rest_framework import serializers
from maka.models import *
from maka.models import Profile
from .firebase_client import FirebaseClient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    def get_name(self, uid):
        profile = Profile.objects.get(user=uid)
        return profile.nickName
    
    class Meta:
        model = Profile
        fields = '__all__'

class GuestContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestContacts
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    target_name = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()
    client = FirebaseClient()

    def get_target_name(self, obj):
        print(obj)
        #profile = Profile.objects.get(user=obj.target)
        #return profile.nickName
        name = self.client.get_by_id(obj.target)
        return name

    def get_actor_name(self, obj):
        print(obj)
        #profile = Profile.objects.get(user=obj.actor)
        #return profile.nickName
        name = self.client.get_by_id(obj.actor)
        return name
    
    class Meta:
        model = UserInteraction
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    other_user_name = serializers.SerializerMethodField()
    other_user_id = serializers.SerializerMethodField()

    client = FirebaseClient()
    def get_other_user_id(self, obj):
        if obj.user1 == self.context['user_id']:
            return obj.user2
        else:
            return obj.user1
        #if obj.user1_id == self.context['user_id']:
        #    return obj.user2_id
        #else:
        #    return obj.user1_id

    def get_other_user_name(self, obj):
        
        #if obj.user1_id == self.context['user_id']:
        #    profile = Profile.objects.get(user=obj.user2)
        #    return profile.nickName
        #else:
        #    profile = Profile.objects.get(user=obj.user1)
        #    return profile.nickName

        if obj.user1 == self.context['user_id']:
            name = self.client.get_by_id(obj.user2)
            return name
        else:
            name = self.client.get_by_id(obj.user1)
            return name


    class Meta:
        model = Matches
        fields = '__all__'

    def create(self, validated_data):
        return Matches.objects.create(**validated_data)

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        exclude = ['event', ]
    
    def create(self, validated_data):
        return EventType.objects.create(**validated_data)

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        exclude = ['event', ]
    
    def create(self, validated_data):
        return EventUser.objects.create(**validated_data)

class EventCheckInSerializer(serializers.ModelSerializer):
    guest_name = serializers.SerializerMethodField()

    def get_guest_name(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return profile.nickName

    class Meta:
        model = EventCheckIn
        fields = ('event', 'user', 'check_in_time', 'guest_type', 'is_host', 'guest_name')

class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        exclude = ['event', ]

    def create(self, validated_data):
        return EventDate.objects.create(**validated_data)

class EventSerializer(serializers.ModelSerializer):
    """
        {
            "description": "description field",
            "require_tickets": "false",
            "password_protected": "false",
            "cost": 0.00,
            "event_user": {},
            "event_type": {},
            "event_date": {}
        }
    """

    class Meta:
        model = Event
        fields = '__all__'


class ConversationStarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationStarters
        fields = ['description']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class KeyPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPerson
        fields = '__all__'