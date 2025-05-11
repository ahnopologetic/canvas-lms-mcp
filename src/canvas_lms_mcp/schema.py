from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


class Plannable(BaseModel):
    id: int
    title: str
    read_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PlannerItem(BaseModel):
    due_at: Optional[datetime] = None
    course_id: Optional[int] = None
    context_type: str
    context_name: Optional[str] = None
    plannable_type: str
    plannable: Plannable
    html_url: Optional[str] = None


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
    state: Optional[str] = None
    completed_at: Optional[datetime] = None
    items_url: Optional[str] = None


class ModuleItem(BaseModel):
    id: int
    title: str
    position: Optional[int] = None
    indent: Optional[int] = None
    quiz_lti: Optional[bool] = None
    type: str
    module_id: Optional[int] = None
    html_url: Optional[str] = None
    content_id: Optional[int] = None
    url: Optional[str] = None


class File(BaseModel):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    filename: Optional[str] = None
    folder_id: Optional[int] = None
    url: Optional[str] = Field(
        default=None,
        alias="url",
        description="Downloadable URL for the file",
    )
    size: Optional[int] = None
    content_type: Optional[str] = None
    mime_class: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    unlock_at: Optional[datetime] = None
    lock_at: Optional[datetime] = None
    hidden: Optional[bool] = None
    locked: Optional[bool] = None
    hidden_for_user: Optional[bool] = None
    locked_for_user: Optional[bool] = None
    thumbnail_url: Optional[str] = None
    uuid: Optional[str] = None
    upload_status: Optional[str] = None
    visibility_level: Optional[str] = None
    category: Optional[str] = None
    media_entry_id: Optional[str] = None
    canvadoc_session_url: Optional[str] = None
    crocodoc_session_url: Optional[str] = None


# Response models

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_page: Optional[str] = None
    previous_page: Optional[str] = None
    page: Optional[int] = None
    total_pages: Optional[int] = None
    total_items: Optional[int] = None
    items_per_page: Optional[int] = None
