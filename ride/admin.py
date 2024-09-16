from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('driver', 'start_location', 'end_location', 'departure_time', 'available_seats', 'created_at')
    search_fields = ('start_location', 'end_location', 'driver__username')
    list_filter = ('departure_time', 'available_seats')
    ordering = ('-departure_time',)
