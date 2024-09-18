from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import *
from .serializers import *
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookedRide(APIView):
    def get(self, request):
        # Get all bookings related to the logged-in user (passenger)
        bookings = Booking.objects.filter(passenger=request.user)

        # Serialize the bookings
        serializer = BookingSerializer(bookings, many=True)

        # Return the response with serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            # Create a new booking
            ride_id = request.data.get('ride_id')
            seats_booked = request.data.get('seats_booked', 1)

            # Fetch the ride
            ride = get_object_or_404(Ride, id=ride_id)

            # Check if there are enough seats available
            if ride.available_seats < int(seats_booked):
                raise ValidationError("Not enough available seats for this ride.")

            # Create the booking
            booking = Booking(
                ride=ride,
                passenger=request.user,
                seats_booked=seats_booked
            )

            booking.save()

            # Serialize the new booking
            serializer = BookingSerializer(booking)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "An error occurred while processing your request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CancelBooking(APIView):

    def post(self, request, booking_id):
        # Get the booking made by the logged-in user
        booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)

        # If booking is already canceled
        if booking.canceled:
            return Response({"detail": "This booking is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel the booking
        booking.cancel()

        return Response({"detail": "Booking canceled successfully."}, status=status.HTTP_200_OK)

class UserRide(APIView):

    def get(self, request):

        rides = request.user.rides.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RideListCreate(APIView):

    def get(self, request):

        current_time = timezone.now()
        rides = Ride.objects.filter(departure_time__gt=current_time)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(driver=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Userdetails(APIView):

    def get(self, request):
        try:
            user_id = request.user.id
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something Went Wrong!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def ride_view(request):
    return render(request, "index.html")
