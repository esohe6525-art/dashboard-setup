# Task Tracker API

This is a simple Flask REST API for managing tasks.

## Features

- CRUD endpoints for `Task` resources
- SQLite database with Flask-SQLAlchemy
- Blueprint-based route organization
- JSON request/response handling
- Basic validation and error handling

## Setup

1. Create and activate your virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

The API server listens on `http://127.0.0.1:5000`.

## API Endpoints

- `GET /tasks` - retrieve all tasks
- `GET /tasks/<id>` - retrieve one task
- `POST /tasks` - create a new task
- `PUT /tasks/<id>` - update a task
- `DELETE /tasks/<id>` - delete a task

### Example Requests

Create a task:

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

Update a task:

```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

Delete a task:

```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

## Reflection

This project helped me practice Flask application structure, blueprints, SQLAlchemy models, and RESTful route design. I learned how to separate configuration, initialize extensions cleanly, and build JSON-based API endpoints with validation and error handling.
