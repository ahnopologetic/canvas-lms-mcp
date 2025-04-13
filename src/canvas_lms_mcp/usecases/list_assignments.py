from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.main import mcp
from canvas_lms_mcp.schema import Assignment, PaginatedResponse


@mcp.tool()
async def list_assignments(
    course_id: int,
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List assignments for a course.

    Args:
        course_id: Course ID
        include: Optional list of additional data to include (e.g., ["submission"])

    Returns:
        PaginatedResponse containing assignments
    """
    client = CanvasClient.get_instance()
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
