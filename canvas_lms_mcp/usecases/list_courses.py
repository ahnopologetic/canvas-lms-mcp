from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Course, PaginatedResponse
from canvas_lms_mcp.tools import tool


@tool
async def list_courses(
    client: CanvasClient,
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List courses for the authenticated user.

    Args:
        client: Canvas API client
        include: Optional list of additional data to include

    Returns:
        PaginatedResponse containing courses
    """
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get("/api/v1/courses", params=params)

    items = [Course(**item) for item in response.get("items", [])]
    return PaginatedResponse(
        items=items,
        next_page=response.get("next_page"),
        previous_page=response.get("previous_page"),
    )
