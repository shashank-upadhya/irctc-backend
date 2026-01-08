from rest_framework import serializers
from .models import Train

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            'id', 'train_number', 'train_name', 'source', 'destination',
            'departure_time', 'arrival_time', 'total_seats', 'available_seats',
            'fare', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if 'available_seats' in attrs and 'total_seats' in attrs:
            if attrs['available_seats'] > attrs['total_seats']:
                raise serializers.ValidationError(
                    "Available seats cannot exceed total seats"
                )
        return attrs

class TrainSearchSerializer(serializers.Serializer):
    source = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)
    date = serializers.DateField(required=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100)
    offset = serializers.IntegerField(required=False, min_value=0)

class TrainCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            'train_number', 'train_name', 'source', 'destination',
            'departure_time', 'arrival_time', 'total_seats', 'available_seats',
            'fare', 'is_active'
        ]

    def validate_train_number(self, value):
        if self.instance is None:  # Creating new train
            if Train.objects.filter(train_number=value).exists():
                raise serializers.ValidationError("Train with this number already exists")
        return value

    def validate(self, attrs):
        if 'available_seats' in attrs and 'total_seats' in attrs:
            if attrs['available_seats'] > attrs['total_seats']:
                raise serializers.ValidationError(
                    "Available seats cannot exceed total seats"
                )
        return attrs