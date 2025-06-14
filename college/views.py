from rest_framework import viewsets
from .models import User, College, Banking
from .serializers import UserSerializer, CollegeSerializer, BankingSerializer

# Django Rest Framework does not support full async yet, 
# but we can create simple ViewSets (they are compatible)
class UserViewSetCollege(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

class BankingViewSet(viewsets.ModelViewSet):
    queryset = Banking.objects.all()
    serializer_class = BankingSerializer
