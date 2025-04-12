from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Assignment, PaginatedResponse
from canvas_lms_mcp.tools import tool


@tool
async def list_assignments(
    client: CanvasClient,
    course_id: int,
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List assignments for a course.

    Args:
        client: Canvas API client
        course_id: Course ID
        include: Optional list of additional data to include (e.g., ["submission"])

    Returns:
        PaginatedResponse containing assignments
    """
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get(
        f"/api/v1/courses/{course_id}/assignments", params=params
    )

    items = [Assignment(**item) for item in response.get("items", [])]
    return PaginatedResponse(
        items=items,
        next_page=response.get("next_page"),
        previous_page=response.get("previous_page"),
    )
