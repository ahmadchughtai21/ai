# 🎯 TickTick-Style AI Todo List App

A professional, TickTick-inspired productivity application built with Django, featuring an intelligent AI assistant powered by Groq API.

## ✨ Features

### 🤖 **AI-Powered Task Management**
- Natural language task creation with categories, priorities, and due dates
- Smart date parsing ("tomorrow", "next monday", "in 3 days")
- Automatic category creation
- Subtask generation from natural language
- Scope-restricted AI (only handles task-related queries)

### 📊 **Advanced Task Organization**
- **Categories/Lists**: Organize tasks with custom colored categories
- **Priorities**: High, Medium, Low, None
- **Due Dates & Times**: Separate date and time fields
- **Subtasks**: Checklist items within tasks
- **Tags**: Label and categorize tasks
- **Smart Views**: Inbox, Today, Next 7 Days

### 🎨 **Modern TickTick-Style UI**
- **4-Pane Layout**:
  - Left Sidebar: Smart views and categories
  - AI Chat: Intelligent assistant
  - Task List: Organized sections (Overdue, Today, Tomorrow, Later)
  - Detail Pane: Full task information with subtasks
- **Dark/Light Theme Toggle**: Beautiful themes with CSS variables
- **Responsive Design**: Smooth scrolling, hover effects, selection highlights

### 🔌 **Full REST API**
- Complete CRUD operations for tasks, categories, subtasks, tags
- Django REST Framework browsable API
- Extensible for future integrations

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 2. Installation

```bash
# Clone the repository (if applicable)
git clone <your-repo-url>
cd aitodo

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key_here
```

Get your Groq API key from: https://console.groq.com/

### 4. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create default categories
python setup_categories.py

# (Optional) Create admin user
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver 0.0.0.0:8000
```

### 6. Access the App

Open your browser and navigate to:
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Browser**: http://localhost:8000/api/

---

## 📖 Usage Examples

### AI Chat Commands

**Create Simple Task:**
```
"add buy milk"
```

**Create Task with Everything:**
```
"create high priority task to prepare presentation in Work category due tomorrow at 2pm with steps: research, create slides, practice"
```

**Update Task:**
```
"mark buy milk as done"
"set finish report priority to high"
"move buy milk to Shopping category"
```

**Query Tasks:**
```
"show me my tasks"
"what's in my Work category?"
"do I have any tasks due today?"
```

**Create Category:**
```
"create Marketing category with green color"
```

---

## 📚 Documentation

- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete upgrade summary
- **[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)** - Feature overview and examples
- **[AI_PROMPT_GUIDE.md](AI_PROMPT_GUIDE.md)** - AI usage and customization guide

---

## 🏗️ Project Structure

```
aitodo/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── setup_categories.py         # Default category setup
├── ai_todo_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── todo_app/
    ├── models.py               # Category, Task, SubTask, Tag
    ├── serializers.py          # DRF serializers
    ├── views.py                # API viewsets
    ├── urls.py                 # URL routing
    ├── admin.py                # Django admin config
    ├── groq_service.py         # AI integration
    └── templates/todo_app/
        └── index.html          # TickTick-style UI
```

---

## 🎯 Database Schema

### Models

**Category**
- name (CharField, unique)
- color (CharField, hex color)

**Task**
- title (CharField)
- description (TextField)
- category (ForeignKey to Category, nullable)
- priority (CharField: none/low/medium/high)
- due_date_only (DateField, nullable)
- due_time (TimeField, nullable)
- status (CharField: pending/completed)
- tags (ManyToMany with Tag)

**SubTask**
- task (ForeignKey to Task)
- title (CharField)
- is_completed (BooleanField)
- order (IntegerField)

**Tag**
- name (CharField, unique)

---

## 🔌 API Endpoints

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task detail
- `PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/add_subtask/` - Add subtask

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category
- `PATCH /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### SubTasks
- `GET /api/subtasks/` - List subtasks
- `PATCH /api/subtasks/{id}/` - Update subtask
- `DELETE /api/subtasks/{id}/` - Delete subtask

### Tags
- `GET /api/tags/` - List tags
- `POST /api/tags/` - Create tag

### Chat
- `POST /api/chat/` - Send message to AI
- `GET /api/chat/history/` - Get chat history
- `POST /api/chat/clear/` - Clear chat history

---

## 🎨 UI Features

### 4-Pane Layout
1. **Sidebar (250px)**: Smart views + categories with counts
2. **AI Chat (350px)**: Conversational task management
3. **Task List (flexible)**: Sections for Overdue, Today, Tomorrow, Later
4. **Detail Pane (350px)**: Full task details, subtasks, metadata

### Smart Sections
Tasks automatically organize into:
- ⚠️ **Overdue**: Past due date (red)
- 📅 **Today**: Due today
- 📆 **Tomorrow**: Due tomorrow
- 📋 **Later**: Future or no due date

### Theme Toggle
Switch between light and dark modes. Theme preference persists across sessions.

---

## 🧪 Testing

### Manual UI Testing
1. Open http://localhost:8000
2. Try AI commands from examples above
3. Click sidebar items to filter tasks
4. Click tasks to view details
5. Toggle theme in navbar
6. Mark tasks complete via checkbox

### API Testing (cURL)

```bash
# Create task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "category_id": 1,
    "priority": "high",
    "due_date_only": "2025-12-30"
  }'

# List tasks
curl http://localhost:8000/api/tasks/

# Create category
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Testing", "color": "#ff0000"}'
```

---

## 🛠️ Tech Stack

**Backend:**
- Django 6.0
- Django REST Framework
- SQLite
- Groq AI (llama-3.1-8b-instant)

**Frontend:**
- Vanilla JavaScript
- CSS Grid + Flexbox
- CSS Variables for theming
- No framework dependencies

---

## 🔒 Security Notes

- Never commit `.env` file with API keys
- Use environment variables for sensitive data
- Run `DEBUG=False` in production
- Use proper WSGI server (not `runserver`) in production
- Set `ALLOWED_HOSTS` in production

---

## 📝 License

[Your License Here]

---

## 🤝 Contributing

[Your contributing guidelines here]

---

## 📧 Contact

[Your contact information here]

---

## 🙏 Acknowledgments

- Groq for AI capabilities
- TickTick for UI inspiration
- Django community for excellent framework

---

**Enjoy your TickTick-style productivity app! 🎉**
