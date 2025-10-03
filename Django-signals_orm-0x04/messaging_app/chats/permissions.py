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
    Only allow participants of a conversation to view, send, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        Only participants can access objects in a conversation.
        """
        # Make sure user is a participant
        is_participant = request.user in obj.conversation.participants.all()

        # For unsafe methods (PUT, PATCH, DELETE), still enforce the same rule
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # For safe methods (GET, POST, etc.), same rule applies
        return is_participant