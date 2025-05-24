from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer 
from django_filters.rest_framework import DjangoFilterBackend




class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]  # For testing
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['conversation_id']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save() 
        if request.user.is_authenticated:
            conversation.participants.add(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]  # For testing
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set sender to authenticated user if available, otherwise use the first user
        if request.user.is_authenticated:
            serializer.save(sender=request.user)
        else:
            # For testing purposes, use the first user
            first_user = User.objects.first()
            if first_user:
                serializer.save(sender=first_user)
            else:
                return Response(
                    {"detail": "No users available for testing."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)