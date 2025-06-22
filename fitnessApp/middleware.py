from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import BlockedIP

class LogAndBlockIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)

        # Check cache first
        is_blocked = cache.get(f'blocked_ip_{ip}')

        if is_blocked is None:
            # Check database if not in cache
            is_blocked = BlockedIP.objects.filter(ip_address=ip).exists()
            if is_blocked:
                cache.set(f'blocked_ip_{ip}', True, timeout=3600)  # Cache for 1 hour

        if is_blocked:
            return HttpResponseForbidden("🚫 Your IP has been blocked.")

        print(f"✅ IP: {ip} | Path: {request.path}")

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
