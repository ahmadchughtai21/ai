from rest_framework import serializers
from .models import Task, Tag, ChatMessage, Category, SubTask, Attachment


class TagSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'task_count']


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


class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'file_size_formatted', 'content_type', 'is_image', 'uploaded_at']
        read_only_fields = ['filename', 'file_size', 'content_type', 'uploaded_at']

    def get_file_url(self, obj):
        """Get the full URL for the file."""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None

    def get_file_size_formatted(self, obj):
        """Format file size in human-readable format."""
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


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
    attachments = AttachmentSerializer(many=True, read_only=True)
    due_time = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['category_id'].queryset = Category.objects.filter(user=request.user)
            self.fields['tag_ids'].queryset = Tag.objects.filter(user=request.user)

    def get_due_time(self, obj):
        """Format due_time in 12-hour format."""
        if obj.due_time:
            return obj.due_time.strftime('%I:%M %p')
        return None

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'status', 'media',
            'tags', 'tag_ids', 'created_at', 'updated_at',
            # New TickTick fields
            'category', 'category_id', 'category_name', 'category_detail',
            'priority', 'due_date_only', 'due_time', 'subtasks', 'attachments',
            'recurrence', 'is_recurring'
        ]

    def create(self, validated_data):
        """Auto-set is_recurring based on recurrence value."""
        if 'recurrence' in validated_data:
            validated_data['is_recurring'] = validated_data['recurrence'] != 'none'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Auto-set is_recurring based on recurrence value."""
        if 'recurrence' in validated_data:
            validated_data['is_recurring'] = validated_data['recurrence'] != 'none'
        return super().update(instance, validated_data)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp']
