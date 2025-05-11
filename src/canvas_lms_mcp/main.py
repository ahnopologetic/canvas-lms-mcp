import logging
import os
from typing import List, Literal, Optional

from fastmcp import FastMCP
from fastmcp.prompts.prompt import AssistantMessage, UserMessage

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import (
    Assignment,
    Course,
    File,
    Module,
    ModuleItem,
    PaginatedResponse,
    PlannerItem,
    Quiz,
)
from canvas_lms_mcp.utils import paginate_response

logger = logging.getLogger(__name__)
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")

canvas_client = CanvasClient(api_token=CANVAS_API_TOKEN, base_url=CANVAS_BASE_URL)
mcp = FastMCP(name="canvas-lms-mcp")


@mcp.prompt("upcoming_works")
def upcoming_works(assignments: list[str], quizzes: list[str]):
    return [
        UserMessage(
            content="I need to know what I have due soon",
            role="user",
        ),
        AssistantMessage(
            content="Here are the assignments and quizzes that are due soon",
            role="assistant",
        ),
        AssistantMessage(
            content=f"Assignments: {assignments}\nQuizzes: {quizzes}",
            role="assistant",
        ),
    ]


# TODO: remove these tools from main.py and move to usecases folder
@mcp.tool()
async def get_assignment(
    course_id: int,
    assignment_id: int,
) -> Assignment:
    """
    Get a single assignment by ID.

    Args:
        course_id: Course ID
        assignment_id: Assignment ID

    Returns:
        Assignment object
    """
    client = CanvasClient.get_instance()
    response = await client.get(
        f"/api/v1/courses/{course_id}/assignments/{assignment_id}"
    )
    return Assignment(**response)


@mcp.tool()
async def get_course_modules(
    course_id: int,
    include: Optional[List[str]] = None,
    per_page: int = 100,
) -> List[Module]:
    """
    Get modules for a course.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include
        per_page: Number of items per page
    Returns:
        List of Module objects
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include
    if per_page:
        params["per_page"] = per_page

    response = await client.get(f"/api/v1/courses/{course_id}/modules", params=params)
    return [Module(**module) for module in response]


@mcp.tool()
async def get_course_syllabus(
    course_id: int,
) -> str:
    """
    Get a course's syllabus.

    Args:
        course_id: Course ID

    Returns:
        Course syllabus as string
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/syllabus")
    return response.get("syllabus_body", "")


@mcp.tool()
async def get_course(
    course_id: int,
    include: Optional[List[str]] = None,
) -> Course:
    """
    Get a single course by ID.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include

    Returns:
        Course object
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get(f"/api/v1/courses/{course_id}", params=params)
    return Course(**response)


@mcp.tool()
async def get_quiz(
    course_id: int,
    quiz_id: int,
) -> Quiz:
    """
    Get a single quiz by ID.

    Args:
        course_id: Course ID
        quiz_id: Quiz ID

    Returns:
        Quiz object
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/quizzes/{quiz_id}")
    return Quiz(**response)


@mcp.tool()
async def list_assignments(
    course_id: int,
    bucket: Literal[
        "past", "overdue", "undated", "ungraded", "unsubmitted", "upcoming", "future"
    ],
    order_by: Literal["due_at", "position", "name"],
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse:
    """
    List assignments for a course.

    Args:
        course_id: Course ID
        bucket: Bucket to filter assignments by (past, overdue, undated, ungraded, unsubmitted, upcoming, future)
        order_by: Field to order assignments by (due_at, position, name)
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing assignments
    """
    client = CanvasClient.get_instance()
    params = {}
    if bucket:
        params["bucket"] = bucket
    if order_by:
        params["order_by"] = order_by

    response = await client.get(
        f"/api/v1/courses/{course_id}/assignments", params=params
    )

    items = [Assignment.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_courses(
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse:
    """
    List courses that the user is actively enrolled in.

    Args:
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing courses
    """
    client = CanvasClient.get_instance()

    params = {}
    params["enrollment_type"] = "student"
    params["enrollment_state"] = "active"

    response = await client.get("/api/v1/courses", params=params)

    items = [Course.model_validate(item) for item in response]

    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_files(
    course_id: Optional[int] = None,
    folder_id: Optional[int] = None,
    include: Optional[List[str]] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[File]:
    """
    List files for a course or folder.

    Args:
        course_id: Optional Course ID
        folder_id: Optional Folder ID
        include: Optional list of additional data to include
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse[File]
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

    if course_id:
        endpoint = f"/api/v1/courses/{course_id}/files"
    elif folder_id:
        endpoint = f"/api/v1/folders/{folder_id}/files"
    else:
        endpoint = "/api/v1/users/self/files"

    response = await client.get(endpoint, params=params)

    items = [File.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_planner_items(
    start_date: str,
    end_date: str,
    context_codes: List[str] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[PlannerItem]:
    """
    List planner items for the authenticated user.

    Args:
        start_date: start date in ISO 8601 format
        end_date: end date in ISO 8601 format
        context_codes: list of context codes (e.g., ["course_123"])
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse[PlannerItem]
    """
    client = CanvasClient.get_instance()
    params = {}
    params["start_date"] = start_date
    params["end_date"] = end_date

    if context_codes:
        params["context_codes[]"] = context_codes

    response = await client.get("/api/v1/planner/items", params=params)

    items = [PlannerItem.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_quizzes(
    course_id: int,
    include: Optional[List[str]] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse:
    """
    List quizzes for a course.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing quizzes
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get(f"/api/v1/courses/{course_id}/quizzes", params=params)

    items = [Quiz.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def get_module_items(
    course_id: int,
    module_id: int,
) -> PaginatedResponse[ModuleItem]:
    """
    Get items for a module.

    Args:
        course_id: Course ID
        module_id: Module ID
    """
    client = CanvasClient.get_instance()
    response = await client.get(
        f"/api/v1/courses/{course_id}/modules/{module_id}/items"
    )
    return [ModuleItem.model_validate(item) for item in response]


@mcp.tool()
async def get_file(
    course_id: int,
    file_id: int,
) -> File:
    """
    Get a file by ID.

    Args:
        course_id: Course ID
        file_id: File ID

    Returns:
        File object
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/files/{file_id}")
    return File.model_validate(response)


if __name__ == "__main__":
    print("Starting Canvas MCP server...")
    mcp.run()
