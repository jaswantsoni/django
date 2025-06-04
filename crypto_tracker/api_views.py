from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WatchEntry, Post, Investment
from .serializers import (
    WatchEntrySerializer, PostSerializer, InvestmentSerializer
)
from .services import CryptoService

class WatchEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all().select_related('user')
        coin_symbol = self.request.query_params.get('coin_symbol', None)
        if coin_symbol:
            queryset = queryset.filter(coin_symbol=coin_symbol)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({
            'likes': post.total_likes(),
            'liked': liked
        })

class InvestmentViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def portfolio_summary(self, request):
        investments = self.get_queryset()
        total_investment = 0
        current_value = 0
        profit_loss = 0

        for investment in investments:
            price_data = CryptoService.get_coin_price(investment.coin_symbol)
            if price_data and investment.coin_symbol in price_data:
                current_price = price_data[investment.coin_symbol]['usd']
                investment_value = float(investment.amount) * current_price
                investment_cost = float(investment.amount) * float(investment.price_at_purchase)
                
                total_investment += investment_cost
                current_value += investment_value
                profit_loss += (current_price - float(investment.price_at_purchase)) * float(investment.amount)

        return Response({
            'total_investment': total_investment,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / total_investment * 100) if total_investment > 0 else 0
        }) 