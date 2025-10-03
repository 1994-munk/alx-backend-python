from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


def delete_user(request, user_id):
    """
    View that deletes a user and triggers post_delete signal
    to clean up related data.
    """
    user = get_object_or_404(User, id=user_id)

    # Only allow deleting your own account (basic safety check)
    if request.user != user:
        return HttpResponse("You are not allowed to delete this account.", status=403)

    username = user.username
    user.delete()  # This triggers post_delete signal
    messages.success(request, f"User '{username}' and related data deleted successfully.")
    return redirect("/")  # Redirect somewhere safe

def conversation_view(request, user_id):
    # Fetch messages for this user and prefetch replies
    messages = (
        Message.objects
        .filter(receiver_id=user_id)
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies")  # Optimized fetching
        .order_by("-created_at")
    )

    return render(request, "messaging/conversation.html", {"messages": messages})

# Fetch a root message with full thread
root_message = Message.objects.get(id=1)
conversation = root_message.get_thread()

# Recursive function to get all replies for a given message
def get_replies(message):
    replies = Message.objects.filter(parent_message=message).select_related("sender", "receiver")
    thread = []
    for reply in replies:
        thread.append({
            "message": reply,
            "replies": get_replies(reply)  # recursion to fetch nested replies
        })
    return thread

def inbox(request):
    # ✅ Use the custom manager
    unread_messages = Message.unread.unread_for_user(request.user).only(
        "id", "sender", "content", "created_at"
    )

    return render(request, "messaging/inbox.html", {"messages": unread_messages})


@login_required
def threaded_conversation(request, message_id):
    """
    Display a threaded conversation starting from a root message.
    Uses select_related + prefetch_related to optimize queries.
    """
    # Only fetch messages belonging to the logged-in user
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver").prefetch_related("replies"),
        id=message_id,
        sender=request.user
    )

    conversation = {
        "root": root_message,
        "replies": get_replies(root_message)
    }

    return render(request, "messaging/threaded_conversation.html", {"conversation": conversation})

 @login_required
 def unread_inbox(request):
    """
    Show all unread messages for the logged-in user.
    """
    unread_messages = Message.unread.for_user(request.user)

    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})   
