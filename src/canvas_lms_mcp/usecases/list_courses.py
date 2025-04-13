from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.main import mcp
from canvas_lms_mcp.schema import Course, PaginatedResponse


@mcp.tool()
async def list_courses(
    include: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List courses from the Canvas LMS for the authenticated user.

    Args:
        include: Optional list of additional data to include

    Returns:
        PaginatedResponse containing courses
    """
    client = CanvasClient.get_instance()
    params = {}
    if include:
        params["include[]"] = include

    response = await client.get("/api/v1/courses", params=params)
    return response
    # print(response)

    # items = [Course(**item) for item in response.get("items", [])]
    # return PaginatedResponse(
    #     items=items,
    #     next_page=response.get("next_page"),
    #     previous_page=response.get("previous_page"),
    # )
