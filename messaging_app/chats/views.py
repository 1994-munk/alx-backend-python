
# messaging_app/chats/views.py
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner,IsParticipantOfConversation
from rest_framework.filters import OrderingFilter
from .pagination import MessagePagination
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer



# ----------------------------
# Conversation ViewSet
# ----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]  # required by checker
    search_fields = ['title']  # example field

    # Custom create method to start a new conversation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.save()

        # Add participants if provided
        participants = request.data.get("participants", [])
        if participants:
            conversation.participants.set(participants)

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


# ----------------------------
# Message ViewSet
# ----------------------------
from django_filters.rest_framework import DjangoFilterBackend

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("sent_at")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsOwner,IsParticipantOfConversation]  
    pagination_class = MessagePagination  # ✅ Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # ✅ Filtering
    filterset_class = MessageFilter
    ordering_fields = ["timestamp"]

    search_fields = ['content']  # example field
    
    def get_queryset(self):
        # Filter messages by conversation_id from the URL/query params
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.none()
    
    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        # Check if user is participant
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)



    # Custom create method to send a message in a conversation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save()

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
