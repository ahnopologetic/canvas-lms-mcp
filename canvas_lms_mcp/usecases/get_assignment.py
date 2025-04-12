from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Assignment
from canvas_lms_mcp.tools import tool


@tool
async def get_assignment(
    client: CanvasClient,
    course_id: int,
    assignment_id: int,
) -> Assignment:
    """
    Get a single assignment by ID.

    Args:
        client: Canvas API client
        course_id: Course ID
        assignment_id: Assignment ID

    Returns:
        Assignment object
    """
    response = await client.get(
        f"/api/v1/courses/{course_id}/assignments/{assignment_id}"
    )
    return Assignment(**response)
