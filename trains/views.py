from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Train
from .serializers import (
    TrainSerializer, 
    TrainSearchSerializer, 
    TrainCreateUpdateSerializer
)
from .permissions import IsAdminUser

class TrainSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainSerializer

    def get_queryset(self):
        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')
        
        if not source or not destination:
            return Train.objects.none()
        
        queryset = Train.objects.filter(
            source__iexact=source,
            destination__iexact=destination,
            is_active=True,
            available_seats__gt=0
        ).order_by('departure_time')
        
        return queryset

    def list(self, request, *args, **kwargs):
        # Validate query parameters
        serializer = TrainSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

class TrainCreateUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TrainCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if train exists for update
        train_number = serializer.validated_data.get('train_number')
        train = Train.objects.filter(train_number=train_number).first()
        
        if train:
            # Update existing train
            for attr, value in serializer.validated_data.items():
                setattr(train, attr, value)
            train.save()
            response_serializer = TrainSerializer(train)
            return Response({
                'message': 'Train updated successfully',
                'train': response_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # Create new train
            train = serializer.save()
            response_serializer = TrainSerializer(train)
            return Response({
                'message': 'Train created successfully',
                'train': response_serializer.data
            }, status=status.HTTP_201_CREATED)