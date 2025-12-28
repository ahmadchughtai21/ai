# AI Todo List App

This is an AI-powered Todo List application built with Django and Groq API.

## Features
-   **Chat Interface**: Interact with an AI assistant to manage tasks.
-   **Natural Language Processing**: The AI understands natural language to create tasks with dates, descriptions, and tags.
-   **Task Management**: View, manage, and organize tasks.
-   **Tagging**: Automatically categorize tasks.

## Setup

1.  **Clone the repository** (if applicable).
2.  **Create a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    -   Create a `.env` file in the root directory.
    -   Add your Groq API key:
        ```
        GROQ_API_KEY=your_api_key_here
        DEBUG=True
        SECRET_KEY=your_secret_key
        ```
5.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```
7.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

## Usage
-   Type in the chat box on the left to add tasks.
-   Example: "Remind me to buy milk tomorrow at 5pm"
-   The AI will create the task and it will appear on the right.
