from django.contrib import admin
from .models import Task, Tag, ChatMessage, Category, SubTask, Attachment


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ['title', 'is_completed', 'order']


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    fields = ['file', 'filename', 'file_size', 'content_type', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'task_count', 'created_at']
    list_filter = ['user']
    search_fields = ['name', 'user__username']

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'priority', 'status', 'due_date_only', 'created_at']
    list_filter = ['user', 'status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    filter_horizontal = ['tags']
    inlines = [SubTaskInline, AttachmentInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description', 'status')
        }),
        ('Organization', {
            'fields': ('category', 'priority', 'tags')
        }),
        ('Dates', {
            'fields': ('due_date_only', 'due_time', 'due_date')
        }),
        ('Media', {
            'fields': ('media',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['user']
    search_fields = ['name', 'user__username']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'is_completed', 'order']
    list_filter = ['is_completed']
    search_fields = ['title', 'task__title']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'content_preview', 'timestamp']
    list_filter = ['user', 'role', 'timestamp']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
