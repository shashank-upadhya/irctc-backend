from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            booking = serializer.save()
            response_serializer = BookingSerializer(booking)
            return Response({
                'message': 'Booking confirmed successfully',
                'booking': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class MyBookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('train', 'user').order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'bookings': serializer.data
        })