from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'bio', 'is_online']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

class DummySerializer(serializers.Serializer):
    dummy_field = serializers.CharField()

    def get_dummy(self):
        return "dummy"

    dummy_method_field = serializers.SerializerMethodField()

    def validate_dummy_field(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value