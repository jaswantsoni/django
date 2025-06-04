from rest_framework import serializers
from .models import WatchEntry, Post, Investment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('date_joined',)

class WatchEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = WatchEntry
        fields = ('id', 'user', 'coin_symbol', 'personal_note', 'image', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'image', 'coin_symbol', 
                 'created_at', 'updated_at', 'likes_count', 'is_liked')
        read_only_fields = ('created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False

class InvestmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_price = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = ('id', 'user', 'coin_symbol', 'amount', 'price_at_purchase', 
                 'created_at', 'current_price', 'profit_loss')
        read_only_fields = ('created_at',)

    def get_current_price(self, obj):
        from .services import CryptoService
        price_data = CryptoService.get_coin_price(obj.coin_symbol)
        if price_data and obj.coin_symbol in price_data:
            return price_data[obj.coin_symbol]['usd']
        return None

    def get_profit_loss(self, obj):
        current_price = self.get_current_price(obj)
        if current_price:
            return (current_price - float(obj.price_at_purchase)) * float(obj.amount)
        return None 