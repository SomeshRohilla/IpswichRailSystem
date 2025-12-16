from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()

    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.source} → {self.destination})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.train.name}"
