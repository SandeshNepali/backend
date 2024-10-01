from django.urls import path
from .views import *

urlpatterns = [
    path("rides/", GetRides.as_view(), name="create-ride"),
    path("booking/", GetBooking.as_view(), name="book-ride"),
    path("rides/<int:pk>/cancel/", CancelRideView.as_view(), name="cancel-ride"),
    path(
        "booking/<int:pk>/cancel/", CancelBookingView.as_view(), name="cancel-booking"
    ),
    path("user_details/", Userdetails.as_view(), name="user_details"),

]
