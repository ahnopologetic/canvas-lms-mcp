from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.tools import tool


@tool
async def get_course_syllabus(
    client: CanvasClient,
    course_id: int,
) -> str:
    """
    Get a course's syllabus.

    Args:
        client: Canvas API client
        course_id: Course ID

    Returns:
        Course syllabus as string
    """
    response = await client.get(f"/api/v1/courses/{course_id}/syllabus")
    return response.get("syllabus_body", "")
