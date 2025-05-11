from typing import Dict, List, TypeVar

from canvas_lms_mcp.schema import PaginatedResponse

T = TypeVar("T")


def paginate_items(items: List[T], page: int = 1, items_per_page: int = 10) -> Dict:
    """
    Paginate a list of items.

    Args:
        items: List of items to paginate
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        Dict containing paginated items and pagination metadata
    """
    total_items = len(items)
    total_pages = (
        total_items + items_per_page - 1
    ) // items_per_page  # Ceiling division

    # Ensure page is within bounds
    page = max(1, min(page, total_pages) if total_pages > 0 else 1)

    # Calculate start and end indices
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)

    # Extract items for the current page
    paginated_items = items[start_idx:end_idx]

    # Calculate next and previous page urls/identifiers
    next_page = str(page + 1) if page < total_pages else None
    previous_page = str(page - 1) if page > 1 else None

    return {
        "items": paginated_items,
        "next_page": next_page,
        "previous_page": previous_page,
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "items_per_page": items_per_page,
    }


async def paginate_response(
    response_items: List[T], page: int = 1, items_per_page: int = 10
) -> PaginatedResponse[T]:
    """
    Create a PaginatedResponse from a list of items.

    Args:
        response_items: List of response items to paginate
        page: Page number (1-indexed)
        items_per_page: Number of items per page

    Returns:
        PaginatedResponse containing paginated items
    """
    pagination_data = paginate_items(response_items, page, items_per_page)

    return PaginatedResponse(
        items=pagination_data["items"],
        next_page=pagination_data["next_page"],
        previous_page=pagination_data["previous_page"],
        page=pagination_data["page"],
        total_pages=pagination_data["total_pages"],
        total_items=pagination_data["total_items"],
        items_per_page=pagination_data["items_per_page"],
    )
