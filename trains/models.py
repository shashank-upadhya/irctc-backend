from django.db import models

class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    train_name = models.CharField(max_length=255)
    source = models.CharField(max_length=100, db_index=True)
    destination = models.CharField(max_length=100, db_index=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trains'
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['train_number']),
        ]

    def __str__(self):
        return f"{self.train_number} - {self.train_name}"

    def save(self, *args, **kwargs):
        # Ensure available_seats doesn't exceed total_seats
        if self.available_seats > self.total_seats:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)