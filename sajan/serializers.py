from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User, Group


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
            "rider_username",
            "contact_name",
            "contact_number"
        ]


    def get_passengers(self, obj):
        return [passenger.username for passenger in obj.get_confirmed_passengers()]














class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = ["id", "passenger", "booking_status", "booking_time", "ride"]
        read_only_fields = ["passenger", "booking_time", "booking_status"]


class BookingSerializerWithRides(serializers.ModelSerializer):
    ride = RideSerializer()
    class Meta:
        model = Booking
        fields = ["ride"]




class UserSerializer(serializers.ModelSerializer):

    groups = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'groups')

    def get_groups(self, obj):
        print(obj.groups.all())
        # Return a list of group names for the user
        return [group.name for group in obj.groups.all()]
