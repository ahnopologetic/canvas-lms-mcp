from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.main import mcp


@mcp.tool()
async def get_course_syllabus(
    course_id: int,
) -> str:
    """
    Get a course's syllabus.

    Args:
        course_id: Course ID

    Returns:
        Course syllabus as string
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/syllabus")
    return response.get("syllabus_body", "")
