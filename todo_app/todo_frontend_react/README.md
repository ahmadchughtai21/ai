# AI Todo App - React Frontend

A modern React frontend for the AI-powered TickTick-style Todo application.

## Features

- 🎨 Modern UI with Dark/Light theme support
- 🤖 AI Chat Assistant for task management
- 📋 Smart task filtering (All, Inbox, Today, Next 7 Days)
- 🏷️ Category and tag-based organization
- 🔍 Real-time task search
- ✅ Subtask management
- 📊 Task statistics and counts

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Django backend server running on `http://localhost:8000`

## Installation

1. Navigate to the React frontend directory:
```bash
cd todo_frontend_react
```

2. Install dependencies (already done):
```bash
npm install
```

## Running the Application

1. Make sure the Django backend is running:
```bash
# From the root directory
python manage.py runserver
```

2. Start the React development server:
```bash
npm start
```

The app will open automatically at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite
- `npm eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
todo_frontend_react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.js          # Top navigation bar
│   │   ├── Sidebar.js         # Left sidebar with filters
│   │   ├── ChatPane.js        # AI chat interface
│   │   ├── TaskListPane.js    # Task list display
│   │   └── DetailPane.js      # Task detail view
│   ├── context/
│   │   └── ThemeContext.js    # Theme management
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── styles/
│   │   └── App.css            # Main stylesheet
│   ├── App.js                 # Main app component
│   └── index.js               # Entry point
├── package.json
└── README.md
```

## API Integration

The frontend communicates with the Django backend through REST API endpoints:

- **Tasks**: CRUD operations, filtering, search
- **Categories**: List and filter tasks by category
- **Tags**: Tag-based filtering
- **Chat**: AI assistant for natural language task management
- **Subtasks**: Subtask management and toggling

All API calls are proxied through `http://localhost:8000` (configured in package.json).

## Theme Support

The app supports both light and dark themes:
- Toggle using the "🌓 Toggle Theme" button in the navbar
- Theme preference is saved to localStorage
- CSS variables ensure consistent theming across all components

## Components Overview

### Navbar
Top navigation bar with app title and theme toggle button.

### Sidebar
- Search functionality
- Smart views (All, Inbox, Today, Next 7 Days)
- Category list with task counts
- Tag list with task counts

### ChatPane
- AI assistant chat interface
- Send natural language commands to manage tasks
- Chat history persistence
- Clear chat functionality

### TaskListPane
- Displays tasks grouped by due date (Overdue, Today, Tomorrow, Later)
- Completed tasks section (collapsible)
- Task checkboxes for status toggle
- Visual indicators for priority, tags, categories

### DetailPane
- Full task details view
- Task information (status, priority, category, due date)
- Subtask management with toggle completion
- Delete task functionality

## State Management

The app uses React hooks for state management:
- `useState` for component-level state
- `useEffect` for side effects and data loading
- `useContext` for global theme state

## Styling

CSS is organized with:
- CSS variables for theming
- Grid layout for responsive design
- Component-specific styles in App.css
- Dark/light theme support via `data-theme` attribute

## Future Enhancements

- [ ] Add task creation/editing forms
- [ ] Implement drag-and-drop task reordering
- [ ] Add task filtering by multiple tags
- [ ] Implement task due date calendar view
- [ ] Add keyboard shortcuts
- [ ] Implement offline support with service workers

## Troubleshooting

**Issue**: API calls fail with CORS errors
- **Solution**: Ensure Django backend has CORS configured properly

**Issue**: Theme doesn't persist
- **Solution**: Check browser localStorage support

**Issue**: Tasks don't update after AI chat
- **Solution**: Verify backend is running and API endpoints are accessible

## License

This project is part of the AI Todo App system.
