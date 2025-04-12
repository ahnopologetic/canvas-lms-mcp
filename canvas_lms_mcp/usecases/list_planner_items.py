from typing import List, Optional

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.schema import PaginatedResponse, PlannerItem
from canvas_lms_mcp.tools import tool


@tool
async def list_planner_items(
    client: CanvasClient,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    context_codes: Optional[List[str]] = None,
) -> PaginatedResponse:
    """
    List planner items for the authenticated user.

    Args:
        client: Canvas API client
        start_date: Optional start date in ISO 8601 format
        end_date: Optional end date in ISO 8601 format
        context_codes: Optional list of context codes (e.g., ["course_123"])

    Returns:
        PaginatedResponse containing planner items
    """
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if context_codes:
        params["context_codes[]"] = context_codes

    response = await client.get("/api/v1/planner/items", params=params)

    items = [PlannerItem(**item) for item in response.get("items", [])]
    return PaginatedResponse(
        items=items,
        next_page=response.get("next_page"),
        previous_page=response.get("previous_page"),
    )
