from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel


class PlannerItem(BaseModel):
    id: int
    title: str
    due_at: Optional[datetime] = None
    course_id: Optional[int] = None
    html_url: Optional[str] = None
    type: str  # assignment, quiz, etc.


class Assignment(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    due_at: Optional[datetime] = None
    points_possible: Optional[float] = None
    html_url: Optional[str] = None


class Quiz(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_at: Optional[datetime] = None
    points_possible: Optional[float] = None
    html_url: Optional[str] = None


class Course(BaseModel):
    id: int
    name: str
    course_code: Optional[str] = None
    syllabus_body: Optional[str] = None
    enrollment_term_id: Optional[int] = None
    html_url: Optional[str] = None


class Module(BaseModel):
    id: int
    name: str
    position: Optional[int] = None
    items: Optional[List[dict]] = None


class File(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None


# Response models

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_page: Optional[str] = None
    previous_page: Optional[str] = None
