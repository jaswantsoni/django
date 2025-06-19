from django.contrib import admin
from .models import WatchEntry, Post, Investment, BlockedIP

@admin.register(WatchEntry)
class WatchEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_symbol', 'created_at', 'updated_at')
    list_filter = ('coin_symbol', 'created_at')
    search_fields = ('user__username', 'coin_symbol', 'personal_note')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'coin_symbol', 'created_at', 'total_likes')
    list_filter = ('coin_symbol', 'created_at')
    search_fields = ('title', 'content', 'user__username')

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_symbol', 'amount', 'price_at_purchase', 'created_at')
    list_filter = ('coin_symbol', 'created_at')
    search_fields = ('user__username', 'coin_symbol')

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'date_added')  
    search_fields = ('ip_address', 'reason')               
    list_filter = ('date_added',)  
