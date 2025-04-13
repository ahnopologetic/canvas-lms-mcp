from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.main import mcp
from canvas_lms_mcp.schema import Assignment


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
