from django.urls import path
from .views import *

urlpatterns = [
    path("create_ride/", CreateRide.as_view(), name="create-ride"),
    path("user_details/", Userdetails.as_view(), name="user_details"),
    path("get_rides/", GetRides.as_view(), name="get-ride"),
    path("update_ride/<int:ride_id>/", UpdateRide.as_view(), name="update-ride"),
    path("delete_ride/<int:ride_id>/", DeleteRide.as_view(), name="delete-ride"),
    path("get_driver_ride/", GetRidesByUserId.as_view(), name="get-driver-ride"),
    
    # user
    path("get_booked/", GetBookRides.as_view(), name="get-booked-ride"),
    path("book_ride/", BookRide.as_view(), name="book-ride"),
    path("get_user_ride/", GetMyBookRides.as_view(), name="get-user-ride"),
    path("book_ride/<int:pk>/cancel/", CancelBookedRide.as_view(), name="cancel-booking"),


    # creating the user api 
    path('create_user/', UserCreateAPIView.as_view(), name='user-create'),






























    
    # path("booking/", GetBooking.as_view(), name="book-ride"),
    # path("rides/<int:pk>/cancel/", CancelRideView.as_view(), name="cancel-ride"),
    # path(
    #     "booking/<int:pk>/cancel/", CancelBookingView.as_view(), name="cancel-booking"
    # ),
    # path("get-ride/<int:ride_id>/", GetRideById.as_view(), name="get_ride_by_id"),
    # path("my-rides/", GetMyRides.as_view(), name="get_my_rides"),
]
