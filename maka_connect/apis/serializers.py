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

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ConversationStarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationStarters
        fields = ['description']