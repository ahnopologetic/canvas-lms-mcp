import logging
import os
from typing import List, Literal, Optional

from fastmcp import FastMCP

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import (
    Announcement,
    Assignment,
    AssignmentGroup,
    CalendarEvent,
    Course,
    Discussion,
    Enrollment,
    File,
    Module,
    ModuleItem,
    Page,
    PaginatedResponse,
    PlannerItem,
    Quiz,
    Submission,
    Tab,
)
from canvas_lms_mcp.utils import paginate_response

logger = logging.getLogger(__name__)
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")

canvas_client = CanvasClient(api_token=CANVAS_API_TOKEN, base_url=CANVAS_BASE_URL)
mcp = FastMCP(name="canvas-lms-mcp")


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
    response = await client.get(
        f"/api/v1/courses/{course_id}", params={"include[]": "syllabus_body"}
    )
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
    include: Optional[List[str]] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse:
    """
    List assignments for a course.

    Args:
        course_id: Course ID
        bucket: Bucket to filter assignments by (past, overdue, undated, ungraded, unsubmitted, upcoming, future)
        order_by: Field to order assignments by (due_at, position, name)
        include: Optional list of additional data to include (e.g., ["submission"] to see grade status)
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
    if include:
        params["include[]"] = include

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
) -> dict:
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
    items = [ModuleItem.model_validate(item).model_dump() for item in response]
    return {"items": items, "total": len(items)}


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


@mcp.tool()
async def get_page(
    course_id: int,
    page_slug: str,
) -> Page:
    """
    Get a single page by its URL slug.

    Args:
        course_id: Course ID
        page_slug: Page URL slug (e.g., "kurshandbok", "examination")

    Returns:
        Page object with title, body (HTML), and metadata
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/pages/{page_slug}")
    return Page.model_validate(response)


@mcp.tool()
async def list_submissions(
    course_id: int,
    include: Optional[List[str]] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[Submission]:
    """
    List the current user's submissions for a course, including grades and feedback.

    Args:
        course_id: Course ID
        include: Optional list of additional data (e.g., ["assignment", "submission_comments"])
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing submissions with grades and comments
    """
    client = CanvasClient.get_instance()
    params = {"student_ids[]": "self"}
    if include:
        params["include[]"] = include

    response = await client.get(
        f"/api/v1/courses/{course_id}/students/submissions", params=params
    )

    items = [Submission.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_announcements(
    course_ids: List[int],
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[Announcement]:
    """
    List announcements for one or more courses.

    Args:
        course_ids: List of course IDs to fetch announcements for
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing announcements
    """
    client = CanvasClient.get_instance()
    params = {"context_codes[]": [f"course_{cid}" for cid in course_ids]}

    response = await client.get("/api/v1/announcements", params=params)

    items = [Announcement.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def list_discussions(
    course_id: int,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[Discussion]:
    """
    List discussion topics for a course.

    Args:
        course_id: Course ID
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing discussion topics
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/discussion_topics")

    items = [Discussion.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def get_discussion_view(
    course_id: int,
    discussion_id: int,
) -> dict:
    """
    Get the full view of a discussion topic including all replies.

    Args:
        course_id: Course ID
        discussion_id: Discussion topic ID

    Returns:
        Full discussion view with participants and all entries
    """
    client = CanvasClient.get_instance()
    response = await client.get(
        f"/api/v1/courses/{course_id}/discussion_topics/{discussion_id}/view"
    )
    return response


@mcp.tool()
async def list_calendar_events(
    context_codes: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    items_per_page: int = 10,
) -> PaginatedResponse[CalendarEvent]:
    """
    List calendar events for courses.

    Args:
        context_codes: List of context codes (e.g., ["course_4538"])
        start_date: Optional start date in ISO 8601 format
        end_date: Optional end date in ISO 8601 format
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing calendar events
    """
    client = CanvasClient.get_instance()
    params = {"context_codes[]": context_codes}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    response = await client.get("/api/v1/calendar_events", params=params)

    items = [CalendarEvent.model_validate(item) for item in response]
    return await paginate_response(items, page, items_per_page)


@mcp.tool()
async def get_enrollments() -> dict:
    """
    Get the current user's enrollments including grades.

    Returns:
        Dict with enrollment items including course IDs and grade data
    """
    client = CanvasClient.get_instance()
    response = await client.get("/api/v1/users/self/enrollments")
    items = [Enrollment.model_validate(item).model_dump() for item in response]
    return {"items": items, "total": len(items)}


@mcp.tool()
async def list_assignment_groups(
    course_id: int,
) -> dict:
    """
    List assignment groups for a course (shows grade weighting/categories).

    Args:
        course_id: Course ID

    Returns:
        Dict with assignment group items
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/assignment_groups")
    items = [AssignmentGroup.model_validate(item).model_dump() for item in response]
    return {"items": items, "total": len(items)}


@mcp.tool()
async def get_tabs(
    course_id: int,
) -> dict:
    """
    Get available tabs/navigation items for a course.

    Args:
        course_id: Course ID

    Returns:
        Dict with tab items showing available course sections
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/tabs")
    items = [Tab.model_validate(item).model_dump() for item in response]
    return {"items": items, "total": len(items)}


@mcp.tool()
async def list_favorites() -> dict:
    """
    List the current user's favorite courses.

    Returns:
        Dict with favorite course items
    """
    client = CanvasClient.get_instance()
    response = await client.get("/api/v1/users/self/favorites/courses")
    items = [Course.model_validate(item).model_dump() for item in response]
    return {"items": items, "total": len(items)}


if __name__ == "__main__":
    print("Starting Canvas MCP server...")
    mcp.run()
