from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import WatchEntry, Post, Investment
from .services import CryptoService
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from testApp.models import User
from django import forms
import json

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Create your views here.

@login_required
def coin_list(request):
    trending_coins = CryptoService.get_trending_coins()
    user_watches = WatchEntry.objects.filter(user=request.user)
    popular_coins = WatchEntry.get_coin_popularity()
    
    context = {
        'trending_coins': trending_coins,
        'user_watches': user_watches,
        'popular_coins': popular_coins,
    }
    return render(request, 'crypto_tracker/coin_list.html', context)

@login_required
def add_watch_entry(request):
    if request.method == 'POST':
        coin_symbol = request.POST.get('coin_symbol')
        personal_note = request.POST.get('personal_note', '')
        image = request.FILES.get('image')
        
        watch_entry, created = WatchEntry.objects.get_or_create(
            user=request.user,
            coin_symbol=coin_symbol,
            defaults={
                'personal_note': personal_note,
                'image': image
            }
        )
        
        if not created:
            watch_entry.personal_note = personal_note
            if image:
                watch_entry.image = image
            watch_entry.save()
            
        messages.success(request, f'Successfully added {coin_symbol} to your watchlist!')
        return redirect('crypto_tracker:coin_list')
    
    return redirect('crypto_tracker:coin_list')

@login_required
def coin_detail(request, coin_id):
    price_data = CryptoService.get_coin_price(coin_id)
    history_data = CryptoService.get_coin_history(coin_id)
    print(f"History data for {coin_id}: {history_data}")
    watch_entry = WatchEntry.objects.filter(
        user=request.user,
        coin_symbol=coin_id
    ).first()
    
    # Get investment count
    investment_count = Investment.objects.filter(coin_symbol=coin_id).count()
    
    # Get recent posts about this coin
    recent_posts = Post.objects.filter(coin_symbol=coin_id).order_by('-created_at')[:5]
    
    # Get coin popularity
    coin_popularity = WatchEntry.get_coin_popularity()
    watchers_count = next((item['watchers_count'] for item in coin_popularity if item['coin_symbol'] == coin_id), 0)
    
    context = {
        'coin_id': coin_id,
        'price_data': price_data,
        'history_data': history_data if history_data else {},
        'watch_entry': watch_entry,
        'investment_count': investment_count,
        'recent_posts': recent_posts,
        'watchers_count': watchers_count,
    }
    return render(request, 'crypto_tracker/coin_detail.html', context)

@login_required
def get_coin_price(request, coin_id):
    price_data = CryptoService.get_coin_price(coin_id)
    if price_data:
        return JsonResponse(price_data)
    return JsonResponse({'error': 'Failed to fetch price data'}, status=400)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('crypto_tracker:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crypto_tracker/register.html', {'form': form})

@login_required
def home(request):
    posts = Post.objects.all().select_related('user')
    return render(request, 'crypto_tracker/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        coin_symbol = request.POST.get('coin_symbol', '')
        
        post = Post.objects.create(
            user=request.user,
            title=title,
            content=content,
            image=image,
            coin_symbol=coin_symbol
        )
        messages.success(request, 'Post created successfully!')
        return redirect('crypto_tracker:home')
    return render(request, 'crypto_tracker/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'likes': post.total_likes(), 'liked': liked})

@login_required
def add_investment(request):
    if request.method == 'POST':
        coin_symbol = request.POST.get('coin_symbol')
        amount = request.POST.get('amount')
        price_data = CryptoService.get_coin_price(coin_symbol)
        
        if price_data and coin_symbol in price_data:
            investment = Investment.objects.create(
                user=request.user,
                coin_symbol=coin_symbol,
                amount=amount,
                price_at_purchase=price_data[coin_symbol]['usd']
            )
            messages.success(request, f'Investment in {coin_symbol} recorded!')
        else:
            messages.error(request, 'Failed to get current price data')
    
    return redirect('crypto_tracker:coin_detail', coin_id=coin_symbol)
