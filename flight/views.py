from django.shortcuts import render
from rest_framework import viewsets
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsStaffOrReadOnly
from datetime import datetime, date

# GET, POST, UPDATE, DELETE, PATCH
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer

    def get_queryset(self):
        now = datetime.now()
        curren_time = now.strftime('%H:%M:%S') #python datetime format / google
        today = date.today()

        if self.request.user.is_staff:
            return super().get_queryset()

        else:
            queryset = Flight.objects.filter(date_of_departure__gt=today)

            if Flight.objects.filter(date_of_departure=today):
                today_gs = Flight.objects.filter(date_of_departure=today).filter(estimated_time_deperture__gt=curren_time)

                queryset = queryset.union(today_gs)
            return queryset        
                



class ReservationView(viewsets.ModelViewSet):
    queryset= Reservation.objects.all()
    serializer_class= ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user = self.request.user) 

            
       
        



