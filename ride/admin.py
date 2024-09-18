from django.contrib import admin
from .models import *



# Define a custom admin class for the Ride model
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'driver',
        'start_location',
        'end_location',
        'departure_time',
        'total_seats',
        'booked_seats',
        'available_seats',
        'created_at'
    )
    list_filter = ('departure_time', 'driver')
    search_fields = ('start_location', 'end_location', 'driver__username')
    readonly_fields = ('created_at',)  

admin.site.register(Ride, RideAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'passenger', 'seats_booked', 'booking_time', 'canceled', 'canceled_at', 'is_expired')
    search_fields = ('ride__start_location', 'ride__end_location', 'passenger__username')
    list_filter = ('canceled', 'booking_time')

admin.site.register(Booking, BookingAdmin)