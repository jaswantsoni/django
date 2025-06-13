from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth import logout as django_logout
from django.views import View
from django.http import JsonResponse
from .models import User, FitnessEntry
from .serializers import UserSerializer, FitnessEntrySerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class FitnessEntryViewSet(viewsets.ModelViewSet):
    queryset = FitnessEntry.objects.all()
    serializer_class = FitnessEntrySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return FitnessEntry.objects.filter(user=self.request.user)

class HomeView(View):
    def get(self, request):
        return JsonResponse({'message': 'Welcome to the Fitness API'})

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    try:
        django_logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    