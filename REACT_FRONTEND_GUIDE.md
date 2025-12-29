# AI Todo App - Complete Project Guide

## Overview

This project consists of two parts:
1. **Django Backend** - REST API for task management with AI integration
2. **React Frontend** - Modern UI for interacting with the API

## Quick Start

### 1. Start the Django Backend

```bash
# From the root directory
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

### 2. Start the React Frontend

**Option A: Using the start script**
```bash
cd todo_frontend_react
./start.sh
```

**Option B: Using npm directly**
```bash
cd todo_frontend_react
node_modules/.bin/react-scripts start
```

Frontend will be available at: `http://localhost:3000`

## Project Structure

```
aitodo/
├── ai_todo_project/           # Django project settings
├── todo_app/                  # Django app (backend)
│   ├── models.py             # Database models
│   ├── views.py              # API endpoints
│   ├── serializers.py        # Data serialization
│   ├── groq_service.py       # AI integration
│   └── templates/            # Original HTML frontend
├── todo_frontend_react/       # React frontend (NEW)
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # Theme context
│   │   ├── services/         # API service
│   │   └── styles/           # CSS styles
│   ├── package.json
│   ├── start.sh              # Convenient start script
│   └── README.md
├── manage.py
└── requirements.txt
```

## Features Implemented in React Frontend

### ✅ Core Features
- [x] Dark/Light theme toggle with persistence
- [x] AI Chat Assistant for natural language task management
- [x] Task list with status toggling
- [x] Task detail view with full information
- [x] Search functionality
- [x] Category filtering
- [x] Tag filtering
- [x] Smart views (All, Inbox, Today, Next 7 Days)
- [x] Subtask display and toggling
- [x] Task deletion
- [x] Real-time statistics

### 🎨 UI Features
- Modern grid layout (Sidebar | Chat | Tasks | Details)
- Responsive design
- Smooth transitions and hover effects
- Task grouping by due date (Overdue, Today, Tomorrow, Later)
- Collapsible completed tasks section
- Visual priority badges
- Category color indicators
- Tag display

### 🔌 API Integration
All endpoints from the Django backend are integrated:
- Tasks CRUD operations
- Category management
- Tag management
- Subtask operations
- Chat/AI assistant
- Search and filtering

## Environment Setup

### Backend Requirements
```bash
pip install -r requirements.txt
```

Required packages:
- Django
- djangorestframework
- django-cors-headers
- groq (for AI integration)

### Frontend Requirements
```bash
cd todo_frontend_react
npm install
```

Dependencies:
- react (^18.2.0)
- react-dom (^18.2.0)
- react-scripts (5.0.1)
- axios (^1.6.2)

## API Configuration

The React frontend is configured to proxy API requests to the Django backend:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Proxy**: Configured in package.json

All API calls from React (e.g., `/api/tasks/`) are automatically proxied to `http://localhost:8000/api/tasks/`

## Development Workflow

### Making Changes to Backend

1. Edit files in `todo_app/` directory
2. Django auto-reloads on file changes
3. Check console for errors
4. Test endpoints at http://localhost:8000/api/

### Making Changes to Frontend

1. Edit files in `todo_frontend_react/src/`
2. React auto-reloads on file changes
3. Check browser console for errors
4. View changes at http://localhost:3000

## Key Differences: Original HTML vs React Frontend

### Original HTML (todo_frontend/index.html)
- Single HTML file with embedded JavaScript
- Vanilla JavaScript with direct DOM manipulation
- All code in one file
- Manual state management

### React Frontend (todo_frontend_react/)
- Component-based architecture
- Declarative UI updates
- Modular code organization
- React hooks for state management
- Better code reusability and maintainability

## Common Issues and Solutions

### Issue: CORS errors
**Solution**: Ensure `django-cors-headers` is installed and configured in Django settings

### Issue: React app can't connect to backend
**Solution**:
- Verify Django is running on port 8000
- Check proxy configuration in package.json
- Ensure no firewall blocking localhost connections

### Issue: Chat not working
**Solution**:
- Verify GROQ API key is set in Django settings
- Check backend console for AI service errors

### Issue: Theme doesn't persist
**Solution**: Check browser localStorage is enabled

### Issue: npm install fails
**Solution**:
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and package-lock.json
- Run `npm install` again

## Testing

### Backend Testing
```bash
python manage.py test
```

### Frontend Testing
```bash
cd todo_frontend_react
npm test
```

## Building for Production

### Backend
```bash
python manage.py collectstatic
# Configure WSGI server (gunicorn, uwsgi)
```

### Frontend
```bash
cd todo_frontend_react
npm run build
# Serve the build/ directory with any static server
```

## Future Enhancements

### Planned Features
- [ ] Task creation/editing forms in React
- [ ] Drag-and-drop task reordering
- [ ] Calendar view for tasks
- [ ] Recurring tasks
- [ ] Task attachments
- [ ] User authentication
- [ ] Mobile responsive improvements
- [ ] PWA support
- [ ] Offline mode

## Technologies Used

### Backend
- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default, can use PostgreSQL/MySQL)
- GROQ AI API

### Frontend
- React 18
- Axios for HTTP requests
- Context API for state management
- CSS Variables for theming
- Create React App

## Contributing

When contributing:
1. Backend changes go in `todo_app/`
2. React frontend changes go in `todo_frontend_react/src/`
3. Keep the original HTML frontend as reference
4. Test both backends and frontends before committing

## License

This is a sample project for learning purposes.

## Credits

Built with modern web technologies and AI assistance.
