from rest_framework import serializers
from .models import User, College, Banking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class BankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banking
        fields = '__all__'
