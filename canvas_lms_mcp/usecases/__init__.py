import inspect
import sys

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
