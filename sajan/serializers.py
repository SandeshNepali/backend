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
            "contact_number",
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
        fields = ("first_name", "last_name", "username", "groups")

    def get_groups(self, obj):
        print(obj.groups.all())
        # Return a list of group names for the user
        return [group.name for group in obj.groups.all()]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name"]

    def create(self, validated_data):
        # Extract the fields from the validated data
        username = validated_data.get("username")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")

        # Create user with hashed password and additional fields
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user
