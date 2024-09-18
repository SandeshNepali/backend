# ride/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("", views.ride_view, name="ride_view"),
    path("api/rides/", views.RideListCreate.as_view(), name="ride_list_create"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user_details/", views.Userdetails.as_view(), name="user_details"),
    path("api/my_rides/", views.UserRide.as_view(), name="my_rides"),
    path("api/booked_rides/", views.BookedRide.as_view(), name="booked_rides"),
    path('api/cancel-booking/<int:booking_id>/', views.CancelBooking.as_view(), name='cancel_booking'),  
]
