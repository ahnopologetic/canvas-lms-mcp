# Canvas LMS MCP Server

[![smithery badge](https://smithery.ai/badge/@ahnopologetic/canvas-lms-mcp)](https://smithery.ai/server/@ahnopologetic/canvas-lms-mcp)
A minimal Canvas LMS MCP (Machine Conversation Protocol) server for easy access to education data through your Canvas LMS instance. This server provides a bridge between AI systems (like Cursor) and Canvas Learning Management System.

## Features

- **Courses**: List enrolled courses, get course details, syllabus, modules, and module items
- **Assignments**: List and get assignments with optional submission status
- **Pages**: Get course pages by URL slug
- **Submissions**: List your own submissions with grades and feedback
- **Announcements**: List announcements across multiple courses
- **Discussions**: List topics and view full discussion threads
- **Calendar**: List calendar events with date filtering
- **Planner**: List planner items (assignments, announcements, etc.)
- **Enrollments**: Get enrollment data with grades
- **Quizzes**: List and get quizzes (classic quizzes only)
- **Files**: List and get files
- **Navigation**: Get course tabs, assignment groups, and favorite courses

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

The server provides 22 tools for interacting with Canvas LMS:

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
Get a course's syllabus body as HTML.

Parameters:
- `course_id` (required): Course ID

#### `get_course_modules`
Get modules for a course.

Parameters:
- `course_id` (required): Course ID
- `include` (optional): List of additional data to include
- `per_page` (optional, default=100): Number of items per page

#### `get_module_items`
Get items for a specific module.

Parameters:
- `course_id` (required): Course ID
- `module_id` (required): Module ID

### Assignments

#### `list_assignments`
List assignments for a course.

Parameters:
- `course_id` (required): Course ID
- `bucket` (required): Filter by "past", "overdue", "undated", "ungraded", "unsubmitted", "upcoming", or "future"
- `order_by` (required): Order by "due_at", "position", or "name"
- `include` (optional): List of additional data to include (e.g., `["submission"]` to see grade status)
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_assignment`
Get a single assignment by ID.

Parameters:
- `course_id` (required): Course ID
- `assignment_id` (required): Assignment ID

#### `list_assignment_groups`
List assignment groups for a course (shows grade weighting/categories).

Parameters:
- `course_id` (required): Course ID

### Pages

#### `get_page`
Get a single page by its URL slug.

Parameters:
- `course_id` (required): Course ID
- `page_slug` (required): Page URL slug (e.g., "syllabus", "course-handbook")

### Submissions

#### `list_submissions`
List the current user's submissions for a course, including grades and feedback.

Parameters:
- `course_id` (required): Course ID
- `include` (optional): List of additional data (e.g., `["assignment", "submission_comments"]`)
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

### Announcements

#### `list_announcements`
List announcements for one or more courses.

Parameters:
- `course_ids` (required): List of course IDs
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

### Discussions

#### `list_discussions`
List discussion topics for a course.

Parameters:
- `course_id` (required): Course ID
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_discussion_view`
Get the full view of a discussion topic including all replies.

Parameters:
- `course_id` (required): Course ID
- `discussion_id` (required): Discussion topic ID

### Calendar

#### `list_calendar_events`
List calendar events for courses.

Parameters:
- `context_codes` (required): List of context codes (e.g., `["course_123"]`)
- `start_date` (optional): Start date in ISO 8601 format
- `end_date` (optional): End date in ISO 8601 format
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

### Planner Items

#### `list_planner_items`
List planner items for the authenticated user.

Parameters:
- `start_date` (required): Start date in ISO 8601 format
- `end_date` (required): End date in ISO 8601 format
- `context_codes` (optional): List of context codes (e.g., `["course_123"]`)
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

### Enrollments

#### `get_enrollments`
Get the current user's enrollments including grades.

### Quizzes

#### `list_quizzes`
List quizzes for a course. Note: only works with Classic Quizzes, not New Quizzes (quiz_lti).

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
List files for a course or folder. Note: may return 403 for student accounts depending on institution permissions.

Parameters:
- `course_id` (optional): Course ID
- `folder_id` (optional): Folder ID
- `include` (optional): List of additional data to include
- `page` (optional, default=1): Page number (1-indexed)
- `items_per_page` (optional, default=10): Number of items per page

#### `get_file`
Get a file by ID. Works with known file IDs even when `list_files` is restricted.

Parameters:
- `course_id` (required): Course ID
- `file_id` (required): File ID

### Other

#### `get_tabs`
Get available tabs/navigation items for a course.

Parameters:
- `course_id` (required): Course ID

#### `list_favorites`
List the current user's favorite courses.

## Integration

This MCP server works with any client that supports the [Model Context Protocol](https://modelcontextprotocol.io/), including Claude Desktop, Claude Code, Cursor, Windsurf, and others.

The MCP configuration is the same across all clients — only the config file location differs:

```json
{
    "mcpServers": {
        "canvas": {
            "command": "uvx",
            "args": ["canvas-lms-mcp"],
            "env": {
                "CANVAS_API_TOKEN": "your_canvas_api_token",
                "CANVAS_BASE_URL": "https://your-institution.instructure.com"
            }
        }
    }
}
```

Replace `your_canvas_api_token` with your Canvas API token (found in Canvas → Account → Settings → New Access Token) and `your-institution.instructure.com` with your institution's Canvas URL.

### Claude Desktop

Add to your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop after saving.

### Claude Code

Add to your project's `.mcp.json` or global `~/.claude/settings.json`:

```json
{
    "mcpServers": {
        "canvas": {
            "command": "uvx",
            "args": ["canvas-lms-mcp"],
            "env": {
                "CANVAS_API_TOKEN": "your_canvas_api_token",
                "CANVAS_BASE_URL": "https://your-institution.instructure.com"
            }
        }
    }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project directory. Restart Cursor after saving.

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`. Restart Windsurf after saving.

### Usage Examples

Once connected, you can ask your AI assistant about your Canvas data:

- "What assignments do I have due next week?"
- "Show me the syllabus for my Biology course"
- "What announcements were posted today?"
- "What are my grades so far?"
- "What's on my schedule for tomorrow?"
- "Show me the discussion posts for my English class"

## Development

For detailed development instructions, please see the [DEVELOPMENT.md](DEVELOPMENT.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
