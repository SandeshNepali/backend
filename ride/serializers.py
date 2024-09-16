from rest_framework import serializers
from .models import Ride
from django.contrib.auth.models import User


class RideSerializer(serializers.ModelSerializer):
    driver_full_name = (
        serializers.SerializerMethodField()
    )  # Custom method for full name

    class Meta:
        model = Ride
        fields = [
            "id",
            "start_location",
            "end_location",
            "departure_time",
            "available_seats",
            "created_at",
            "driver_full_name",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
        ]

    def get_driver_full_name(self, obj):
        return f"{obj.driver.first_name} {obj.driver.last_name}"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
