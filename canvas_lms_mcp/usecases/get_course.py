from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Course
from canvas_lms_mcp.tools import tool


@tool
async def get_course(
    client: CanvasClient,
    course_id: int,
    include: Optional[List[str]] = None,
) -> Course:
    """
    Get a single course by ID.

    Args:
        client: Canvas API client
        course_id: Course ID
        include: Optional list of additional data to include

    Returns:
        Course object
    """
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get(f"/api/v1/courses/{course_id}", params=params)
    return Course(**response)
