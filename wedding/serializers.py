from rest_framework import serializers
from .models import Item, RSVP, Friend

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        ordering = ['ordering']

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'