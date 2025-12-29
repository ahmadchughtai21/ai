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

    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
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
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default='none',
        help_text='Task recurrence pattern'
    )
    is_recurring = models.BooleanField(
        default=False,
        help_text='Whether this task is a recurring task'
    )
    next_occurrence = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_occurrence',
        help_text='Link to the next occurrence of this recurring task'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def category_name(self):
        """Returns category name or 'Inbox' as default."""
        return self.category.name if self.category else 'Inbox'

    def get_next_occurrence_date(self):
        """Calculate the next occurrence date based on recurrence pattern."""
        if not self.due_date_only or self.recurrence == 'none':
            return None

        from datetime import timedelta
        from dateutil.relativedelta import relativedelta

        base_date = self.due_date_only

        if self.recurrence == 'daily':
            return base_date + timedelta(days=1)
        elif self.recurrence == 'weekly':
            return base_date + timedelta(weeks=1)
        elif self.recurrence == 'monthly':
            return base_date + relativedelta(months=1)
        elif self.recurrence == 'yearly':
            return base_date + relativedelta(years=1)

        return None

    def create_next_occurrence(self):
        """Create the next occurrence of this recurring task."""
        if not self.is_recurring or self.recurrence == 'none':
            return None

        # If next occurrence already exists, don't create another
        if self.next_occurrence:
            return self.next_occurrence

        next_date = self.get_next_occurrence_date()
        if not next_date:
            return None

        # Create a new task with the same properties but new due date
        new_task = Task.objects.create(
            title=self.title,
            description=self.description,
            priority=self.priority,
            category=self.category,
            due_date_only=next_date,
            due_time=self.due_time,
            recurrence=self.recurrence,
            is_recurring=True,
            status='pending'
        )

        # Copy tags
        new_task.tags.set(self.tags.all())

        # Copy subtasks (checklist items)
        for subtask in self.subtasks.all():
            SubTask.objects.create(
                task=new_task,
                title=subtask.title,
                is_completed=False,  # Reset completion status for new occurrence
                order=subtask.order
            )

        # Link this task to the next occurrence
        self.next_occurrence = new_task
        self.save(update_fields=['next_occurrence'])

        return new_task

    def delete_next_occurrence(self):
        """Delete the next occurrence if this task is marked pending again."""
        if self.next_occurrence:
            next_task = self.next_occurrence
            self.next_occurrence = None
            self.save(update_fields=['next_occurrence'])
            next_task.delete()
            return True
        return False


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


class Attachment(models.Model):
    """File attachments for tasks."""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='task_attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text='File size in bytes')
    content_type = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.task.title} - {self.filename}"

    @property
    def is_image(self):
        """Check if attachment is an image."""
        image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
        return self.content_type in image_types

    def delete(self, *args, **kwargs):
        """Override delete to also delete the file from storage."""
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


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
