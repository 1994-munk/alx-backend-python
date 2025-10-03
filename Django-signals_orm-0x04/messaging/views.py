from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse

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
