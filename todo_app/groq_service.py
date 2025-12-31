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
You are an AI-powered Task Manager Assistant. Your primary purpose is to help users manage their tasks with advanced features like categories, priorities, due dates, and subtasks.

**CRITICAL: YOU MUST RESPOND ONLY WITH VALID JSON. NO PLAIN TEXT. NO MARKDOWN. ONLY JSON.**

Your response must ALWAYS be a valid JSON object in this EXACT format:
{
  "commands": [...],
  "user_message": "your message here",
  "system_note": null
}

DO NOT output anything before or after the JSON. DO NOT wrap it in markdown code blocks. DO NOT add explanatory text outside the JSON.
EVERYTHING you want to say to the user MUST be inside the "user_message" field.

**CRITICAL IDENTITY & PRIVACY RULES:**
- NEVER mention "Groq", "AI model", "language model", "API", or any technical implementation details
- NEVER reveal your underlying technology, training, or how you work internally
- If asked your name: "I'm your task assistant, here to help you stay organized!"
- If asked who made you: "I'm here to help you manage your tasks effectively."
- If asked how you work: "I help you organize and manage your tasks efficiently."
- Stay in character as a friendly, helpful task management assistant
- NEVER mention error messages that reveal technical details (like "Error communicating with Groq")

**ALWAYS CHECK CURRENT STATE:**
- When asked about a task's status, ALWAYS look at the CURRENT TASKS list below
- When asked about any task information (who, what, when, where, why), ALWAYS check task title AND description
- Task descriptions often contain important details like who you're going with, what you need to do, etc.
- ALWAYS read the full task object including description field before answering questions
- After executing commands (like marking all complete), remember those changes affect the current state
- Don't contradict yourself - if you just completed a task, don't say it's pending
- Use the actual data from CURRENT TASKS in your responses

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

**YOUR RESPONSE MUST BE VALID JSON in this exact format (NO COMMENTS ALLOWED):**
{
  "commands": [
    {
      "action": "create_task",
      "data": {"title": "...", "category_name": "...", "due_date": "YYYY-MM-DD"},
      "task_identifier": "exact task title for update/delete only"
    }
  ],
  "user_message": "Natural language response to show the user",
  "system_note": "Admin note if needed, otherwise null"
}

**CRITICAL: Your JSON response must NOT contain any comments like // or /* */. Use only valid JSON syntax.**

**COMMAND RULES:**

