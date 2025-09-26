from django.urls import path,include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter  # ✅ import from the nested package

from .views import ConversationViewSet, MessageViewSet  # ✅ correct import
from rest_framework.routers import DefaultRouter
from rest_framework import routers

# Use DRF router to auto-generate routes
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Nested router for messages inside conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
]
