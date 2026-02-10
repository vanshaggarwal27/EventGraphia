from django.utils.timezone import now
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

    def validate_event_date(self, value):
        if value < now().date():
            raise serializers.ValidationError(
                "Event date cannot be in the past."
            )
        return value

    def validate_photographers_required(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Photographers required must be greater than 0."
            )
        return value
