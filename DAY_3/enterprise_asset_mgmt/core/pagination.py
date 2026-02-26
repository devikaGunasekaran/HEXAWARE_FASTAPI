from typing import List, Generic, TypeVar, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

def paginate(query: Query, page: int, size: int) -> dict:
    total = query.count()
    pages = (total + size - 1) // size if size > 0 else 0
    items = query.offset((page - 1) * size).limit(size).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }
