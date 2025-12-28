from django.shortcuts import render
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Task, Tag, ChatMessage, Category, SubTask
from .serializers import TaskSerializer, TagSerializer, ChatMessageSerializer, CategorySerializer, SubTaskSerializer
from .groq_service import chat_with_groq

# Template View
def index(request):
    return render(request, 'todo_app/index.html')

# API Views
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def all_pending(self, request):
        """Get all pending tasks."""
        tasks = Task.objects.filter(status='pending').order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get inbox tasks (pending tasks with no category or Inbox category)."""
        inbox_cat = Category.objects.filter(name='Inbox').first()
        tasks = Task.objects.filter(
            status='pending'
        ).filter(
            models.Q(category__isnull=True) | models.Q(category=inbox_cat)
        ).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get tasks due today."""
        from datetime import date
        today = date.today()
        tasks = Task.objects.filter(
            status='pending',
            due_date_only=today
        ).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def next7days(self, request):
        """Get tasks due in the next 7 days."""
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)
        tasks = Task.objects.filter(
            status='pending',
            due_date_only__gte=today,
            due_date_only__lte=next_week
        ).order_by('due_date_only')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get tasks by category name. Use ?category=Work"""
        category_name = request.query_params.get('category')
        if not category_name:
            return Response({'error': 'category parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(category__name=category_name).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_tag(self, request):
        """Get tasks by tag name. Use ?tag=urgent"""
        tag_name = request.query_params.get('tag')
        if not tag_name:
            return Response({'error': 'tag parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(tags__name=tag_name).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search tasks by title or description. Use ?q=search_term"""
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'q parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        ).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get task statistics."""
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)

        total = Task.objects.count()
        pending = Task.objects.filter(status='pending').count()
        completed = Task.objects.filter(status='completed').count()

        inbox_cat = Category.objects.filter(name='Inbox').first()
        inbox = Task.objects.filter(
            status='pending'
        ).filter(
            models.Q(category__isnull=True) | models.Q(category=inbox_cat)
        ).count()

        today_tasks = Task.objects.filter(
            status='pending',
            due_date_only=today
        ).count()

        week_tasks = Task.objects.filter(
            status='pending',
            due_date_only__gte=today,
            due_date_only__lte=next_week
        ).count()

        overdue = Task.objects.filter(
            status='pending',
            due_date_only__lt=today
        ).count()

        return Response({
            'total': total,
            'pending': pending,
            'completed': completed,
            'inbox': inbox,
            'today': today_tasks,
            'next_7_days': week_tasks,
            'overdue': overdue
        })

    @action(detail=True, methods=['post'])
    def add_subtask(self, request, pk=None):
        """Add a subtask to this task."""
        task = self.get_object()
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        subtask = SubTask.objects.create(
            task=task,
            title=title,
            order=task.subtasks.count()
        )
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=False, methods=['get'])
    def pending_tasks_tags(self, request):
        """Get all tags used in pending tasks with counts."""
        from django.db.models import Count
        tags = Tag.objects.filter(
            task__status='pending'
        ).annotate(
            task_count=Count('task')
        ).order_by('name')
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        """Toggle subtask completion status."""
        subtask = self.get_object()
        subtask.is_completed = not subtask.is_completed
        subtask.save()
        serializer = self.get_serializer(subtask)
        return Response(serializer.data)


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

