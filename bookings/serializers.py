from rest_framework import serializers
from .models import Booking
from trains.models import Train
from trains.serializers import TrainSerializer
from django.db import transaction
from datetime import date

class BookingCreateSerializer(serializers.ModelSerializer):
    train_id = serializers.IntegerField(write_only=True)
    booking_date = serializers.DateField(required=False)

    class Meta:
        model = Booking
        fields = ['train_id', 'seats_booked', 'booking_date']

    def validate_seats_booked(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of seats must be greater than 0")
        if value > 10:
            raise serializers.ValidationError("Cannot book more than 10 seats at once")
        return value

    def validate_booking_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Cannot book for past dates")
        return value

    def validate(self, attrs):
        train_id = attrs.get('train_id')
        seats_booked = attrs.get('seats_booked')
        
        try:
            # Remove select_for_update from validation - just check if train exists
            train = Train.objects.get(id=train_id, is_active=True)
        except Train.DoesNotExist:
            raise serializers.ValidationError("Train not found or inactive")
        
        if train.available_seats < seats_booked:
            raise serializers.ValidationError(
                f"Only {train.available_seats} seats available. Cannot book {seats_booked} seats."
            )
        
        attrs['train'] = train
        if 'booking_date' not in attrs:
            attrs['booking_date'] = date.today()
        
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        train = validated_data.pop('train')
        validated_data.pop('train_id')
        user = self.context['request'].user
        seats_booked = validated_data['seats_booked']
        
        # Lock the train row for update
        train = Train.objects.select_for_update().get(id=train.id)
        
        # Double check availability
        if train.available_seats < seats_booked:
            raise serializers.ValidationError("Seats no longer available")
        
        # Calculate total fare
        total_fare = train.fare * seats_booked
        
        # Create booking
        booking = Booking.objects.create(
            user=user,
            train=train,
            seats_booked=seats_booked,
            booking_date=validated_data['booking_date'],
            total_fare=total_fare,
            status='CONFIRMED'
        )
        
        # Update available seats
        train.available_seats -= seats_booked
        train.save()
        
        return booking

class BookingSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'user_email', 'user_name', 'train',
            'seats_booked', 'booking_date', 'total_fare', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'booking_id', 'created_at', 'updated_at']