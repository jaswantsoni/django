from rest_framework import viewsets, permissions
from .models import Skill, SkillSession, Rating, User
from .serializers import SkillSerializer, SkillSessionSerializer, RatingSerializer, UserSerializer
from .permissions import IsVerifiedUser
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import render


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class SkillSessionViewSet(viewsets.ModelViewSet):
    queryset = SkillSession.objects.all()
    serializer_class = SkillSessionSerializer
    # permission_classes = [AllowAny]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def index(request):
    return render(request, 'index.html')

def users_page(request):
    return render(request, 'users.html')

def skills_page(request):
    return render(request, 'skills.html')

def sessions_page(request):
    return render(request, 'sessions.html')


    @action(detail=False, methods=['get', 'PUT', 'POST'])
    def top_teachers(self, request):
        top_teachers = User.objects.annotate(session_count=Count('sessions_taught')) \
            .order_by('-session_count')[:5]
        serializer = self.get_serializer(top_teachers, many=True)
        return Response(serializer.data)
