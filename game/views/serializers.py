from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'winner', 'creator', 'opponent', 'cols',
                  'rows', 'completed', 'created', 'current_turn')
        depth = 1

class GameLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLog
        fields = ('id', 'text', 'player', 'created')
        depth = 1

class GameSquareSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSquare
        fields = ('id', 'game', 'owner', 'status', 'row', 'col')