# messaging_app/chats/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow only owners to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes your Message model has a 'user' field
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        Only participants of the conversation can access messages.
        """
        # Assuming obj has a conversation attribute and that conversation has participants
        return request.user in obj.conversation.participants.all()