from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import File, PaginatedResponse
from canvas_lms_mcp.tools import tool


@tool()
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

    items = [File(**item) for item in response.get("items", [])]
    return PaginatedResponse(
        items=items,
        next_page=response.get("next_page"),
        previous_page=response.get("previous_page"),
    )
