from typing import TypeVar, List, Generic
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total_count: int
    page: int
    size: int

def paginate(items: list, page: int, size: int):
    start = (page - 1) * size
    end = start + size
    return PaginatedResponse(
        items=items[start:end],
        total_count=len(items),
        page=page,
        size=size
    )
