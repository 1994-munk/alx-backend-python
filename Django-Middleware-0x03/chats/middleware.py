# chats/middleware.py
from django.http import HttpResponseForbidden
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