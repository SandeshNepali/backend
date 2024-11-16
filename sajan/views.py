from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone


# update the ride from the driver of that ride only
class UpdateRide(APIView):

    def put(self, request, ride_id):
        # Check if user is in the 'Rider' group
        if not request.user.groups.filter(name="Rider").exists():
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve the ride instance or return a 404 if not found
        ride = get_object_or_404(Ride, id=ride_id, driver=request.user)

        # Partially update the ride with incoming data
        serializer = RideSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save changes to the ride instance
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete ride
class DeleteRide(APIView):

    def delete(self, request, ride_id):
        # Check if user is in the 'Rider' group
        if not request.user.groups.filter(name="Rider").exists():
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve the ride instance or return a 404 if not found
        ride = get_object_or_404(Ride, id=ride_id, driver=request.user)

        print(ride)

        # Delete the ride instance
        ride.delete()

        return Response(
            {"detail": "Ride deleted successfully."}, status=status.HTTP_200_OK
        )


# driver can create the ride using this api
class CreateRide(APIView):
    def post(self, request):

        if not request.user.groups.filter(name="Rider").exists():
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        print(request.data)

        serializer = RideSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(driver=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user details like name
class Userdetails(APIView):

    def get(self, request):

        try:
            user_id = request.user.id
            user = get_object_or_404(User, id=user_id)

            # print(user)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something Went Wrong!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# get rides
class GetRides(APIView):
    def get(self, request):
        now = timezone.now()
        rides = Ride.objects.filter(departure_time__gt=now, status="PENDING")
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# getBook ride of the user
class GetBookRides(APIView):

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(passenger=user, booking_status="CONFIRMED")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# book avilable ride
class BookRide(APIView):

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

# get the driver ride by driver only
class GetRidesByUserId(APIView):
    def get(self, request):
        rides = Ride.objects.filter(driver=request.user)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# get my booked rides
class GetMyBookRides(APIView):
    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(passenger=user, booking_status="CONFIRMED")
        serializer = BookingSerializerWithRides(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# cancel book ride
class CancelBookedRide(APIView):
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




# creating the user 

from rest_framework.permissions import AllowAny

class UserCreateAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# driver application handling
class AddUserToRiderGroup(APIView):

    def post(self, request):
        # Get the authenticated user
        user = request.user
        
        # Check if the user exists
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the "Rider" group
        rider_group, created = Group.objects.get_or_create(name='Rider')

        if rider_group in user.groups.all():
            return Response({"message": f"User {user.username} is already registered as rider"}, status=status.HTTP_200_OK)

        # Add the user to the "Rider" group
        user.groups.add(rider_group)

        return Response({"message": f"User {user.username} is now registered as rider"}, status=status.HTTP_200_OK)



################################## old


# class GetRides(APIView):
    def get(self, request):
        now = timezone.now()
        rides = Ride.objects.filter(departure_time__gt=now, status="PENDING")
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        if not request.user.groups.filter(name="Rider").exists():
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(driver=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetBooking(APIView):

#     def get(self, request):
#         user = request.user
#         bookings = Booking.objects.filter(passenger=user, booking_status="CONFIRMED")
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):

#         try:
#             ride = request.data.get("ride")

#             existing_booking = Booking.objects.filter(
#                 ride=ride, passenger=request.user
#             ).latest("booking_time")

#             if existing_booking:

#                 if existing_booking.booking_status == "CONFIRMED":
#                     return Response(
#                         {"message": "You have already booked this ride."},
#                         status=status.HTTP_202_ACCEPTED,
#                     )
#                 else:
#                     existing_booking.booking_status = "CONFIRMED"
#                     existing_booking.save()
#                     return Response(
#                         {"status": "Booking CONFIRMED"}, status=status.HTTP_200_OK
#                     )

#         except Booking.DoesNotExist:

#             ride_obj = Ride.objects.get(pk=ride)

#             if not ride_obj.is_ride_available():
#                 return Response(
#                     {"message": "Ride Full !"}, status=status.HTTP_202_ACCEPTED
#                 )

#             serializer = BookingSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(passenger=request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             print(e)
#             return Response(
#                 {"message": "something went wrong", "success": "False"},
#                 status=status.HTTP_202_ACCEPTED,
#             )


# class CancelRideView(APIView):
#     def post(self, request, pk):
#         try:
#             ride = Ride.objects.get(pk=pk)
#             if ride.driver == request.user:
#                 ride.cancel_ride()
#                 return Response({"status": "Ride canceled"}, status=status.HTTP_200_OK)
#             return Response(
#                 {"error": "You are not authorized to cancel this ride"},
#                 status=status.HTTP_202_ACCEPTED,
#             )
#         except Ride.DoesNotExist:
#             return Response(
#                 {"error": "Ride not found"}, status=status.HTTP_202_ACCEPTED
#             )


# class CancelBookingView(APIView):
#     def post(self, request, pk):
#         try:
#             booking = Booking.objects.get(pk=pk, passenger=request.user)

#             if booking.booking_status == "CANCELED":
#                 return Response(
#                     {"message": "Booking is already canceled."},
#                     status=status.HTTP_202_ACCEPTED,
#                 )

#             booking.booking_status = "CANCELED"
#             booking.save()
#             return Response({"status": "Booking canceled"}, status=status.HTTP_200_OK)

#         except Booking.DoesNotExist:
#             return Response(
#                 {"message": "Booking not found or you are not authorized"},
#                 status=status.HTTP_202_ACCEPTED,
#             )


# class GetRideById(APIView):

#     def get(self, request, ride_id):
#         try:
#             # Retrieve the ride with the given id
#             ride = Ride.objects.get(id=ride_id)
#         except Ride.DoesNotExist:
#             # Return a 404 response if the ride is not found
#             return Response(
#                 {"message": "Ride not found."}, status=status.HTTP_202_ACCEPTED
#             )

#         # Serialize the ride data and return it
#         serializer = RideSerializer(ride)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class GetMyRides(APIView):
#     def get(self, request):
#         rides = Ride.objects.filter(driver=request.user)
#         serializer = RideSerializer(rides, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
