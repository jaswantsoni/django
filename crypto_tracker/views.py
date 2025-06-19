from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import WatchEntry, Post, Investment, BlockedIP
from .services import CryptoService
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from testApp.models import User
from django import forms
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.views.generic import ListView, DetailView, CreateView, FormView, RedirectView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'crypto_tracker/home.html'
    context_object_name = 'posts' 
    ordering = ['-created_at']
    paginate_by = 4 
    
    

class CoinListView(LoginRequiredMixin, TemplateView):
    template_name = 'crypto_tracker/coin_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trending_coins'] = CryptoService.get_trending_coins()
        context['user_watches'] = WatchEntry.objects.filter(user=self.request.user)
        context['popular_coins'] = WatchEntry.get_coin_popularity()
        return context

class AddWatchEntryView(LoginRequiredMixin, CreateView):
    model = WatchEntry
    fields = ['coin_symbol', 'personal_note', 'image']
    template_name = 'crypto_tracker/coin_list.html' 
    success_url = reverse_lazy('crypto_tracker:coin_list')

    def form_valid(self, form):
        
        coin_symbol = form.cleaned_data['coin_symbol']
        existing_entry = WatchEntry.objects.filter(user=self.request.user, coin_symbol=coin_symbol).exists()

        if existing_entry:
            messages.error(self.request, f'{coin_symbol} is already in your watchlist.')
            return redirect(self.success_url) 

        form.instance.user = self.request.user
        messages.success(self.request, f'Successfully added {form.instance.coin_symbol} to your watchlist!')
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'Failed to add watch entry. Please check the form data.')
        # Manually render the template with context data similar to CoinListView
        context = self.get_context_data(form=form)
        context['trending_coins'] = CryptoService.get_trending_coins()
        context['user_watches'] = WatchEntry.objects.filter(user=self.request.user)
        context['popular_coins'] = WatchEntry.get_coin_popularity()
        return render(self.request, self.template_name, context)

class CoinDetailView(LoginRequiredMixin, DetailView):
    model = WatchEntry
    template_name = 'crypto_tracker/coin_detail.html'
    slug_field = 'coin_symbol'
    slug_url_kwarg = 'coin_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        coin_id = self.kwargs.get(self.slug_url_kwarg)
        try:
            return queryset.get(user=self.request.user, coin_symbol=coin_id)
        except WatchEntry.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coin_id = self.kwargs.get(self.slug_url_kwarg)
        
        context['coin_id'] = coin_id
        context['price_data'] = CryptoService.get_coin_price(coin_id)
        context['history_data'] = CryptoService.get_coin_history(coin_id) if CryptoService.get_coin_history(coin_id) else {}
        
        context['investment_count'] = Investment.objects.filter(coin_symbol=coin_id).count()
        context['recent_posts'] = Post.objects.filter(coin_symbol=coin_id).order_by('-created_at')[:5]
        
        coin_popularity = WatchEntry.get_coin_popularity()
        context['watchers_count'] = next((item['watchers_count'] for item in coin_popularity if item['coin_symbol'] == coin_id), 0)
        
        return context

class GetCoinPriceView(View):
    def get(self, request, coin_id):
        price_data = CryptoService.get_coin_price(coin_id)
        if price_data:
            return JsonResponse(price_data)
        return JsonResponse({'error': 'Failed to fetch price data'}, status=400)

class RegisterView(CreateView):
    template_name = 'crypto_tracker/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('crypto_tracker:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return super().form_valid(form)

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'coin_symbol']
    template_name = 'crypto_tracker/create_post.html'
    success_url = reverse_lazy('crypto_tracker:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'likes': post.total_likes(), 'liked': liked})

class AddInvestmentView(LoginRequiredMixin, CreateView):
    model = Investment
    fields = ['coin_symbol', 'amount']
    template_name = 'crypto_tracker/coin_detail.html' 
    success_url = reverse_lazy('crypto_tracker:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        coin_symbol = form.cleaned_data['coin_symbol']
       
        price_data = CryptoService.get_coin_price(coin_symbol)
        if price_data and coin_symbol in price_data:
            form.instance.price_at_purchase = price_data[coin_symbol]['usd']
            messages.success(self.request, f'Investment in {coin_symbol} recorded!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Failed to get current price data for investment.')
            return self.form_invalid(form)

def sync_view(request):
    return "this is a synchronous view"

async def async_view(request):
    return "this is a asynchrounous view"

async def calling_sync_view(request):
    response = sync_view(request)
    await async_view(request)
    return Response({"message": response})


 
 
 
# IP Blocking API endpoints
@api_view(['POST'])
@permission_classes([IsAdminUser])
def block_ip(request):
    """Block an IP address"""
    ip_address = request.data.get('ip_address')
    reason = request.data.get('reason', '')
   
    if not ip_address:
        return Response({'error': 'IP address is required'}, status=status.HTTP_400_BAD_REQUEST)
   
    # Create or update the blocked IP
    blocked_ip, created = BlockedIP.objects.update_or_create(
        ip_address=ip_address,
        defaults={'reason': reason}
    )
   
    # Clear cache for this IP
    from django.core.cache import cache
    cache.delete(f'blocked_ip_{ip_address}')
   
    if created:
        return Response({'message': f'IP {ip_address} has been blocked'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': f'IP {ip_address} block has been updated'}, status=status.HTTP_200_OK)
 
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def unblock_ip(request, ip_address):
    """Unblock an IP address"""
    try:
        blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
        blocked_ip.delete()
       
        # Clear cache for this IP
        from django.core.cache import cache
        cache.delete(f'blocked_ip_{ip_address}')
       
        return Response({'message': f'IP {ip_address} has been unblocked'}, status=status.HTTP_200_OK)
    except BlockedIP.DoesNotExist:
        return Response({'error': f'IP {ip_address} is not blocked'}, status=status.HTTP_404_NOT_FOUND)
 
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_blocked_ips(request):
    """List all blocked IPs"""
    blocked_ips = BlockedIP.objects.all().order_by('ip_address')
    data = [{'ip_address': ip.ip_address, 'reason': ip.reason, 'date_added': ip.date_added} for ip in blocked_ips]
    return Response(data)
 