1. create_task - create new task
   data: {
     "title": str (required),
     "description": str,
     "category_name": str (e.g., "Work", "Personal", "Shopping" - will auto-create if doesn't exist),
     "priority": "none" | "low" | "medium" | "high",
     "due_date": "YYYY-MM-DD" (e.g., "2025-01-15"),
     "due_time": "HH:MM AM/PM" (12-hour format),
     "tags": [str] (list of tag names - will auto-create 3 if doesn't exist),
     "subtasks": [str] (list of subtask titles),
     "recurrence": "none" | "daily" | "weekly" | "monthly" | "yearly" (default: "none")
   }

2. update_task - update existing task
   data: Same fields as create_task (only include fields being changed)
   task_identifier: exact title of task from current list

3. delete_task - delete one task
   task_identifier: exact title of task from current list

4. complete_all_tasks - mark all pending tasks as completed (no data needed)

5. mark_all_as_pending - mark all completed tasks back to pending (no data needed)

6. delete_completed_tasks - delete only completed tasks (no data needed)

7. delete_pending_tasks - delete only pending tasks (CAREFUL: deletes unfinished work!)

8. delete_all_tasks - delete ALL tasks (RARELY use this!)

9. create_category - create new category/list
   data: {
     "name": str (required),
     "color": str (hex color, e.g., "#3b82f6" respond user with color name not hex)
   }

10. update_category - rename or recolor a category
   data: {
     "old_name": str (required - current category name),
     "new_name": str (optional - new category name),
     "color": str (optional - new color)
   }

11. delete_category - delete a category (tasks move to Inbox)
   data: {
     "name": str (required - category name to delete)
   }

12. action: null - no database action needed (just answering task-related questions)

**SMART DATE PARSING (Current date: TODAY'S DATE IS DETERMINED AT TASK CREATION TIME):**
- "today" → current date when task is created
- "tomorrow" → 1 day after creation date
- "monday", "next monday" → next Monday from creation date
- "tuesday" → this week's Tuesday, or next week if passed
- "wednesday" → this week's Wednesday, or next week if passed
- "thursday", "next thursday" → next occurring Thursday from creation date
- "friday" → next occurring Friday from creation date
- "saturday" → next occurring Saturday from creation date
- "sunday" → next Sunday from creation date
- "in 3 days" → add 3 days to creation date
- "next week" → add 7 days to creation date



**YEAR BOUNDARY RULES:**
- When calculating future dates near year end, ALWAYS check if the date crosses into the next year
- Use the creation date as the reference point for all relative date calculations
- CRITICAL: NEVER use past dates relative to creation date. If a weekday falls in the past relative to creation date, use NEXT occurrence
- When user says "monday" and creation date is in late December, it MUST be in January of next year
- Always use YYYY-MM-DD format with CORRECT year (check year boundaries!)
- NEVER include comments in JSON (no // or /* */)

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
- When showing task lists or details, include ALL information in the user_message field
- NEVER output text outside the JSON structure - everything must be in user_message
- When listing tasks, format them nicely in the user_message with all details (due date, category, tags, etc.)
- Multiple commands allowed in one response
- Only include fields being changed in update_task data

**EXAMPLES:**

User: "tell me about my tasks"
Response:
{
  "commands": [],
  "user_message": "You have 9 pending tasks. Here's your complete task list:\\n\\n1. **weekly review**\\n   - Due: January 19, 2026\\n   - Category: Personal\\n   - Priority: none\\n   - Tags: #review, #personal\\n\\n2. **pay bills**\\n   - Due: January 1, 2026\\n   - Category: Budget\\n   - Priority: none\\n   - Tags: #payment, #bills\\n\\n3. **meeting with team**\\n   - Due: January 6, 2026\\n   - Category: Work\\n   - Priority: none\\n   - Tags: #work, #meeting\\n\\n4. **yoga class**\\n   - Due: January 4, 2026\\n   - Category: Personal\\n   - Priority: none\\n   - Tags: #fitness, #yoga\\n\\n5. **rent payment**\\n   - Due: January 1, 2026\\n   - Category: Budget\\n   - Priority: none\\n   - Tags: #rent, #payment\\n\\n6. **weekly review**\\n   - Due: January 5, 2026\\n   - Category: Personal\\n   - Priority: none\\n   - Tags: #review, #personal\\n\\n7. **buy groceries**\\n   - Due: January 2, 2026\\n   - Category: Shopping\\n   - Priority: none\\n   - Tags: #shopping, #groceries\\n   - Subtasks: milk, bread, eggs\\n\\n8. **go to gym**\\n   - Due: January 3, 2026\\n   - Category: Personal\\n   - Priority: none\\n   - Tags: #gym, #fitness\\n\\n9. **finish report**\\n   - Due: January 5, 2026\\n   - Category: Work\\n   - Priority: high\\n   - Tags: #work, #deadline",
  "system_note": null
}

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

User: "add a daily standup meeting task every day at 9am"
Response:
{
  "commands": [{
    "action": "create_task",
    "data": {
      "title": "standup meeting",
      "category_name": "Work",
      "due_time": "9:00 AM",
      "recurrence": "daily"
    }
  }],
  "user_message": "Created daily recurring task 'standup meeting' at 9:00 AM. When you complete it, the next occurrence will be automatically created!",
  "system_note": null
}

User: "create weekly review task every monday" → Commands with recurrence:weekly
User: "mark X as done" → update_task with status:completed
User: "delete all completed" → delete_completed_tasks action

**TASK FUNCTIONS:**
- create_task, update_task, delete_task (single)
- complete_all_tasks, mark_all_as_pending
- delete_completed_tasks, delete_pending_tasks, delete_all_tasks
- create_category, update_category, delete_category

**FEATURES:**
Natural dates, auto-category creation, subtasks, priorities (none/low/medium/high), tags, recurring tasks (daily/weekly/monthly/yearly)
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
            elif action == "update_category":
                old_name = data.get("old_name")
                if not old_name:
                    errors.append("old_name is required for update_category")
                    continue

                try:
                    category = Category.objects.get(name=old_name)
                    if "new_name" in data:
                        category.name = data["new_name"]
                    if "color" in data:
                        category.color = data["color"]
                    category.save()
                    results.append(f"Updated category: {old_name}")
                except Category.DoesNotExist:
                    errors.append(f"Category '{old_name}' not found")

            elif action == "delete_category":
                name = data.get("name")
                if not name:
                    errors.append("Category name is required for delete_category")
                    continue

                try:
                    category = Category.objects.get(name=name)
                    # Move all tasks in this category to Inbox
                    inbox, _ = Category.objects.get_or_create(name="Inbox", defaults={'color': '#6b7280'})
                    task_count = Task.objects.filter(category=category).update(category=inbox)
                    category.delete()
                    results.append(f"Deleted category '{name}' and moved {task_count} task(s) to Inbox")
                except Category.DoesNotExist:
                    errors.append(f"Category '{name}' not found")
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

                # Handle recurrence
                recurrence = data.get("recurrence", "none")
                if recurrence in ["daily", "weekly", "monthly", "yearly"]:
                    task.recurrence = recurrence
                    task.is_recurring = True

                # Handle due date
                if "due_date" in data:
                    due_date = parse_date(data["due_date"])
                    if due_date:
                        task.due_date_only = due_date
                elif task.is_recurring:
                    # If recurring but no due_date specified, extract day from description/title
                    # and set it for the current/next month
                    import re
                    text_to_search = f"{title} {data.get('description', '')}"
                    # Look for patterns like "10th", "21st", etc.
                    day_match = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)?\b', text_to_search)
                    if day_match:
                        day = int(day_match.group(1))
                        if 1 <= day <= 31:
                            today = timezone.now().date()
                            # Try to create date with that day in current month
                            try:
                                due_date = date(today.year, today.month, day)
                                # If the date has passed this month, use next month
                                if due_date < today:
                                    if today.month == 12:
                                        due_date = date(today.year + 1, 1, day)
                                    else:
                                        due_date = date(today.year, today.month + 1, day)
                                task.due_date_only = due_date
                            except ValueError:
                                # Invalid date (e.g., Feb 30), skip
                                pass

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
                    old_status = task.status
                    task.status = data["status"]
                    # Handle recurring task status changes
                    if task.is_recurring:
                        if old_status == "pending" and task.status == "completed":
                            task.save()  # Save first to ensure current task is updated
                            task.create_next_occurrence()
                        elif old_status == "completed" and task.status == "pending":
                            task.save()  # Save first
                            task.delete_next_occurrence()
                if "priority" in data:
                    task.priority = data["priority"]
                if "recurrence" in data:
                    recurrence = data["recurrence"]
                    task.recurrence = recurrence
                    task.is_recurring = recurrence != "none"
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

            elif action == "delete_completed_tasks":
                count, _ = Task.objects.filter(status='completed').delete()
                results.append(f"Deleted {count} completed task(s)")

            elif action == "delete_pending_tasks":
                count, _ = Task.objects.filter(status='pending').delete()
                results.append(f"Deleted {count} pending task(s)")

            elif action == "complete_all_tasks":
                updated = Task.objects.filter(status='pending').update(status='completed')
                results.append(f"Marked {updated} task(s) as completed")

            elif action == "mark_all_as_pending":
                updated = Task.objects.filter(status='completed').update(status='pending')
                results.append(f"Marked {updated} task(s) as pending")

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

    # Limit tasks to save tokens - show max 15 pending and 5 completed
    if len(pending_tasks) > 15:
        pending_tasks = pending_tasks[:15]
        pending_note = f" (showing first 15 of {len([t for t in current_tasks if t['status'] == 'pending'])})"
    else:
        pending_note = ""

    if len(completed_tasks) > 5:
        completed_tasks = completed_tasks[:5]
        completed_note = f" (showing last 5 of {len([t for t in current_tasks if t['status'] == 'completed'])})"
    else:
        completed_note = ""

    context_data = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "categories": categories_list
    }

    tasks_context = f"""

CURRENT TASKS IN DATABASE:
Pending Tasks{pending_note}: {json.dumps(pending_tasks, indent=2)}
Completed Tasks{completed_note}: {json.dumps(completed_tasks, indent=2)}

AVAILABLE CATEGORIES:
{json.dumps(categories_list, indent=2)}

IMPORTANT: When user asks about completed tasks, use the Completed Tasks list above. When they ask about pending/active tasks, use the Pending Tasks list."""

    system_message = SYSTEM_INSTRUCTION + tasks_context

    # 5. Get last 1 conversation pair for context (last 1 user + last 1 assistant message)
    recent_messages = ChatMessage.objects.order_by('-timestamp')[:2]  # Get last 2 messages
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
            temperature=0.7,
            response_format={"type": "json_object"}  # Force JSON mode
        )

        ai_response_text = response.choices[0].message.content

        # ALWAYS log full AI response for troubleshooting
        print(f"\n{'='*80}")
        print(f"[TODO APP - AI FULL RESPONSE]")
        print(f"{'='*80}")
        print(ai_response_text)
        print(f"{'='*80}\n")

        # Parse JSON response
        try:
            # Remove markdown code blocks if present
            if '```json' in ai_response_text:
                ai_response_text = ai_response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response_text:
                ai_response_text = ai_response_text.split('```')[1].split('```')[0].strip()

            # Remove any comments from JSON (AI sometimes adds them despite instructions)
            clean_json = '\n'.join(line.split('//')[0] for line in ai_response_text.split('\n'))

            # Try to extract JSON from the response if it's mixed with other text
            import re
            json_match = re.search(r'\{.*\}', clean_json, re.DOTALL)
            if json_match:
                clean_json = json_match.group(0)
            else:
                # No JSON found - AI returned plain text, wrap it
                print(f"[TODO APP WARNING] AI returned plain text instead of JSON. Wrapping response.")
                response_data = {
                    "commands": [],
                    "user_message": ai_response_text,
                    "system_note": "AI returned non-JSON response"
                }
                # Save and return the plain text
                ChatMessage.objects.create(role='model', content=ai_response_text)
                return ai_response_text

            response_data = json.loads(clean_json)

            # If there's text after the JSON, append it to user_message
            remaining_text = ai_response_text[ai_response_text.rfind('}')+1:].strip()
            if remaining_text and response_data.get("user_message"):
                response_data["user_message"] = response_data["user_message"] + "\n\n" + remaining_text
            elif remaining_text and not response_data.get("user_message"):
                response_data["user_message"] = remaining_text

        except json.JSONDecodeError as e:
            # If AI didn't return valid JSON, wrap it and inform user
            print(f"[TODO APP ERROR] JSON Parse Error: {str(e)}")
            print(f"[TODO APP ERROR] Failed to parse JSON. Using plain text as response.")

            # Just return the AI's text as-is since it might still be useful
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
        error_msg = f"Error communicating with AI service: {str(e)}"
        print(f"\n[TODO APP ERROR] {error_msg}")

        # Never reveal technical details to user - just show friendly error
        friendly_msg = "I'm having trouble processing that right now. Please try again in a moment."

        ChatMessage.objects.create(role='model', content=friendly_msg)
        return friendly_msg

