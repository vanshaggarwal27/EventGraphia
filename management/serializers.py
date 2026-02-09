from rest_framework import serializers
from .models import Event, Photographer, Assignment


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    photographer = PhotographerSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ["id", "photographer"]


class EventSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
