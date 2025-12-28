# AI Todo App - REST API Documentation

Complete API documentation for the AI-powered TickTick-style Todo application.

**Base URL:** `http://localhost:8000/api/`

---

## Table of Contents
- [Authentication](#authentication)
- [Tasks Endpoints](#tasks-endpoints)
- [Categories Endpoints](#categories-endpoints)
- [Tags Endpoints](#tags-endpoints)
- [Subtasks Endpoints](#subtasks-endpoints)
- [Chat/AI Endpoints](#chatai-endpoints)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Tasks Endpoints

### 1. List All Tasks
**GET** `/api/tasks/`

Returns all tasks ordered by creation date (newest first).

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project report",
    "description": "Write the final report for Q4",
    "status": "pending",
    "priority": "high",
    "category": 2,
    "category_name": "Work",
    "category_detail": {
      "id": 2,
      "name": "Work",
      "color": "#ef4444"
    },
    "due_date": "2025-12-30T17:00:00Z",
    "due_date_only": "2025-12-30",
    "due_time": "05:00 PM",
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T10:00:00Z",
    "tags": [
      {"id": 1, "name": "urgent"}
    ],
    "subtasks": [
      {
        "id": 1,
        "title": "Research data",
        "is_completed": true,
        "order": 0
      }
    ]
  }
]
```

---

### 2. Get All Pending Tasks
**GET** `/api/tasks/all_pending/`

Returns only tasks with status='pending'.

**Response:** Same as List All Tasks

---

### 3. Get Inbox Tasks
**GET** `/api/tasks/inbox/`

Returns pending tasks that have no category or are in the "Inbox" category.

**Response:** Same as List All Tasks

---

### 4. Get Today's Tasks
**GET** `/api/tasks/today/`

Returns pending tasks due today.

**Response:** Same as List All Tasks

---

### 5. Get Next 7 Days Tasks
**GET** `/api/tasks/next7days/`

Returns pending tasks due in the next 7 days.

**Response:** Same as List All Tasks

---

### 6. Get Tasks by Category
**GET** `/api/tasks/by_category/?category=Work`

Returns tasks filtered by category name.

**Query Parameters:**
- `category` (required): Category name (e.g., "Work", "Personal", "Shopping")

**Response:** Same as List All Tasks

---

### 7. Get Tasks by Tag
**GET** `/api/tasks/by_tag/?tag=urgent`

Returns tasks filtered by tag name.

**Query Parameters:**
- `tag` (required): Tag name (e.g., "urgent", "important")

**Response:** Same as List All Tasks

---

### 8. Search Tasks
**GET** `/api/tasks/search/?q=report`

Search tasks by title or description.

**Query Parameters:**
- `q` (required): Search query string

**Response:** Same as List All Tasks

---

### 9. Get Task Statistics
**GET** `/api/tasks/statistics/`

Returns counts and statistics for tasks.

**Response:**
```json
{
  "total": 25,
  "pending": 15,
  "completed": 10,
  "inbox": 5,
  "today": 3,
  "next_7_days": 8,
  "overdue": 2
}
```

---

### 10. Create Task
**POST** `/api/tasks/`

Create a new task.

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "status": "pending",
  "priority": "medium",
  "category": 3,
  "due_date_only": "2025-12-30",
  "due_time": "06:00 PM"
}
```

**Required Fields:**
- `title` (string)

**Optional Fields:**
- `description` (string)
- `status` (string): "pending" or "completed" (default: "pending")
- `priority` (string): "none", "low", "medium", "high" (default: "none")
- `category` (integer): Category ID
- `due_date_only` (date): "YYYY-MM-DD"
- `due_time` (time): "HH:MM AM/PM"

**Response:** Created task object (201 Created)

---

### 11. Get Single Task
**GET** `/api/tasks/{id}/`

Get details of a specific task.

**Response:** Single task object

---

### 12. Update Task
**PUT/PATCH** `/api/tasks/{id}/`

Update an existing task. Use PATCH for partial updates.

**Request Body:** Same as Create Task (only include fields to update for PATCH)

**Response:** Updated task object

---

### 13. Delete Task
**DELETE** `/api/tasks/{id}/`

Delete a task.

**Response:** 204 No Content

---

### 14. Add Subtask to Task
**POST** `/api/tasks/{id}/add_subtask/`

Add a subtask to a specific task.

**Request Body:**
```json
{
  "title": "Buy milk"
}
```

**Response:**
```json
{
  "id": 5,
  "title": "Buy milk",
  "is_completed": false,
  "order": 0,
  "task": 1
}
```

---

## Categories Endpoints

### 1. List All Categories
**GET** `/api/categories/`

Returns all categories ordered by name.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Work",
    "color": "#ef4444",
    "task_count": 12
  },
  {
    "id": 2,
    "name": "Personal",
    "color": "#10b981",
    "task_count": 5
  }
]
```

---

### 2. Create Category
**POST** `/api/categories/`

Create a new category.

**Request Body:**
```json
{
  "name": "Fitness",
  "color": "#ec4899"
}
```

**Required Fields:**
- `name` (string)

**Optional Fields:**
- `color` (string): Hex color code (default: "#3b82f6")

**Response:** Created category object (201 Created)

---

### 3. Get Single Category
**GET** `/api/categories/{id}/`

**Response:** Single category object

---

### 4. Update Category
**PUT/PATCH** `/api/categories/{id}/`

**Request Body:** Same as Create Category

**Response:** Updated category object

---

### 5. Delete Category
**DELETE** `/api/categories/{id}/`

**Response:** 204 No Content

---

## Tags Endpoints

### 1. List All Tags
**GET** `/api/tags/`

Returns all tags.

**Response:**
```json
[
  {
    "id": 1,
    "name": "urgent"
  },
  {
    "id": 2,
    "name": "important"
  }
]
```

---

### 2. Get Tags from Pending Tasks
**GET** `/api/tags/pending_tasks_tags/`

Returns only tags used in pending tasks with task counts.

**Response:**
```json
[
  {
    "id": 1,
    "name": "urgent",
    "task_count": 5
  },
  {
    "id": 2,
    "name": "important",
    "task_count": 3
  }
]
```

---

### 3. Create Tag
**POST** `/api/tags/`

**Request Body:**
```json
{
  "name": "priority"
}
```

**Response:** Created tag object (201 Created)

---

### 4. Update/Delete Tag
Standard REST operations available at `/api/tags/{id}/`

---

## Subtasks Endpoints

### 1. List All Subtasks
**GET** `/api/subtasks/`

Returns all subtasks.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Research data",
    "is_completed": true,
    "order": 0,
    "task": 5
  }
]
```

---

### 2. Create Subtask
**POST** `/api/subtasks/`

**Request Body:**
```json
{
  "task": 5,
  "title": "Review findings",
  "is_completed": false,
  "order": 1
}
```

**Required Fields:**
- `task` (integer): Task ID
- `title` (string)

**Response:** Created subtask object (201 Created)

---

### 3. Toggle Subtask Completion
**PATCH** `/api/subtasks/{id}/toggle_complete/`

Toggles the completion status of a subtask.

**Response:** Updated subtask object

---

### 4. Update Subtask
**PUT/PATCH** `/api/subtasks/{id}/`

**Request Body:**
```json
{
  "title": "Updated title",
  "is_completed": true
}
```

**Response:** Updated subtask object

---

### 5. Delete Subtask
**DELETE** `/api/subtasks/{id}/`

**Response:** 204 No Content

---

## Chat/AI Endpoints

### 1. Send Message to AI
**POST** `/api/chat/`

Send a message to the AI assistant to manage tasks.

**Request Body:**
```json
{
  "message": "Create a high priority task to finish the report due tomorrow at 5pm in Work category"
}
```

**Response:**
```json
{
  "response": "Created high priority task 'finish the report' in Work category, due tomorrow at 5:00 PM!"
}
```

---

### 2. Get Chat History
**GET** `/api/chat/history/`

Returns all chat messages ordered by timestamp.

**Response:**
```json
[
  {
    "id": 1,
    "role": "user",
    "content": "Create a task to buy groceries",
    "timestamp": "2025-12-28T10:00:00Z"
  },
  {
    "id": 2,
    "role": "model",
    "content": "Created task 'buy groceries' in Inbox!",
    "timestamp": "2025-12-28T10:00:01Z"
  }
]
```

---

### 3. Clear Chat History
**POST** `/api/chat/clear/`

Deletes all chat messages.

**Response:**
```json
{
  "status": "success",
  "message": "Chat history cleared"
}
```

---

## Response Formats

### Success Responses

**List/Retrieve:**
- Status Code: 200 OK
- Body: Object or array of objects

**Create:**
- Status Code: 201 Created
- Body: Created object

**Update:**
- Status Code: 200 OK
- Body: Updated object

**Delete:**
- Status Code: 204 No Content
- Body: Empty

---

## Error Handling

### Error Response Format
```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Status Codes

- **400 Bad Request**: Invalid request data or missing required fields
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side error

### Example Errors

**Missing Required Field:**
```json
{
  "error": "Title is required"
}
```

**Invalid Query Parameter:**
```json
{
  "error": "category parameter is required"
}
```

**AI Error:**
```json
{
  "error": "Error communicating with Groq: Connection timeout"
}
```

---

## Usage Examples

### Create a Task with All Features

**Request:**
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete quarterly review",
    "description": "Prepare and submit Q4 review document",
    "priority": "high",
    "category": 2,
    "due_date_only": "2025-12-31",
    "due_time": "05:00 PM",
    "status": "pending"
  }'
```

---

### Search Tasks

**Request:**
```bash
curl -X GET "http://localhost:8000/api/tasks/search/?q=review"
```

---

### Get Statistics

**Request:**
```bash
curl -X GET http://localhost:8000/api/tasks/statistics/
```

---

### Use AI to Create Task

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "add task to call mom tomorrow at 6pm high priority"
  }'
```

---

## Notes

1. **Date Format:** All dates use ISO 8601 format (YYYY-MM-DD)
2. **Time Format:** Times use 12-hour format with AM/PM (e.g., "05:00 PM")
3. **Priority Values:** "none", "low", "medium", "high"
4. **Status Values:** "pending", "completed"
5. **Colors:** Hex color codes (e.g., "#3b82f6")

---

## Integration Tips

### React/Vue/Angular Frontend

```javascript
// Fetch all pending tasks
const response = await fetch('http://localhost:8000/api/tasks/all_pending/');
const tasks = await response.json();

// Create a task
await fetch('http://localhost:8000/api/tasks/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'New task',
    priority: 'high'
  })
});

// Get statistics
const stats = await fetch('http://localhost:8000/api/tasks/statistics/')
  .then(r => r.json());
```

### Mobile App (Flutter/React Native)

```dart
// Flutter example
Future<List<Task>> getTodayTasks() async {
  final response = await http.get(
    Uri.parse('http://localhost:8000/api/tasks/today/')
  );
  if (response.statusCode == 200) {
    return parseTaskList(json.decode(response.body));
  }
  throw Exception('Failed to load tasks');
}
```

---

## API Changelog

### Version 1.0 (Current)
- Initial API release
- Full CRUD for tasks, categories, tags, subtasks
- AI chat integration
- Advanced filtering (by category, tag, date)
- Search functionality
- Statistics endpoint
- Subtask toggle completion
