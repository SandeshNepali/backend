from .models import *
from rest_framework import serializers

class RideSerializer(serializers.ModelSerializer):
    passengers = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id",
            "start_location",
            "end_location",
            "departure_time",
            "status",
            "passengers",
            "rider_fullname",
            "max_passengers",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
        ]

    def get_passengers(self, obj):
        return [passenger.username for passenger in obj.get_confirmed_passengers()]
    



class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "passenger",
            "booking_status",
            "booking_time",
            "ride"
        ]
        read_only_fields = ['passenger', 'booking_time', 'booking_status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

