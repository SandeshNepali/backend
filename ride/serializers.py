# ride/serializers.py
from rest_framework import serializers
from .models import Ride  # Replace with your actual model
from django.contrib.auth.models import User

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"  # List the fields you want to include in the API


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"