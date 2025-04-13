import inspect
import sys

from canvas_lms_mcp.usecases.get_assignment import get_assignment
from canvas_lms_mcp.usecases.get_course import get_course
from canvas_lms_mcp.usecases.get_course_modules import get_course_modules
from canvas_lms_mcp.usecases.get_course_syllabus import get_course_syllabus
from canvas_lms_mcp.usecases.get_quiz import get_quiz
from canvas_lms_mcp.usecases.list_assignments import list_assignments
from canvas_lms_mcp.usecases.list_courses import list_courses
from canvas_lms_mcp.usecases.list_files import list_files
from canvas_lms_mcp.usecases.list_planner_items import list_planner_items
from canvas_lms_mcp.usecases.list_quizzes import list_quizzes

__all__ = [
    "get_assignment",
    "get_course",
    "get_course_modules",
    "get_course_syllabus",
    "get_quiz",
    "list_assignments",
    "list_courses",
    "list_files",
    "list_planner_items",
    "list_quizzes",
]


TOOLS_DEFINITION = [
    obj
    for name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isfunction(obj) and hasattr(obj, "_is_tool") and obj._is_tool
]
