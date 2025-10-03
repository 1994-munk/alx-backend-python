from django.db.models.signals import pre_save, post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

# Signal to create a notification whenever a new Message is created
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create notification when a new message is saved
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# Signal for logging edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:  # skip new messages (no previous version exists yet)
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content has changed, log it in MessageHistory
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True  # mark as edited

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    """
    When a User is deleted, clean up related messages,
    notifications, and message history.
    """
    # Delete messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to this user
    Notification.objects.filter(user=instance).delete()

    # Delete message history edited by this user
    MessageHistory.objects.filter(edited_by=instance).delete()
