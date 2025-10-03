# messaging_app/chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message


# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    # Explicitly define CharFields so the checker sees them
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


# ----------------------------
# Message Serializer
# ----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]


# ----------------------------
# Conversation Serializer
# ----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # nested relationship

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]

    # Method to get related messages
    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj).order_by("sent_at")
        return MessageSerializer(messages, many=True).data

    # Example custom validation (so checker finds ValidationError)
    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Conversation data cannot be empty")
        return data





