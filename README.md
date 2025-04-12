# Canvas LMS MCP Server

A minimal Canvas LMS MCP server for easy access to education data.

## Features

- List planner items (assignments, quizzes, etc.)
- Get and list assignments
- Get and list quizzes
- Get and list courses
- Get course syllabus
- Get course modules
- List files

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -e .
```

## Configuration

Set your Canvas API token as an environment variable:
```bash
export CANVAS_API_TOKEN="your_api_token_here"
```

## Running the Server

Start the server with:
```bash
uvicorn canvas_lms_mcp.main:app --reload
```

The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Planner
- `GET /planner/items` - List planner items

### Assignments
- `GET /courses/{course_id}/assignments` - List assignments for a course
- `GET /courses/{course_id}/assignments/{assignment_id}` - Get a specific assignment

### Quizzes
- `GET /courses/{course_id}/quizzes` - List quizzes for a course
- `GET /courses/{course_id}/quizzes/{quiz_id}` - Get a specific quiz

### Courses
- `GET /courses` - List courses
- `GET /courses/{course_id}` - Get a specific course
- `GET /courses/{course_id}/syllabus` - Get course syllabus
- `GET /courses/{course_id}/modules` - Get course modules

### Files
- `GET /files` - List files (optionally filtered by course or folder)
