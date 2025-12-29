# Quick Start Guide - React Frontend

## 🚀 Start the Application

### Step 1: Start Django Backend
```bash
# In terminal 1 (from project root)
python manage.py runserver
```
✅ Backend running at: http://localhost:8000

### Step 2: Start React Frontend
```bash
# In terminal 2
cd todo_frontend_react
./start.sh
```
✅ Frontend running at: http://localhost:3000

## 📂 Project Files

### React Frontend Location
```
/home/ahmad/repos/aitodo/todo_frontend_react/
```

### Key Files You Might Edit
- `src/App.js` - Main application logic
- `src/components/*.js` - Individual UI components
- `src/styles/App.css` - Styling
- `src/services/api.js` - API endpoints

## 🎨 Features Available

### Left Sidebar
- 🔍 Search tasks
- 📋 All tasks
- 📥 Inbox (tasks without category)
- 📅 Today's tasks
- 🗓️ Next 7 days tasks
- 🏷️ Categories (click to filter)
- #️⃣ Tags (click to filter)

### AI Chat (Second Column)
- Type natural language commands
- Examples:
  - "Create a task to buy groceries tomorrow"
  - "Add high priority task for meeting at 2pm"
  - "Show me all work tasks"

### Task List (Third Column)
- Click checkbox to complete/uncomplete task
- Click task to view details
- Grouped by: Overdue, Today, Tomorrow, Later
- Completed tasks section (collapsible)

### Task Details (Right Column)
- View all task information
- Toggle subtasks
- Delete task

### Top Bar
- 🌓 Toggle between dark/light theme

## 🛠️ Troubleshooting

### React app won't start
```bash
cd todo_frontend_react
rm -rf node_modules package-lock.json
npm install
./start.sh
```

### Backend not connecting
- Ensure Django is running on port 8000
- Check: http://localhost:8000/api/tasks/

### Theme not working
- Clear browser cache
- Check browser console for errors

## 📱 Browser Access

Open in your browser:
- **React App**: http://localhost:3000
- **Django API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 🎯 Common Tasks

### View API Documentation
```
/home/ahmad/repos/aitodo/todo_frontend/API_DOCUMENTATION.md
```

### View Full Guide
```
/home/ahmad/repos/aitodo/REACT_FRONTEND_GUIDE.md
```

### Implementation Details
```
/home/ahmad/repos/aitodo/todo_frontend_react/IMPLEMENTATION_SUMMARY.md
```

## 💡 Tips

1. **Both servers must be running** - Django (port 8000) and React (port 3000)
2. **Auto-reload enabled** - Changes to code automatically refresh
3. **Theme persists** - Your theme choice is saved in browser
4. **API is proxied** - React automatically forwards API calls to Django

## ✅ Verification

Your app is working if you can:
- [x] See the app at http://localhost:3000
- [x] Toggle dark/light theme
- [x] View tasks in the task list
- [x] Click a task and see details on the right
- [x] Chat with AI assistant
- [x] Search for tasks
- [x] Filter by category or tag

## 🆘 Need Help?

Check these files:
1. `REACT_FRONTEND_GUIDE.md` - Complete guide
2. `todo_frontend_react/README.md` - Frontend specific docs
3. `API_DOCUMENTATION.md` - API reference

## 📊 Project Structure at a Glance

```
aitodo/
├── manage.py                      # Django management
├── todo_app/                      # Backend (Django)
├── todo_frontend/                 # Original HTML frontend
└── todo_frontend_react/           # NEW React frontend
    ├── src/
    │   ├── components/            # React components
    │   ├── services/              # API integration
    │   └── styles/                # CSS files
    └── start.sh                   # Easy start script
```

---

**Happy coding! 🎉**
