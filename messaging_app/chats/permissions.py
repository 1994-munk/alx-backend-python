# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow only owners to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes your Message model has a 'user' field
        return obj.user == request.user
