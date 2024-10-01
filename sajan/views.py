from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone


class GetRides(APIView):

    def get(self, request):
        now = timezone.now()
        rides = Ride.objects.filter(departure_time__gt=now)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(driver=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBooking(APIView):

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(passenger=user, booking_status="CONFIRMED")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            ride = request.data.get("ride")

            existing_booking = Booking.objects.filter(
                ride=ride, passenger=request.user
            ).latest("booking_time")

            if existing_booking:

                if existing_booking.booking_status == "CONFIRMED":
                    return Response(
                        {"message": "You have already booked this ride."},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    existing_booking.booking_status = "CONFIRMED"
                    existing_booking.save()
                    return Response(
                        {"status": "Booking CONFIRMED"}, status=status.HTTP_200_OK
                    )

        except Booking.DoesNotExist:

            ride_obj = Ride.objects.get(pk=ride)

            if not ride_obj.is_ride_available():
                return Response(
                    {"message": "Ride Full !"}, status=status.HTTP_202_ACCEPTED
                )

            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(passenger=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response(
                {"message": "something went wrong", "success": "False"},
                status=status.HTTP_202_ACCEPTED,
            )


class CancelRideView(APIView):
    def post(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
            if ride.driver == request.user:
                ride.cancel_ride()
                return Response({"status": "Ride canceled"}, status=status.HTTP_200_OK)
            return Response(
                {"error": "You are not authorized to cancel this ride"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Ride.DoesNotExist:
            return Response(
                {"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CancelBookingView(APIView):
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, passenger=request.user)

            if booking.booking_status == "CANCELED":
                return Response(
                    {"message": "Booking is already canceled."},
                    status=status.HTTP_202_ACCEPTED,
                )

            booking.booking_status = "CANCELED"
            booking.save()
            return Response({"status": "Booking canceled"}, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found or you are not authorized"},
                status=status.HTTP_202_ACCEPTED,
            )

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
