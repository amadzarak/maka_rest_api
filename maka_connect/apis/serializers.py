from rest_framework import serializers
from maka.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'

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
    """
    This class is sperate from the Event object when serializing.
    """
    class Meta:
        model = EventCheckIn
        fields = '__all__'

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