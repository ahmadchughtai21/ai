from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Tag, ChatMessage
from .serializers import TaskSerializer, TagSerializer, ChatMessageSerializer
from .groq_service import chat_with_groq

# Template View
def index(request):
    return render(request, 'todo_app/index.html')

# API Views
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['POST'])
def chat_api(request):
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ai_response = chat_with_groq(user_message)
        return Response({'response': ai_response})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def chat_history(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def clear_chat(request):
    try:
        ChatMessage.objects.all().delete()
        return Response({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

