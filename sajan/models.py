from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Ride(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
        ("CANCELED", "Canceled"),
    ]

    driver = models.ForeignKey(
        User, related_name="rides_as_driver", on_delete=models.CASCADE
    )

    start_location = models.CharField(max_length=255) 
    end_location = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    max_passengers = models.PositiveIntegerField(default=4)
    
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride Obj {self.driver.username}"

    def is_ride_available(self):
        """
        Check if the ride is available for new bookings.
        """
        return (
            self.status == "PENDING"
            and self.get_confirmed_passenger_count() < self.max_passengers
        )
    
    def get_confirmed_passenger_count(self):
        """
        Returns the number of confirmed passengers.
        """
        return self.bookings.filter(booking_status="CONFIRMED").count()
    
    def can_add_passenger(self, passenger):
        """
        Ensure the ride can accommodate more passengers.
        """
        if not self.is_ride_available():
            raise ValidationError("Ride is either full or not available for booking.")
        if self.bookings.filter(
            passenger=passenger, booking_status="CONFIRMED"
        ).exists():
            raise ValidationError("Passenger is already in the ride.")
    
    def get_confirmed_passengers(self):
        """
        Returns the list of passengers with confirmed bookings.
        """
        confirmed_bookings = self.bookings.filter(booking_status="CONFIRMED")
        return [booking.passenger for booking in confirmed_bookings]
    
    # UNDERSTAND
    def cancel_ride(self):
        """
        Cancels the ride and clears all bookings.
        """
        self.status = "CANCELED"
        self.bookings.update(booking_status="TERMINATED")
        self.save()

    @property
    def rider_username(self):
        return self.driver.username
    
    @property
    def rider_fullname(self):
        return f"{self.driver.first_name} {self.driver.last_name}"


class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("CONFIRMED", "Confirmed"),
        ("CANCELED", "Canceled"),
        ("TERMINATED", "Terminated"),
        ("COMPLETED", "Completed"),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="bookings")
    passenger = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_status = models.CharField(
        max_length=10, choices=BOOKING_STATUS_CHOICES, default="CONFIRMED"
    )
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.passenger.username} for ride {self.ride}"