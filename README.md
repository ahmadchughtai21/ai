# AI Todo App

AI-powered todo app with a Django REST backend and a React frontend, built around natural-language task management.

## Features

- AI chat commands for task creation, updates, queries, and deletion
- User authentication (signup/login/logout)
- Per-user data isolation for tasks, categories, tags, and chat history
- Categories, priorities, tags, subtasks, due date/time
- Recurring tasks (`daily`, `weekly`, `monthly`, `yearly`)
- Task attachments (file upload/delete)
- Smart views: Inbox, Today, Next 7 Days, search, stats
- 4-pane React UI with light/dark theme

## Tech Stack

- Backend: Django, Django REST Framework, SQLite, Groq API
- Frontend: React 18, Axios, CSS variables

## Project Structure

```text
aitodo/
├── manage.py
├── requirements.txt
├── setup_categories.py
├── ai_todo_project/
├── todo_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── groq_service.py
│   └── todo_frontend_react/   # React frontend used by this project
└── README.md
```

## Setup

### 1. Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key_here
```

Run migrations and seed default categories:

```bash
python manage.py migrate
python setup_categories.py
```

### 2. Frontend

```bash
cd todo_app/todo_frontend_react
npm install
```

## Run

Start backend (terminal 1):

```bash
python manage.py runserver 0.0.0.0:8000
```

Start frontend (terminal 2):

```bash
cd todo_app/todo_frontend_react
node node_modules/react-scripts/bin/react-scripts.js start
```

App URLs:

- Public landing page: http://localhost:8000/
- App (after login): http://localhost:8000/app/
- Login: http://localhost:8000/login/
- Signup: http://localhost:8000/signup/
- Frontend (dev): http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- DRF browser: http://localhost:8000/api/

## API Overview

Base URL: `http://localhost:8000/api/`

### Core resources

- `tasks/` (CRUD)
- `categories/` (CRUD)
- `tags/` (CRUD)
- `subtasks/` (CRUD)
- `attachments/` (CRUD + file upload)

### Task custom endpoints

- `GET /api/tasks/all_pending/`
- `GET /api/tasks/inbox/`
- `GET /api/tasks/today/`
- `GET /api/tasks/next7days/`
- `GET /api/tasks/by_category/?category=Work`
- `GET /api/tasks/by_tag/?tag=urgent`
- `GET /api/tasks/search/?q=report`
- `GET /api/tasks/statistics/`
- `POST /api/tasks/{id}/add_subtask/`

### Other custom endpoints

- `GET /api/tags/pending_tasks_tags/`
- `PATCH /api/subtasks/{id}/toggle_complete/`
- `POST /api/chat/`
- `GET /api/chat/history/`
- `POST /api/chat/clear/`

## Data Model Summary

- `Task`: title, description, status, category, priority, due_date_only, due_time, recurrence, is_recurring, tags, subtasks, attachments
- `Category`: name, color
- `Tag`: name
- `SubTask`: title, is_completed, order, task
- `Attachment`: file, filename, file_size, content_type, task
- `ChatMessage`: role (`user`/`model`), content, timestamp

## AI Command Examples

- `add buy milk`
- `create high priority task to prepare presentation in Work category due tomorrow at 2pm with steps: research, create slides, practice`
- `mark buy milk as done`
- `show me my tasks`
- `create Marketing category with green color`

The assistant is restricted to task-management operations.

## Troubleshooting

- Backend not reachable: ensure `python manage.py runserver` is running on port `8000`
- Frontend not reachable: run frontend from `todo_app/todo_frontend_react`
- AI chat fails: verify `GROQ_API_KEY` is set correctly in `.env`
- React frontend also provides `/`, `/login`, `/signup`, and `/app` routes with auth-gated workspace access.

## Screenshots

<img width="1326" height="702" alt="1" src="https://github.com/user-attachments/assets/afccaa4e-9693-4e81-aa8d-f250c6f32411" />
<img width="1326" height="702" alt="2" src="https://github.com/user-attachments/assets/50a221d3-a98a-443f-bce0-986651dcdc6d" />
<img width="1326" height="702" alt="3" src="https://github.com/user-attachments/assets/308ab077-5237-44e9-918b-ca5619b9bf24" />
<img width="1326" height="702" alt="4" src="https://github.com/user-attachments/assets/e3f08669-3263-4a69-b87b-dd9e6a8fbd08" />
<img width="1280" height="2186" alt="5" src="https://github.com/user-attachments/assets/fd11adfe-25af-48d9-8da6-4ad7ecf8174d" />
<img width="1326" height="702" alt="6" src="https://github.com/user-attachments/assets/f3412fce-cd10-467e-bad1-cfd708d8a7f4" />


