from rest_framework import serializers
from maka.models import *
from maka.models import Profile



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
    class Meta:
        model = UserInteraction
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
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