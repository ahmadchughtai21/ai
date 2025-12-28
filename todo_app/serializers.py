from rest_framework import serializers
from .models import Task, Tag, ChatMessage, Category, SubTask


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'task_count', 'created_at']

    def get_task_count(self, obj):
        return obj.tasks.filter(status='pending').count()


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'is_completed', 'order', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tag.objects.all(), source='tags', required=False
    )
    category_name = serializers.ReadOnlyField()
    category_detail = CategorySerializer(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Category.objects.all(), source='category', required=False, allow_null=True
    )
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'status', 'media',
            'tags', 'tag_ids', 'created_at', 'updated_at',
            # New TickTick fields
            'category', 'category_id', 'category_name', 'category_detail',
            'priority', 'due_date_only', 'due_time', 'subtasks'
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp']
