from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Lists/Categories for organizing tasks (e.g., Work, Personal, Shopping)."""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#3b82f6', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Original fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    media = models.FileField(upload_to='task_media/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NEW TickTick-style fields (all nullable/with defaults for backward compatibility)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tasks',
        help_text='Category/List this task belongs to. Defaults to Inbox if not set.'
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='none',
        help_text='Task priority level'
    )
    due_date_only = models.DateField(
        null=True, 
        blank=True,
        help_text='Due date without time component'
    )
    due_time = models.TimeField(
        null=True, 
        blank=True,
        help_text='Due time component'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    @property
    def category_name(self):
        """Returns category name or 'Inbox' as default."""
        return self.category.name if self.category else 'Inbox'


class SubTask(models.Model):
    """Checklist items within a task."""
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='subtasks'
    )
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text='Display order')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.task.title} - {self.title}"

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('model', 'Model'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
