from django.http import HttpResponseForbidden
from django.core.cache import cache
import re
from .models import BlockedIP
from django.conf import settings
from datetime import datetime
 
class IPBlockingMiddleware:
    def __init__(self, get_response):
       
        print("IPBlocking initialized",datetime.now())
        self.get_response = get_response
        # One-time configuration and initialization
       
        # Compile patterns for better performance
        self.blocked_ip_patterns = [
            r'^172\.16\.',  # Block 172.16.x.x
            # Add more patterns as needed
        ]
        self.compiled_patterns = [re.compile(pattern) for pattern in self.blocked_ip_patterns]
 
    def __call__(self, request):
        # Code to be executed for each request before the view is called
       
        # Get client IP
        ip_address = self.get_client_ip(request)
       
        # Check if IP is blocked
        if self.is_ip_blocked(ip_address):
            return HttpResponseForbidden("Access denied: Your IP address is blocked.")
       
        # Continue processing the request
        response = self.get_response(request)
       
        # Code to be executed for each request/response after the view is called
        return response
   
    def get_client_ip(self, request):
        """Extract the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # In case of proxy, get the first IP
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
   
    def is_ip_blocked(self, ip):
        """Check if an IP is blocked"""
        # Check cache first for performance
        cache_key = f'blocked_ip_{ip}'
        cached_result = cache.get(cache_key)
       
        if cached_result is not None:
            return cached_result
       
        # Check against settings
        if hasattr(settings, 'BLOCKED_IPS') and ip in settings.BLOCKED_IPS:
            cache.set(cache_key, True, 3600)  # Cache for 1 hour
            return True
       
        # Check against database
        try:
            BlockedIP.objects.get(ip_address=ip)
            cache.set(cache_key, True, 3600)
            return True
        except BlockedIP.DoesNotExist:
            pass
       
        # Check against patterns
        for pattern in self.compiled_patterns:
            if pattern.match(ip):
                cache.set(cache_key, True, 3600)
                return True
       
        # Not blocked
        cache.set(cache_key, False, 3600)
        return False
 
 
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("logger initialized",datetime.now())
   
    def __call__(self, request):
        # Pre-processing: Log request details
        ip = self.get_client_ip(request)
        path = request.path
        method = request.method
       
        print(f"[REQUEST] {method} {path} from {ip}")
       
        # Process the request
        response = self.get_response(request)
       
        # Post-processing: Log response details
        status_code = response.status_code
        print(f"[RESPONSE] {status_code} for {method} {path}")
       
        return response
   
    def get_client_ip(self, request):
        """Extract the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # In case of proxy, get the first IP
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip