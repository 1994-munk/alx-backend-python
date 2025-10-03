from django.db.models.signals import pre_save, post_save
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