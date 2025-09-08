from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MessageSerializer, EmojiSerializer
from . import crypto_utils

_PRIV, _PUB = crypto_utils.generate_keys()

@api_view(['POST'])
def encrypt_message(request):
    serializer = MessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    msg = serializer.validated_data['message'].encode('utf-8')
    try:
        enc = crypto_utils.encrypt(_PUB, msg)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    return Response({"encrypted": enc})

@api_view(['POST'])
def decrypt_message(request):
    serializer = EmojiSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    emoji_text = serializer.validated_data['emoji_text']
    try:
        dec = crypto_utils.decrypt(_PRIV, emoji_text)
        return Response({"message": dec.decode('utf-8')})
    except Exception as e:
        return Response({"error": str(e)}, status=400)
