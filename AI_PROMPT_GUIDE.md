# 🤖 AI Assistant - Complete Prompt Guide

## System Instructions Summary

The AI assistant is configured with comprehensive instructions in `groq_service.py`. This guide explains how to use and customize it.

---

## 🎯 Core Capabilities

### 1. Task Creation

**Basic Task**
```
User: "add buy milk"
Response: Creates task with title "buy milk" in Inbox
```

**Task with Category**
```
User: "create task to prepare presentation in Work category"
Response: Creates task in Work (auto-creates category if needed)
```

**Task with Priority**
```
User: "add high priority task to finish report"
Response: Creates task with priority set to "high"

Priority Mapping:
- "important", "urgent", "critical" → high
- "normal" → medium
- "someday", "maybe" → low
- Default → none
```

**Task with Due Date**
```
User: "add task to call client due tomorrow"
Response: Sets due_date_only to tomorrow's date

Smart Date Parsing:
- "today" → Current date
- "tomorrow" → Next day
- "next monday" → Calculated date
- "in 3 days" → Current date + 3
- "2025-01-15" → Explicit date
```

**Task with Due Time**
```
User: "add meeting due tomorrow at 3pm"
Response: Sets due_date_only and due_time

Time Format:
- Input: "3pm", "3:30 PM", "15:00"
- Stored: "3:00 PM" (12-hour format)
```

**Task with Subtasks**
```
User: "create grocery list with milk, bread, eggs"
Response: Creates task with 3 subtasks

Triggers:
- "with [items]"
- "including [items]"
- "checklist: [items]"
```

**Task with Tags**
```
User: "add task to review code with tags urgent, backend"
Response: Creates/uses tags "urgent" and "backend"
```

**Complex Task (All Features)**
```
User: "add high priority task to prepare presentation in Work category due tomorrow at 2pm with steps: research, create slides, practice"

Response: Creates task with:
- Title: "prepare presentation"
- Category: Work
- Priority: high
- Due Date: Tomorrow
- Due Time: 2:00 PM
- Subtasks: ["research", "create slides", "practice"]
```

---

### 2. Task Updates

**Mark as Complete**
```
User: "mark buy milk as done"
Response: Updates status to "completed"

Triggers:
- "mark [task] as done"
- "complete [task]"
- "finish [task]"
- "set [task] to done"
```

**Change Priority**
```
User: "set finish report priority to high"
Response: Updates priority field
```

**Update Due Date**
```
User: "change buy milk due date to next friday"
Response: Updates due_date_only
```

**Move to Category**
```
User: "move buy milk to Shopping category"
Response: Updates category (creates if needed)
```

**Add Tags**
```
User: "tag finish report with urgent"
Response: Adds "urgent" tag
```

**Reopen Task**
```
User: "reopen buy milk" or "mark buy milk as pending"
Response: Sets status back to "pending"
```

---

### 3. Task Deletion

**Delete Single Task**
```
User: "delete buy milk"
Response: Removes task by matching title
```

**Delete All Tasks**
```
User: "delete all tasks" or "clear all tasks"
Response: Removes all tasks (use with caution!)
```

---

### 4. Category Management

**Create Category**
```
User: "create Work category"
Response: Creates category with default blue color

User: "create Work category with red color"
Response: Creates category with color #ef4444
```

**Auto-Creation**
Categories are automatically created when mentioned in task creation:
```
User: "add task in Marketing category"
Response: Creates "Marketing" category if it doesn't exist
```

---

### 5. Task Queries

**List All Tasks**
```
User: "what tasks do I have?" or "show my tasks"
Response: Lists all pending tasks
```

**Count Tasks**
```
User: "how many tasks do I have?"
Response: Returns count of tasks
```

**Filter by Category**
```
User: "show my Work tasks"
Response: Lists tasks in Work category
```

**Check Specific Task**
```
User: "do I have a task about groceries?"
Response: Searches and reports
```

---

## 🚫 Scope Restrictions

The AI **WILL REJECT** non-task-related requests:

**Examples of Rejected Queries:**
```
❌ "how to make biryani?"
❌ "what's the weather?"
❌ "help me with coding"
❌ "tell me a joke"
❌ "translate this to Spanish"

Response: "Sorry, I can't help with that. I'm a todo list assistant..."
```

**Only Task-Related Requests Allowed:**
```
✅ "add task to learn Python"
✅ "create reminder for doctor appointment"
✅ "what's on my todo list?"
```

---

## 🔧 Customizing the AI

### Editing System Instructions

Location: `todo_app/groq_service.py` → `SYSTEM_INSTRUCTION`

### Adding New Commands

1. **Define Action in System Prompt**
```python
# Add to SYSTEM_INSTRUCTION
- action: "archive_task" - archive completed task
  task_identifier: exact title of task
```

2. **Implement in execute_commands()**
```python
elif action == "archive_task":
    # Your archiving logic
    task.archived = True
    task.save()
```

