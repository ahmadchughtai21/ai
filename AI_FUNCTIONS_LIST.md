# AI Manager - Complete Functions List

## 📋 TASK CREATION & EDITING

### 1. **create_task**
Create new tasks with full details
- **Examples:**
  - "Add task to buy groceries tomorrow"
  - "Create high priority task: finish report, due Monday at 5pm"
  - "Make shopping list with milk, bread, eggs"
  - "Remind me to go to gym tomorrow at 8pm"

- **Properties you can set:**
  - Title (required)
  - Description
  - Category (Work, Personal, Shopping, etc.)
  - Priority (none, low, medium, high)
  - Due date (today, tomorrow, next monday, 2026-01-15)
  - Due time (8:00 PM, 9:30 AM)
  - Tags (#important, #urgent)
  - Subtasks (checklist items)

### 2. **update_task**
Modify existing task properties
- **Examples:**
  - "Mark 'finish report' as done"
  - "Change due date of grocery shopping to Friday"
  - "Set priority of gym task to high"
  - "Update description of vacation task"

---

## 🗑️ TASK DELETION

### 3. **delete_task**
Remove a specific task by name
- **Examples:**
  - "Delete the grocery task"
  - "Remove 'buy milk' task"

### 4. **delete_completed_tasks**
Clear all finished tasks (keeps pending safe)
- **Examples:**
  - "Delete all completed tasks"
  - "Clear completed tasks"
  - "Clean up finished tasks"

### 5. **delete_pending_tasks**
Remove all unfinished tasks (use carefully!)
- **Examples:**
  - "Delete all pending tasks"
  - "Remove all unfinished tasks"

### 6. **delete_all_tasks**
Delete everything (rarely needed)
- **Examples:**
  - "Delete all tasks"
  - "Clear everything"

---

## ✅ TASK STATUS MANAGEMENT

### 7. **complete_all_tasks**
Mark all pending tasks as done
- **Examples:**
  - "Mark all tasks as completed"
  - "Complete all tasks"
  - "Set all to done"

### 8. **mark_all_as_pending**
Revert all completed tasks back to pending
- **Examples:**
  - "Mark all as pending"
  - "Undo complete all"
  - "Set all back to pending"

---

## 📁 ORGANIZATION

### 9. **create_category**
Make new categories/lists with custom colors
- **Examples:**
  - "Create Work category"
  - "Add new category called Budget"

---

## 🔍 VIEWING & SEARCHING

### Built-in Search (No command needed)
Search automatically by title, description, or tags
- **Examples:**
  - "Find tasks about vacation"
  - "Search for grocery"
  - Type in search bar: "vacation"

### Filter Views
- **All**: See everything (pending + completed)
- **Inbox**: Default category tasks
- **Today**: Due today
- **Next 7 Days**: Due this week
- **By Category**: Click any category in sidebar
- **By Tag**: Click any tag in sidebar

---

## 💬 QUESTIONS YOU CAN ASK

### Task Information
- "What tasks do I have?"
- "Show my tasks"
- "What's pending?"
- "What's completed?"
- "List all my tasks"

### Statistics
- "How many tasks done?"
- "How many pending tasks?"
- "Task statistics"

### Specific Details
- "Tell me about [task name]" - AI checks title AND description
- "Who am I going with on vacation?" - Searches descriptions automatically
- "What's the status of [task]?"

---

## ⚡ SMART FEATURES

### Natural Date Parsing
- **Today**: "add task for today"
- **Tomorrow**: "remind me tomorrow"
- **Weekdays**: "monday", "next thursday"
- **Relative**: "in 3 days", "next week"
- **Specific**: "2026-01-15", "Jan 5th"

### Time Recognition
- 12-hour format: "8:00 PM", "9:30 AM"
- Natural: "8pm tonight", "tomorrow at 5pm"

### Automatic Features
- ✅ Categories auto-created if they don't exist
- ✅ Subtasks with checkboxes
- ✅ Priority badges (high, medium, low)
- ✅ Tag support with # prefix
- ✅ Due date highlighting (overdue in red)

---

## 📝 EXAMPLE CONVERSATIONS

**Create with subtasks:**
> "I have to buy grocery tomorrow make a list in it for tape, scissors, eggs, milk, gloves"
- Creates "buy grocery" task
- Due tomorrow
- With 5 subtasks as checklist

**Ask about details:**
> "Who am I going with on vacation?"
- AI checks task descriptions automatically
- Finds "vacation" task
- Tells you details from description

**Bulk operations:**
> "Mark all tasks as completed"
- Completes all pending tasks at once

> "Delete all completed tasks"
- Removes only finished tasks
- Keeps pending tasks safe

**Smart dates:**
> "Remind me to call mom next Monday at 2pm"
- Calculates next Monday (2026-01-05)
- Sets time to 2:00 PM
- Creates task

---

## 🎯 TIPS

1. **Be natural** - Talk like you normally would
2. **Include details** - More info = better organization
3. **Use descriptions** - AI reads them when answering questions
4. **Tags help** - Use #urgent, #important for quick filtering
5. **Categories organize** - Group related tasks together
6. **Subtasks break down** - Big tasks into smaller steps

---

## 🔒 PRIVACY

- ❌ AI will NEVER mention "Groq" or technical details
- ✅ All your data stays in your local database
- ✅ Friendly, helpful assistant personality
- ✅ Focused on task management only
