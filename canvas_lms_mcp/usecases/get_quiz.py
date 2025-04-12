from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import Quiz
from canvas_lms_mcp.tools import tool


@tool()
async def get_quiz(
    course_id: int,
    quiz_id: int,
) -> Quiz:
    """
    Get a single quiz by ID.

    Args:
        course_id: Course ID
        quiz_id: Quiz ID

    Returns:
        Quiz object
    """
    client = CanvasClient.get_instance()
    response = await client.get(f"/api/v1/courses/{course_id}/quizzes/{quiz_id}")
    return Quiz(**response)
