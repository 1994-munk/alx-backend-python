# chats/middleware.py
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import logging
from datetime import datetime

# create a logger for this file
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

# add file handler if not already added
if not logger.handlers:
    file_handler = logging.FileHandler("requests.log")
    formatter = logging.Formatter("%(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the chat app
    outside of working hours (9AM - 6PM).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (hour in 24h format)
        current_hour = datetime.now().hour  

        # Deny access if outside 9AM - 6PM (i.e. <9 or >=18)
        if current_hour < 9 or current_hour >= 18:
            return HttpResponseForbidden(
                "⛔ Access to the chat is restricted outside 9AM - 6PM."
            )

        # Otherwise continue normally
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of chat messages per IP address.
    Each IP can only send 5 POST requests (messages) per 1 minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests per IP {ip: [timestamps]}
        self.ip_request_log = {}

    def __call__(self, request):
        # Only check POST requests (chat messages)
        if request.method == "POST":
            ip_address = self.get_client_ip(request)
            now = datetime.now()

            # Initialize log for this IP if not exists
            if ip_address not in self.ip_request_log:
                self.ip_request_log[ip_address] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.ip_request_log[ip_address] = [
                ts for ts in self.ip_request_log[ip_address] if ts > one_minute_ago
            ]

            # Check how many requests remain in the 1-minute window
            if len(self.ip_request_log[ip_address]) >= 5:
                return HttpResponseForbidden(
                    "⛔ Too many messages. You are limited to 5 per minute."
                )

            # Log the new request
            self.ip_request_log[ip_address].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Helper to extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")        

class RolePermissionMiddleware:
    """
    Middleware to enforce role-based permissions.
    Only users with role 'admin' or 'moderator' are allowed
    to access protected views.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user role from request (assuming it's stored in request.user or session)
        user = getattr(request, "user", None)

        # If user is authenticated and has a role attribute
        if user and hasattr(user, "role"):
            if user.role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Forbidden: Insufficient permissions"},
                    status=403
                )
        else:
            # If no role info, block request
            return JsonResponse(
                {"error": "Forbidden: Role not found"},
                status=403
            )

        # Allow request if role is okay
        response = self.get_response(request)
        return response