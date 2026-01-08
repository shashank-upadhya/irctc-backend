from django.db import models
from django.conf import settings
from trains.models import Train
import uuid

class Booking(models.Model):
    BOOKING_STATUS = (
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    )

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='bookings')
    seats_booked = models.PositiveIntegerField()
    booking_date = models.DateField()
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['booking_id']),
        ]

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.email}"