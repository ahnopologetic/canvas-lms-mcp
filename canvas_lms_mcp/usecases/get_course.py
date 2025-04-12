from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Course
from canvas_lms_mcp.tools import tool


@tool()
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
