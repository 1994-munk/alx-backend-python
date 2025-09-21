from django.urls import path,include
from .views import ConversationViewSet, MessageViewSet  # ✅ correct import
from rest_framework.routers import DefaultRouter


# Use DRF router to auto-generate routes
router = "routers.DefaultRouter()"
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
