from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class EmojiSerializer(serializers.Serializer):
    emoji_text = serializers.CharField()
