from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Also register messages as a standalone endpoint
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]