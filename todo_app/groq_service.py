import os
from groq import Groq
from django.conf import settings
from .models import Task, Tag, ChatMessage, Category, SubTask
import json
from datetime import datetime, time, timedelta
from django.utils import timezone

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"



SYSTEM_INSTRUCTION = """
You are a TickTick-style Todo List Assistant. Your primary purpose is to help users manage their tasks with advanced features like categories, priorities, due dates, and subtasks.

**FRIENDLY CONVERSATION:**
You can respond to:
- Greetings (hi, hello, hey, good morning, etc.) - Respond warmly and ask how you can help with tasks
- Thank you / appreciation - Respond politely
- Casual pleasantries - Respond briefly and redirect to tasks
- Simple questions about what you can do - Explain your capabilities

**STRICT SCOPE FOR COMPLEX REQUESTS:**
You MUST REJECT detailed requests that are NOT related to task management:
- Recipes, cooking instructions
- General knowledge questions (history, science, etc.)
- Weather information
- Coding help (unless it's about tasks related to coding projects)
- Math problems
- Translations
- Stories or entertainment
- Any other non-task-management topics

**TASK MANAGEMENT INCLUDES:**
- Creating, updating, deleting tasks
- Viewing tasks (all, pending, completed)
- Asking about task counts, statistics (e.g., "how many tasks completed?", "what's done?", "show completed tasks")
- Task organization (categories, priorities, due dates)
- Any questions about the user's tasks and their status

For non-task requests (not greetings), respond with:
{
  "commands": [],
  "user_message": "I'm focused on helping you manage your tasks. I can't help with [topic]. Would you like to create, update, or view your tasks instead?",
  "system_note": null
}

**YOUR RESPONSE MUST BE VALID JSON in this exact format:**
{
  "commands": [
    {
      "action": "create_task" | "update_task" | "delete_task" | "delete_all_tasks" | "create_category" | null,
      "data": {task/category details},
      "task_identifier": "title of task to update/delete" (for update/delete only)
    }
  ],
  "user_message": "Natural language response to show the user",
  "system_note": "Admin note if needed, otherwise null"
}

**COMMAND RULES:**

1. create_task - create new task
   data: {
     "title": str (required),
     "description": str,
     "category_name": str (e.g., "Work", "Personal", "Shopping" - will auto-create if doesn't exist),
     "priority": "none" | "low" | "medium" | "high",
     "due_date": "YYYY-MM-DD" (e.g., "2025-01-15"),
     "due_time": "HH:MM AM/PM" (12-hour format),
     "tags": [str],
     "subtasks": [str] (list of subtask titles)
   }

2. update_task - update existing task
   data: Same fields as create_task (only include fields being changed)
   task_identifier: exact title of task from current list

3. delete_task - delete one task
   task_identifier: exact title of task from current list

4. delete_all_tasks - delete all tasks (no data needed)

5. create_category - create new category/list
   data: {
     "name": str (required),
     "color": str (hex color, e.g., "#3b82f6")
   }

6. action: null - no database action needed (just answering task-related questions)

**SMART DATE PARSING:**
- "today" → use today's date (2025-12-28)
- "tomorrow" → use tomorrow's date (2025-12-29)
- "thursday", "next thursday" → calculate next occurring Thursday from today
- "next monday", "next week" → calculate appropriate date
- "in 3 days" → add 3 days to today
- CRITICAL: Current year is 2025. Always use dates in 2025 or later, NEVER 2024 or earlier
- Always use YYYY-MM-DD format in response with correct year (2025 or later)

**TIME FORMAT:**
- Use 12-hour format: "8:00 PM", "9:30 AM", "5:00 PM"
- When user says "8pm tonight" or "8pm today", use "8:00 PM"

**PRIORITY MAPPING:**
- "important", "urgent", "critical" → "high"
- "normal" → "medium"
- "someday", "maybe" → "low"
- Default → "none"

**CATEGORY/LIST LOGIC:**
- If user mentions a category that doesn't exist, CREATE IT automatically
- Default category is "Inbox" (created automatically if needed)
- Examples: "Work", "Personal", "Shopping", "University", "Budget"

**SUBTASKS:**
- When user says "with steps", "checklist", or lists items, create subtasks
- Example: "Buy groceries with milk, bread, eggs" → create task with 3 subtasks

**STATUS RULES:**
- "mark as done", "complete it", "set to done" → status: "completed"
- "mark as pending", "reopen" → status: "pending"

**IMPORTANT:**
- user_message MUST be friendly and natural, NEVER show JSON or technical details
- When updating, use task_identifier to match the task title from CURRENT TASKS
- Multiple commands allowed in one response
- Only include fields being changed in update_task data

**EXAMPLES:**

User: "how to make biryani?"
Response:
{
  "commands": [],
  "user_message": "Sorry, I can't help with that. I'm a todo list assistant and can only help you manage your tasks. Would you like to create, update, or view your tasks?",
  "system_note": null
}

User: "add high priority task to finish the report in Work category due tomorrow at 5pm"
Response:
{
  "commands": [{
    "action": "create_task",
    "data": {
      "title": "finish the report",
      "category_name": "Work",
      "priority": "high",
      "due_date": "2025-12-29",
      "due_time": "5:00 PM"
    }
  }],
  "user_message": "Created high priority task 'finish the report' in Work category, due tomorrow at 5:00 PM!",
  "system_note": null
}

User: "create shopping list for groceries with milk, bread, and eggs"
Response:
{
  "commands": [{
    "action": "create_task",
    "data": {
      "title": "groceries",
      "category_name": "Shopping",
      "subtasks": ["milk", "bread", "eggs"]
    }
  }],
  "user_message": "Created task 'groceries' in Shopping category with 3 items on your checklist!",
  "system_note": null
}

User: "mark finish report as done"
Response:
{
  "commands": [{
    "action": "update_task",
    "data": {"status": "completed"},
    "task_identifier": "finish the report"
  }],
  "user_message": "Marked 'finish the report' as completed! Great job! 🎉",
  "system_note": null
}
"""

