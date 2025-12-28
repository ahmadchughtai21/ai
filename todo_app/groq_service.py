import os
from groq import Groq
from django.conf import settings
from .models import Task, Tag, ChatMessage
import json
from datetime import datetime, time
from django.utils import timezone

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"



SYSTEM_INSTRUCTION = """
You are a Todo List Assistant. Your ONLY purpose is to help users manage their todo tasks.

**STRICT SCOPE RESTRICTION:**
You MUST REJECT any request that is NOT related to task management. This includes but not limited to:
- Recipes (biryani, cooking, etc.)
- General knowledge questions
- Weather information
- Coding help (unless it's about tasks related to coding)
- Math problems
- Translations
- Stories or entertainment
- Any other non-task-management topics

If the user asks about anything NOT related to managing their todo list, respond with:
{
  "commands": [],
  "user_message": "Sorry, I can't help with that. I'm a todo list assistant and can only help you manage your tasks. Would you like to create, update, or view your tasks?",
  "system_note": null
}

**YOUR RESPONSE MUST BE VALID JSON in this exact format:**
{
  "commands": [
    {
      "action": "create_task" | "update_task" | "delete_task" | "delete_all_tasks" | null,
      "data": {task details},
      "task_identifier": "title of task to update/delete" (for update/delete only)
    }
  ],
  "user_message": "Natural language response to show the user",
  "system_note": "Admin note if needed, otherwise null"
}

**COMMAND RULES:**
- action: "create_task" - create new task
  data: {"title": str (required), "description": str, "due_time": "HH:MM AM/PM" (12-hour format), "tags": [str]}

- action: "update_task" - update existing task
  data: {"title": str, "description": str, "status": "pending"|"completed", "due_time": "HH:MM AM/PM", "tags": [str]}
  task_identifier: exact title of task from current list

- action: "delete_task" - delete one task
  task_identifier: exact title of task from current list

- action: "delete_all_tasks" - delete all tasks

- action: null - no database action needed (just answering task-related questions)

**TIME FORMAT:**
- Use 12-hour format: "8:00 PM", "9:30 AM", "5:00 PM"
- When user says "8pm tonight" or "8pm today", use "8:00 PM"
- When user says "tomorrow at 9am", note it in description and use "9:00 AM"

**STATUS RULES:**
- "mark as done", "complete it", "set to done" → status: "completed"
- "mark as pending", "reopen" → status: "pending"

**IMPORTANT:**
- user_message MUST be friendly and natural, NEVER show JSON or technical details
- When updating, use task_identifier to match the task title from CURRENT TASKS
- Multiple commands allowed in one response (e.g., create multiple tasks)
- Only include fields being changed in update_task data

**EXAMPLES:**

User: "how to make biryani?"
Response:
{
  "commands": [],
  "user_message": "Sorry, I can't help with that. I'm a todo list assistant and can only help you manage your tasks. Would you like to create, update, or view your tasks?",
  "system_note": null
}

User: "add task buy milk"
Response:
{
  "commands": [{"action": "create_task", "data": {"title": "buy milk"}}],
  "user_message": "Task 'buy milk' has been added!",
  "system_note": null
}

User: "mark drink water as done"
Response:
{
  "commands": [{"action": "update_task", "data": {"status": "completed"}, "task_identifier": "drink water"}],
  "user_message": "Marked 'drink water' as completed!",
  "system_note": null
}

User: "set clean shoes due to 8pm"
Response:
{
  "commands": [{"action": "update_task", "data": {"due_time": "8:00 PM"}, "task_identifier": "clean shoes"}],
  "user_message": "Set 'clean shoes' due time to 8:00 PM!",
  "system_note": null
}

User: "do i have any tasks?"
Response:
{
  "commands": [],
  "user_message": "You have 3 tasks: drink water, clean shoes, decide cloths.",
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


def execute_commands(commands, current_tasks):
    """Execute the commands and return results."""
    results = []
    errors = []

    for cmd in commands:
        action = cmd.get("action")
        data = cmd.get("data", {})
        task_identifier = cmd.get("task_identifier")

        try:
            if action == "create_task":
                title = data.get("title")
                if not title:
                    errors.append("Title is required for creating task")
                    continue

                task = Task.objects.create(
                    title=title,
                    description=data.get("description", "")
                )

                # Handle due time
                if "due_time" in data:
                    due_dt = parse_time_to_datetime(data["due_time"])
                    if due_dt:
                        task.due_date = due_dt

                # Handle tags
                if "tags" in data:
                    for tag_name in data["tags"]:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        task.tags.add(tag)

                task.save()
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
                if "due_time" in data:
                    due_dt = parse_time_to_datetime(data["due_time"])
                    if due_dt:
                        task.due_date = due_dt
                if "tags" in data:
                    task.tags.clear()
                    for tag_name in data["tags"]:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        task.tags.add(tag)

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
        current_tasks.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "due_date": t.due_date.strftime("%I:%M %p on %m/%d/%Y") if t.due_date else None,
            "status": t.status,
            "tags": [tag.name for tag in t.tags.all()]
        })

    # 3. Build context with current tasks
    tasks_context = f"\n\nCURRENT TASKS IN DATABASE:\n{json.dumps(current_tasks, indent=2)}"
    system_message = SYSTEM_INSTRUCTION + tasks_context

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message_text}
    ]

    # 4. Get AI response
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

