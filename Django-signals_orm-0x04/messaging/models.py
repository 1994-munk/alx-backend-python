from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return only unread messages for a given user.
        Uses `.only()` to fetch only needed fields for optimization.
        """
        return (
            super().get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )

# Message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    

    #  who edited the message
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages"
    )

    #  track if message was edited
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="edited_messages")

    #  parent message (threading)
    parent_message = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="replies"
    )

    def get_thread(self):
        """Recursively fetch all replies to this message."""
        thread = []
        for reply in self.replies.all():
            thread.append({
                "id": reply.id,
                "content": reply.content,
                "sender": reply.sender.username,
                "created_at": reply.created_at,
                "replies": reply.get_thread()  # recursion
            })
        return thread

        # Custom managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager


    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"

class MessageHistory(models.Model):   
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"