def parse_time_to_datetime(time_str):
    """Convert 12-hour time format to datetime for today."""
    try:
        # Parse time like "8:00 PM" or "9:30 AM"
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        # Combine with today's date
        now = timezone.now()
        result = datetime.combine(now.date(), time_obj)
        # Make it timezone aware
        return timezone.make_aware(result)
    except Exception:
        return None


def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def execute_commands(commands, current_tasks):
    """Execute the commands and return results."""
    results = []
    errors = []

    for cmd in commands:
        action = cmd.get("action")
        data = cmd.get("data", {})
        task_identifier = cmd.get("task_identifier")

        try:
            if action == "create_category":
                name = data.get("name")
                if not name:
                    errors.append("Category name is required")
                    continue

                category, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'color': data.get("color", "#3b82f6")}
                )
                if created:
                    results.append(f"Created category: {name}")
                else:
                    results.append(f"Category '{name}' already exists")

            elif action == "create_task":
                title = data.get("title")
                if not title:
                    errors.append("Title is required for creating task")
                    continue

                # Handle category
                category = None
                category_name = data.get("category_name", "Inbox")
                if category_name:
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'color': '#3b82f6'}
                    )

                task = Task.objects.create(
                    title=title,
                    description=data.get("description", ""),
                    category=category,
                    priority=data.get("priority", "none")
                )

                # Handle due date
                if "due_date" in data:
                    due_date = parse_date(data["due_date"])
                    if due_date:
                        task.due_date_only = due_date

                # Handle due time
                if "due_time" in data:
                    try:
                        time_obj = datetime.strptime(data["due_time"], "%I:%M %p").time()
                        task.due_time = time_obj

                        # Also set combined due_date for backward compatibility
                        date_to_use = task.due_date_only if task.due_date_only else timezone.now().date()
                        combined_dt = datetime.combine(date_to_use, time_obj)
                        task.due_date = timezone.make_aware(combined_dt)
                    except Exception:
                        pass

                # Handle tags
                if "tags" in data:
                    for tag_name in data["tags"]:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        task.tags.add(tag)

                task.save()

                # Handle subtasks
                if "subtasks" in data:
                    for idx, subtask_title in enumerate(data["subtasks"]):
                        SubTask.objects.create(
                            task=task,
                            title=subtask_title,
                            order=idx
                        )

                results.append(f"Created task: {title} (ID: {task.id})")

            elif action == "update_task":
                if not task_identifier:
                    errors.append("task_identifier required for update")
                    continue

                # Find task by title (case-insensitive)
                task = None
                for t in current_tasks:
                    if t['title'].lower() == task_identifier.lower():
                        task = Task.objects.get(id=t['id'])
                        break

                if not task:
                    errors.append(f"Task '{task_identifier}' not found")
                    continue

                # Update fields
                if "title" in data:
                    task.title = data["title"]
                if "description" in data:
                    task.description = data["description"]
                if "status" in data:
                    task.status = data["status"]
                if "priority" in data:
                    task.priority = data["priority"]
                if "category_name" in data:
                    category, _ = Category.objects.get_or_create(
                        name=data["category_name"],
                        defaults={'color': '#3b82f6'}
                    )
                    task.category = category
                if "due_date" in data:
                    due_date = parse_date(data["due_date"])
                    if due_date:
                        task.due_date_only = due_date
                if "due_time" in data:
                    try:
                        time_obj = datetime.strptime(data["due_time"], "%I:%M %p").time()
                        task.due_time = time_obj

                        # Update combined due_date
                        date_to_use = task.due_date_only if task.due_date_only else timezone.now().date()
                        combined_dt = datetime.combine(date_to_use, time_obj)
                        task.due_date = timezone.make_aware(combined_dt)
                    except Exception:
                        pass
                if "tags" in data:
                    task.tags.clear()
                    for tag_name in data["tags"]:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        task.tags.add(tag)
                if "subtasks" in data:
                    # Clear existing subtasks and add new ones
                    task.subtasks.all().delete()
                    for idx, subtask_title in enumerate(data["subtasks"]):
                        SubTask.objects.create(
                            task=task,
                            title=subtask_title,
                            order=idx
                        )

                task.save()
                results.append(f"Updated task: {task.title} (ID: {task.id})")

            elif action == "delete_task":
                if not task_identifier:
                    errors.append("task_identifier required for delete")
                    continue

                # Find and delete task
                task = None
                for t in current_tasks:
                    if t['title'].lower() == task_identifier.lower():
                        task = Task.objects.get(id=t['id'])
                        break

                if task:
                    task.delete()
                    results.append(f"Deleted task: {task_identifier}")
                else:
                    errors.append(f"Task '{task_identifier}' not found")

            elif action == "delete_all_tasks":
                count, _ = Task.objects.all().delete()
                results.append(f"Deleted all {count} tasks")

        except Exception as e:
            errors.append(f"Error executing {action}: {str(e)}")

    return results, errors


