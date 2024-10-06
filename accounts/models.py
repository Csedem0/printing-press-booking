# booking/models.py

from django.db import models
from django.contrib.auth.models import User

class PrintingPress(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    printing_press = models.ForeignKey(PrintingPress, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    ), default='Pending')

    def __str__(self):
        return f"Booking by {self.customer.username} for {self.printing_press.name} on {self.date}"

