from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Task, Tag, ChatMessage, Category, SubTask, Attachment
from .serializers import TaskSerializer, TagSerializer, ChatMessageSerializer, CategorySerializer, SubTaskSerializer, AttachmentSerializer
from .groq_service import chat_with_groq

DEFAULT_CATEGORIES = [
    {'name': 'Inbox', 'color': '#3b82f6'},
    {'name': 'Work', 'color': '#ef4444'},
    {'name': 'Personal', 'color': '#10b981'},
    {'name': 'Shopping', 'color': '#f59e0b'},
    {'name': 'University', 'color': '#8b5cf6'},
    {'name': 'Budget', 'color': '#06b6d4'},
    {'name': 'Health', 'color': '#ec4899'},
    {'name': 'Projects', 'color': '#14b8a6'},
]


def ensure_default_categories(user):
    for category in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            user=user,
            name=category['name'],
            defaults={'color': category['color']}
        )


@require_http_methods(["GET"])
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('app')
    return render(request, 'todo_app/landing.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('app')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        ensure_default_categories(user)
        login(request, user)
        return redirect('app')

    return render(request, 'todo_app/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('app')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        ensure_default_categories(user)
        login(request, user)
        return redirect('app')

    return render(request, 'todo_app/login.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('home')


@api_view(['GET'])
def auth_csrf(request):
    token = get_token(request)
    return Response({'csrfToken': token})


@api_view(['GET'])
def auth_status(request):
    if request.user.is_authenticated:
        ensure_default_categories(request.user)
        return Response({'authenticated': True, 'username': request.user.username})
    return Response({'authenticated': False, 'username': None})


@api_view(['POST'])
def auth_signup(request):
    form = UserCreationForm(request.data)
    if form.is_valid():
        user = form.save()
        ensure_default_categories(user)
        login(request, user)
        return Response({'authenticated': True, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth_login(request):
    form = AuthenticationForm(request=request, data=request.data)
    if form.is_valid():
        user = form.get_user()
        ensure_default_categories(user)
        login(request, user)
        return Response({'authenticated': True, 'username': user.username})
    return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth_logout(request):
    logout(request)
    return Response({'authenticated': False, 'username': None})


# Template View
@login_required
def index(request):
    return render(request, 'todo_app/index.html')

# API Views
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """Override create to handle subtasks."""
        # Make a mutable copy of request data
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)

        # Extract subtasks from request data
        subtasks_data = data.pop('subtasks', [])

        # Create the task
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=request.user)

        # Create subtasks if provided
        if subtasks_data:
            for idx, subtask_title in enumerate(subtasks_data):
                SubTask.objects.create(
                    task=task,
                    title=subtask_title,
                    order=idx
                )

        # Reload task to include subtasks
        task.refresh_from_db()
        serializer = self.get_serializer(task)

        # Return the task with subtasks
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Override update to handle recurring tasks and subtasks."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if status is being changed
        old_status = instance.status
        new_status = request.data.get('status', old_status)

        # Make a mutable copy of request data
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)

        # Extract subtasks from request data
        subtasks_data = data.pop('subtasks', None)

        # Perform the update first
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Refresh instance to get the updated status
        instance.refresh_from_db()

        # Update subtasks if provided
        if subtasks_data is not None:
            # Clear existing subtasks and create new ones
            instance.subtasks.all().delete()
            for idx, subtask_title in enumerate(subtasks_data):
                SubTask.objects.create(
                    task=instance,
                    title=subtask_title,
                    order=idx
                )

        # Handle recurring task status changes AFTER the update
        if instance.is_recurring:
            # If marking as completed: create next occurrence
            if old_status == 'pending' and instance.status == 'completed':
                instance.create_next_occurrence()
            # If marking as pending again: delete the next occurrence
            elif old_status == 'completed' and instance.status == 'pending':
                instance.delete_next_occurrence()

        # Reload task to include updated subtasks and next occurrence
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_pending(self, request):
        """Get all pending tasks."""
        tasks = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get inbox tasks (pending tasks with no category or Inbox category)."""
        inbox_cat = Category.objects.filter(user=request.user, name='Inbox').first()
        tasks = self.get_queryset().filter(
            status='pending'
        ).filter(
            models.Q(category__isnull=True) | models.Q(category=inbox_cat)
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get tasks due today."""
        from datetime import date
        today = date.today()
        tasks = self.get_queryset().filter(
            status='pending',
            due_date_only=today
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def next7days(self, request):
        """Get tasks due in the next 7 days."""
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)
        tasks = self.get_queryset().filter(
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

        tasks = self.get_queryset().filter(category__name=category_name)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_tag(self, request):
        """Get tasks by tag name. Use ?tag=urgent"""
        tag_name = request.query_params.get('tag')
        if not tag_name:
            return Response({'error': 'tag parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = self.get_queryset().filter(tags__name=tag_name)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search tasks by title, description, or tags. Use ?q=search_term"""
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'q parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = self.get_queryset().filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get task statistics."""
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)

        user_tasks = self.get_queryset()
        total = user_tasks.count()
        pending = user_tasks.filter(status='pending').count()
        completed = user_tasks.filter(status='completed').count()

        inbox_cat = Category.objects.filter(user=request.user, name='Inbox').first()
        inbox = user_tasks.filter(
            status='pending'
        ).filter(
            models.Q(category__isnull=True) | models.Q(category=inbox_cat)
        ).count()

        today_tasks = user_tasks.filter(
            status='pending',
            due_date_only=today
        ).count()

        week_tasks = user_tasks.filter(
            status='pending',
            due_date_only__gte=today,
            due_date_only__lte=next_week
        ).count()

        overdue = user_tasks.filter(
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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pending_tasks_tags(self, request):
        """Get all tags used in pending tasks with counts."""
        from django.db.models import Count
        tags = self.get_queryset().filter(
            task__status='pending'
        ).annotate(
            task_count=Count('task')
        ).order_by('name')
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__user=self.request.user)

    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        """Toggle subtask completion status."""
        subtask = self.get_object()
        subtask.is_completed = not subtask.is_completed
        subtask.save()
        serializer = self.get_serializer(subtask)
        return Response(serializer.data)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attachment.objects.filter(task__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Upload a file attachment to a task."""
        task_id = request.data.get('task')
        file = request.FILES.get('file')

        if not task_id:
            return Response({'error': 'task_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not file:
            return Response({'error': 'file is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create attachment
        attachment = Attachment.objects.create(
            task=task,
            file=file,
            filename=file.name,
            file_size=file.size,
            content_type=file.content_type or ''
        )

        serializer = self.get_serializer(attachment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Delete an attachment and its file."""
        attachment = self.get_object()
        attachment.delete()  # This will also delete the file due to the overridden delete method
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_api(request):
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ai_response = chat_with_groq(user_message, user=request.user)
        return Response({'response': ai_response})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_chat(request):
    try:
        ChatMessage.objects.filter(user=request.user).delete()
        return Response({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
