# Canvas LMS MCP Server

[![smithery badge](https://smithery.ai/badge/@ahnopologetic/canvas-lms-mcp)](https://smithery.ai/server/@ahnopologetic/canvas-lms-mcp)
A minimal Canvas LMS MCP (Machine Conversation Protocol) server for easy access to education data through your Canvas LMS instance. This server provides a bridge between AI systems (like Cursor) and Canvas Learning Management System.

## Features

- List planner items (assignments, quizzes, etc.)
- Get and list assignments
- Get and list quizzes
- Get and list courses
- Get course syllabus
- Get course modules
- List files

## Installation

### Installing via Smithery

To install Canvas LMS Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@ahnopologetic/canvas-lms-mcp):

```bash
npx -y @smithery/cli install @ahnopologetic/canvas-lms-mcp --client claude
```

### Prerequisites

- Python 3.13+
- Canvas LMS API token
- `uv` package manager (recommended)

### Installation Methods

#### Option 1: Install with uvx (Recommended)

The easiest way to install and run canvas-lms-mcp is using uvx:

```bash
uvx canvas-lms-mcp
```

This will run the server in an isolated environment without installing it permanently.

To install the tool permanently:

```bash
uv tool install canvas-lms-mcp
```

#### Option 2: Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/canvas-lms-mcp.git
   cd canvas-lms-mcp
   ```

2. Install with uv:
   ```bash
   # Install uv if you don't have it yet
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create a virtual environment and install dependencies
   uv venv
   uv pip install -e .
   ```

   Alternatively, use traditional methods:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

## Configuration

Set the following environment variables:

```bash
export CANVAS_API_TOKEN="your_canvas_api_token"
export CANVAS_BASE_URL="https://your-institution.instructure.com"  # Default: https://canvas.instructure.com
```

You can get your Canvas API token from your Canvas account settings.

## Running the Server

Start the server with uv:

```bash
uv run src/canvas_lms_mcp/main.py
```

If installed with uvx tool:
```bash
canvas-lms-mcp
```

By default, the server runs on http://localhost:8000. You can use the FastMCP interface at http://localhost:8000/docs to interact with the API.

## Available Tools

The server provides the following tools for interacting with Canvas LMS:

### Courses

#### `list_courses`
List courses that the user is actively enrolled in.

Parameters:
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_course`
Get a single course by ID.

Parameters:
- `course_id` (required): Course ID
- `include` (optional): List of additional data to include

#### `get_course_syllabus`
Get a course's syllabus.

Parameters:
- `course_id` (required): Course ID

#### `get_course_modules`
Get modules for a course.

Parameters:
- `course_id` (required): Course ID
- `include` (optional): List of additional data to include

### Assignments

#### `list_assignments`
List assignments for a course.

Parameters:
- `course_id` (required): Course ID
- `bucket` (required): Filter assignments by ("past", "overdue", "undated", "ungraded", "unsubmitted", "upcoming", "future")
- `order_by` (required): Field to order assignments by ("due_at", "position", "name")
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_assignment`
Get a single assignment by ID.

Parameters:
- `course_id` (required): Course ID
- `assignment_id` (required): Assignment ID

### Quizzes

#### `list_quizzes`
List quizzes for a course.

Parameters:
- `course_id` (required): Course ID
- `include` (optional): List of additional data to include
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_quiz`
Get a single quiz by ID.

Parameters:
- `course_id` (required): Course ID
- `quiz_id` (required): Quiz ID

### Files

#### `list_files`
List files for a course or folder.

Parameters:
- `course_id` (optional): Course ID
- `folder_id` (optional): Folder ID
- `include` (optional): List of additional data to include
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

### Planner Items

#### `list_planner_items`
List planner items for the authenticated user.

Parameters:
- `start_date` (required): Start date in ISO 8601 format
- `end_date` (required): End date in ISO 8601 format
- `context_codes` (optional): List of context codes (e.g., ["course_123"])
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

## Integration with Cursor

Cursor is an AI-powered IDE that can interact with the Canvas LMS MCP server to provide education data directly within your development environment.

### Setting Up Cursor Integration

1. Install the Cursor IDE from [https://cursor.sh/](https://cursor.sh/)

2. Create a `.cursor/mcp.json` file in your project directory with the following content:
   ```json
   {
       "mcpServers": {
           "canvas": {
               "command": "uvx",
               "args": [
                    "canvas-lms-mcp"
               ],
               "env": {
                   "CANVAS_API_TOKEN": "your_canvas_api_token",
                   "CANVAS_BASE_URL": "https://your-institution.instructure.com"
               }
           }
       }
   }
   ```

   Replace:
   - `your_canvas_api_token` with your actual Canvas API token
   - `your-institution.instructure.com` with your Canvas institution URL

3. Restart Cursor for the changes to take effect.

### Cursor Time Integration (Optional)

You can also integrate a time server for timezone-related queries by adding a "time" server to your mcp.json:

```json
"time": {
    "command": "uvx",
    "args": [
        "mcp-server-time",
        "--local-timezone=America/New_York"
    ]
}
```

This allows you to use time-related functions with your Canvas data.

### Usage Examples

Once connected, you can ask Cursor AI about your Canvas data:

- "What assignments do I have due next week?"
- "Show me the syllabus for my Biology course"
- "List all my upcoming quizzes"
- "What's on my schedule for tomorrow?"

Example conversation:

```
YOU: What assignments do I have due soon?

CURSOR: I'll check your upcoming assignments.

Based on your Canvas data, here are your upcoming assignments:
- "Final Project" for CS101 due on December 10, 2023
- "Lab Report #5" for BIOL200 due on December 7, 2023
- "Research Paper" for ENGL301 due on December 15, 2023
```

## Development

For detailed development instructions, please see the [DEVELOPMENT.md](DEVELOPMENT.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
