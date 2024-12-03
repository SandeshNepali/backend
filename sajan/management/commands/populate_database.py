from django.core.management.base import BaseCommand
from sajan.models import Ride  
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Populates the database with dummy data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_records = 10  # Change this number to generate more or fewer records

        for _ in range(num_records):
            # Generate random data using Faker
            start_location = fake.city()
            end_location = fake.city()
            departure_time = timezone.now() + timedelta(days=fake.random_int(1, 30))
            status = "PENDING"
            rider_fullname = fake.name()
            max_passengers = fake.random_int(1, 5)
            start_latitude = fake.latitude()
            start_longitude = fake.longitude()
            end_latitude = fake.latitude()
            end_longitude = fake.longitude()
            rider_username = fake.user_name()
            contact_name = fake.name()
            contact_number = fake.phone_number()

            # Create and save a new Ride instance
            ride = Ride(
                start_location=start_location,
                end_location=end_location,
                departure_time=departure_time,
                status=status,
                rider_fullname=rider_fullname,
                max_passengers=max_passengers,
                start_latitude=start_latitude,
                start_longitude=start_longitude,
                end_latitude=end_latitude,
                end_longitude=end_longitude,
                rider_username=rider_username,
                contact_name=contact_name,
                contact_number=contact_number,
            )
            ride.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added ride with ID {ride.id}")
            )