3. **Update Examples**
```python
User: "archive buy milk"
Response:
{
  "commands": [{"action": "archive_task", "task_identifier": "buy milk"}],
  "user_message": "Archived task 'buy milk'!",
  "system_note": null
}
```

---

## 📊 JSON Response Format

The AI always responds with this structure:

```json
{
  "commands": [
    {
      "action": "create_task | update_task | delete_task | create_category | null",
      "data": {
        "title": "string",
        "category_name": "string",
        "priority": "none | low | medium | high",
        "due_date": "YYYY-MM-DD",
        "due_time": "HH:MM AM/PM",
        "tags": ["string"],
        "subtasks": ["string"]
      },
      "task_identifier": "string (for update/delete)"
    }
  ],
  "user_message": "Natural language response shown to user",
  "system_note": "Admin/debug note (or null)"
}
```

**Fields:**
- `commands`: Array of actions to execute (can be empty for queries)
- `user_message`: Friendly response displayed in chat
- `system_note`: Optional admin note logged to console

---

## 🧪 Testing the AI

### Test Script Example

```python
from todo_app.groq_service import chat_with_groq

# Test basic task creation
response = chat_with_groq("add buy milk")
print(response)  # "Task 'buy milk' has been added!"

# Test complex task
response = chat_with_groq(
    "create high priority task to prepare slides in Work due tomorrow at 3pm"
)
print(response)  # "Created high priority task..."

# Test rejection
response = chat_with_groq("how to make biryani?")
print(response)  # "Sorry, I can't help with that..."
```

### Manual Testing via UI

1. Open chat pane
2. Try commands from examples above
3. Check task list updates
4. Verify detail pane shows correct data

---

## 🎓 Advanced Features

### Date Parsing Logic

The AI uses `parse_date()` in `groq_service.py`:

```python
# Handled by AI's natural language understanding:
"today" → datetime.now().date()
"tomorrow" → datetime.now().date() + timedelta(days=1)
"next monday" → [calculated]
"in 3 days" → datetime.now().date() + timedelta(days=3)
```

### Time Parsing Logic

```python
def parse_time_to_datetime(time_str):
    # "8:00 PM" → time(20, 0)
    # "9:30 AM" → time(9, 30)
```

### Category Auto-Creation

```python
category_name = data.get("category_name", "Inbox")
category, created = Category.objects.get_or_create(
    name=category_name,
    defaults={'color': '#3b82f6'}
)
```

### Subtask Creation

```python
if "subtasks" in data:
    for idx, subtask_title in enumerate(data["subtasks"]):
        SubTask.objects.create(
            task=task,
            title=subtask_title,
            order=idx
        )
```

---

## 🐛 Debugging

### Enable Verbose Logging

Check terminal output for:
```
[TODO APP] Executed commands: Created task: buy milk (ID: 123)
[TODO APP ERROR] Error executing create_task: ...
[TODO APP NOTE] Some admin note
```

### Common Issues

**1. AI Returns Plain Text Instead of JSON**
- Check if prompt is too complex
- AI might be confused - rephrase the request

**2. Task Not Found for Update/Delete**
- Task identifier must match title exactly (case-insensitive)
- Check for typos in task name

**3. Date Not Parsing**
- AI should format as YYYY-MM-DD
- If not, update SYSTEM_INSTRUCTION examples

**4. Category Not Auto-Creating**
- Check `execute_commands()` logic
- Verify category_name is in data dict

---

## 📝 Best Practices

### Writing AI Prompts

✅ **Good Examples:**
```
"add task to buy groceries"
"create high priority meeting in Work due tomorrow"
"mark buy milk as done"
```

❌ **Avoid:**
```
"can you maybe add a task if possible about groceries?"
→ Too ambiguous

"asdfkljasdf buy milk"
→ Unclear intent
```

### Testing New Features

1. Write example user input
2. Add to SYSTEM_INSTRUCTION examples
3. Test via chat UI
4. Check database to verify changes
5. Review terminal logs

---

## 🔄 Migration from Old to New Format

### Old Format (Before Upgrade)
```
User: "add task buy milk"
Response: Simple task with title only
```

### New Format (After Upgrade)
```
User: "add task buy milk"
Response: Task with optional category, priority, dates, subtasks, tags

User: "add high priority task buy milk in Shopping due tomorrow"
Response: Fully featured task utilizing all new fields
```

**Backward Compatibility:** Old simple commands still work!

---

## 🎉 Summary

The AI assistant is now a powerful TickTick-style task manager that:
- ✅ Creates tasks with categories, priorities, dates, and subtasks
- ✅ Updates and deletes tasks
- ✅ Auto-creates categories
- ✅ Parses natural language dates/times
- ✅ Rejects non-task queries
- ✅ Maintains backward compatibility

Use this guide to understand, test, and customize the AI to your needs!
