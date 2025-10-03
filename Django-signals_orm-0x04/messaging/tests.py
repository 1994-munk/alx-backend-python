from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification,MessageHistory
class SignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="12345")
        self.user2 = User.objects.create_user(username="bob", password="12345")

    def test_notification_created_on_message(self):
        # Send a message
        msg = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello Bob!"
        )

        # Check if notification exists for Bob
        notif = Notification.objects.filter(user=self.user2, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)

class MessageEditTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="12345")
        self.user2 = User.objects.create_user(username="bob", password="12345")
        self.message = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Original"
        )

    def test_message_edit_creates_history(self):
        # Update message content
        self.message.content = "Updated content"
        self.message.save()

        # Check if history exists
        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original")
        self.assertTrue(self.message.edited)