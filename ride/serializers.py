from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




class RideSerializer(serializers.ModelSerializer):
    driver_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id",
            "start_location",
            "end_location",
            "departure_time",
            "booked_seats",
            "created_at",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
            "total_seats",
            "available_seats",
            "driver_full_name",
        ]

    def get_driver_full_name(self, obj):
        return f"{obj.driver.first_name} {obj.driver.last_name}"



class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "ride",
            "seats_booked",
            "booking_time",
            "canceled",
            "canceled_at",
            "ride_details"
        ]





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

