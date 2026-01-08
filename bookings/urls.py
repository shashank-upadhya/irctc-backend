from django.urls import path
from .views import BookingCreateView, MyBookingsView

urlpatterns = [
    path('', BookingCreateView.as_view(), name='booking-create'),
    path('my/', MyBookingsView.as_view(), name='my-bookings'),
]