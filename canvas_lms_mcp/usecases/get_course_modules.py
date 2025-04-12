from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Module
from canvas_lms_mcp.tools import tool


@tool()
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