def chat_with_groq(user_message_text):
    """Process user message and execute task commands."""
    # 1. Save user message
    ChatMessage.objects.create(role='user', content=user_message_text)

    # 2. Get current tasks from database
    tasks_query = Task.objects.all()
    current_tasks = []
    for t in tasks_query:
        subtasks_list = [{"title": st.title, "completed": st.is_completed} for st in t.subtasks.all()]
        current_tasks.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "category": t.category_name,
            "priority": t.priority,
            "due_date": t.due_date_only.strftime("%Y-%m-%d") if t.due_date_only else None,
            "due_time": t.due_time.strftime("%I:%M %p") if t.due_time else None,
            "due_date_full": t.due_date.strftime("%I:%M %p on %m/%d/%Y") if t.due_date else None,
            "status": t.status,
            "tags": [tag.name for tag in t.tags.all()],
            "subtasks": subtasks_list
        })

    # 3. Get current categories
    categories_list = [{"name": cat.name, "color": cat.color} for cat in Category.objects.all()]

    # 4. Build context with current tasks and categories (separate by status)
    pending_tasks = [t for t in current_tasks if t['status'] == 'pending']
    completed_tasks = [t for t in current_tasks if t['status'] == 'completed']

    context_data = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "categories": categories_list
    }

    tasks_context = f"""

CURRENT TASKS IN DATABASE:
Pending Tasks ({len(pending_tasks)}): {json.dumps(pending_tasks, indent=2)}
Completed Tasks ({len(completed_tasks)}): {json.dumps(completed_tasks, indent=2)}

AVAILABLE CATEGORIES:
{json.dumps(categories_list, indent=2)}

IMPORTANT: When user asks about completed tasks, use the Completed Tasks list above. When they ask about pending/active tasks, use the Pending Tasks list."""

    system_message = SYSTEM_INSTRUCTION + tasks_context

    # 5. Get last 2 conversation pairs for context (last 2 user + last 2 assistant messages)
    recent_messages = ChatMessage.objects.order_by('-timestamp')[:4]  # Get last 4 messages
    conversation_history = []

    for msg in reversed(recent_messages):  # Reverse to get chronological order
        if msg.content.strip():  # Only add non-empty messages
            # Map 'model' role to 'assistant' for Groq API compatibility
            role = 'assistant' if msg.role == 'model' else msg.role
            conversation_history.append({
                "role": role,
                "content": msg.content
            })

    # Build messages array: system + conversation history + current user message
    messages = [{"role": "system", "content": system_message}]
    messages.extend(conversation_history)

    # Only add current user message if it's not already in history
    if not conversation_history or conversation_history[-1].get("content") != user_message_text:
        messages.append({"role": "user", "content": user_message_text})

    # 5. Get AI response
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )

        ai_response_text = response.choices[0].message.content

        # Parse JSON response
        try:
            response_data = json.loads(ai_response_text)
        except json.JSONDecodeError:
            # If AI didn't return valid JSON, create a simple response
            ChatMessage.objects.create(role='model', content=ai_response_text)
            return ai_response_text

        # Execute commands
        commands = response_data.get("commands", [])
        user_message = response_data.get("user_message", "")
        system_note = response_data.get("system_note")

        if commands:
            results, errors = execute_commands(commands, current_tasks)

            # Log to terminal for admin
            if results:
                print(f"\n[TODO APP] Executed commands: {', '.join(results)}")
            if errors:
                print(f"\n[TODO APP ERROR] {', '.join(errors)}")
            if system_note:
                print(f"\n[TODO APP NOTE] {system_note}")

        # Save AI response
        if user_message:
            ChatMessage.objects.create(role='model', content=user_message)

        return user_message if user_message else "Task processed."

    except Exception as e:
        error_msg = f"Error communicating with Groq: {str(e)}"
        print(f"\n[TODO APP ERROR] {error_msg}")
        return error_msg

