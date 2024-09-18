from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ride(models.Model):
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    booked_seats = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    total_seats = models.IntegerField(default=1)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rides")

    def __str__(self):
        return f"From {self.start_location} to {self.end_location} by {self.driver.username}"

    @property
    def available_seats(self):
        return self.total_seats - self.booked_seats



class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="bookings")
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    seats_booked = models.IntegerField(default=1)
    booking_time = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.passenger.username} for {self.seats_booked} seat(s) on {self.ride}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only update ride seats when booking is being created
            if self.ride.available_seats >= self.seats_booked:
                self.ride.booked_seats += self.seats_booked
                self.ride.save()
            else:
                raise ValueError("Not enough available seats for this booking.")
        super().save(*args, **kwargs)

    def cancel(self):
        if not self.canceled:
            self.canceled = True
            self.canceled_at = timezone.now()
            self.ride.booked_seats -= self.seats_booked
            self.ride.save()
            self.save()
    
    @property
    def ride_details(self):
        return f"From {self.ride.start_location} to {self.ride.end_location} by {self.ride.driver.username}"

    
    @property
    def is_expired(self):
        if self.ride.departure_time <= timezone.now():
            return "Expired"
        else:
            return "Open"