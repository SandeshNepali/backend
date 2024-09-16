from django.db import models
from django.contrib.auth.models import User  # or your custom User model

class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    start_location = models.CharField(max_length=255)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)  # Default value
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)  # Default value
    end_location = models.CharField(max_length=255)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)  # Default value
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)  # Default value
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride from {self.start_location} to {self.end_location} by {self.driver.username}"
