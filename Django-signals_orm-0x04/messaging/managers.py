from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Returns unread messages for a given user with only the necessary fields
        return (
            super().get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
