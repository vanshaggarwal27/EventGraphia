from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

from .models import Event, Photographer, Assignment
from .serializers import (
    EventSerializer,
    EventScheduleSerializer,
    PhotographerSerializer,
    AssignmentSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=["get"], url_path="assignments")
    def get_assignments(self, request, pk=None):
        event = self.get_object()
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="assign-photographers")
    def assign_photographers(self, request, pk=None):
        event = self.get_object()

        # Validations
        if event.event_date < now().date():
            return Response(
                {"error": "Event date is in the past"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.photographers_required <= 0:
            return Response(
                {"error": "photographers_required must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Assignment.objects.filter(event=event).exists():
            return Response(
                {"error": "Photographers already assigned to this event"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find available photographers
        busy_photographers = Assignment.objects.filter(
            event__event_date=event.event_date
        ).values_list("photographer_id", flat=True)

        available_photographers = Photographer.objects.filter(
            is_active=True
        ).exclude(id__in=busy_photographers)

        if available_photographers.count() < event.photographers_required:
            return Response(
                {"error": "Not enough photographers available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Assign photographers
        selected_photographers = available_photographers[
            : event.photographers_required
        ]

        Assignment.objects.bulk_create(
            [
                Assignment(event=event, photographer=p)
                for p in selected_photographers
            ]
        )

        return Response(
            {
                "message": "Photographers assigned successfully",
                "assigned_photographers": PhotographerSerializer(
                    selected_photographers, many=True
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    @action(detail=True, methods=["get"], url_path="schedule")
    def schedule(self, request, pk=None):
        photographer = self.get_object()

        events = Event.objects.filter(
            assignments__photographer=photographer
        ).distinct()

        serializer = EventScheduleSerializer(events, many=True)
        return Response(serializer.data)



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
