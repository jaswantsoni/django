from rest_framework import serializers
from JobPortalApp.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "is_recruiter"]


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"