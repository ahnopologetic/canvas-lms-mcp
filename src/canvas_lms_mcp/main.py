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
    PaginatedResponse,
    PlannerItem,
    Quiz,
)

logger = logging.getLogger(__name__)
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")

canvas_client = CanvasClient(api_token=CANVAS_API_TOKEN, base_url=CANVAS_BASE_URL)
mcp = FastMCP(name="canvas-lms-mcp")


@mcp.prompt()
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
) -> List[Module]:
    """
    Get modules for a course.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include

    Returns:
        List of Module objects
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

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
) -> PaginatedResponse:
    """
    List assignments for a course.

    Args:
        course_id: Course ID
        bucket: Bucket to filter assignments by (past, overdue, undated, ungraded, unsubmitted, upcoming, future)
        order_by: Field to order assignments by (due_at, position, name)

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
    return PaginatedResponse(
        items=items,
        # next_page=response.get("next_page"),
        # previous_page=response.get("previous_page"),
    )


@mcp.tool()
async def list_courses() -> PaginatedResponse:
    """
    List courses that the user is actively enrolled in.

    Args:
        include: Optional list of additional data to include

    Returns:
        PaginatedResponse containing courses
    """
    client = CanvasClient.get_instance()

    params = {}
    params["enrollment_type"] = "student"
    params["enrollment_state"] = "active"

    response = await client.get("/api/v1/courses", params=params)

    items = [Course.model_validate(item) for item in response]

    return PaginatedResponse(
        items=items,
    )


@mcp.tool()
async def list_files(
    course_id: Optional[int] = None,
    folder_id: Optional[int] = None,
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List files for a course or folder.

    Args:
        course_id: Optional Course ID
        folder_id: Optional Folder ID
        include: Optional list of additional data to include

    Returns:
        PaginatedResponse containing files
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
    return PaginatedResponse(
        items=items,
        # next_page=response.get("next_page"),
        # previous_page=response.get("previous_page"),
    )


@mcp.tool()
async def list_planner_items(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    context_codes: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List planner items for the authenticated user.

    Args:
        start_date: Optional start date in ISO 8601 format
        end_date: Optional end date in ISO 8601 format
        context_codes: Optional list of context codes (e.g., ["course_123"])

    Returns:
        PaginatedResponse containing planner items
    """
    client = CanvasClient.get_instance()
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if context_codes:
        params["context_codes[]"] = context_codes

    response = await client.get("/api/v1/planner/items", params=params)

    items = [PlannerItem.model_validate(item) for item in response]
    return PaginatedResponse(
        items=items,
        # next_page=response.get("next_page"),
        # previous_page=response.get("previous_page"),
    )


@mcp.tool()
async def list_quizzes(
    course_id: int,
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List quizzes for a course.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include

    Returns:
        PaginatedResponse containing quizzes
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get(f"/api/v1/courses/{course_id}/quizzes", params=params)

    items = [Quiz.model_validate(item) for item in response]
    return PaginatedResponse(
        items=items,
        # next_page=response.get("next_page"),
        # previous_page=response.get("previous_page"),
    )


if __name__ == "__main__":
    print("Starting Canvas MCP server...")
    mcp.run()
