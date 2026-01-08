from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'email': serializer.data['email'],
            },
            'tokens': serializer.data['tokens']
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'message': 'Login successful',
            'user': serializer.data['user'],
            'tokens': serializer.data['tokens']
        }, status=status.HTTP_200_OK)