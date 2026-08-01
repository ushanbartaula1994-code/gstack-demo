"""
Common Pydantic schemas
"""

from pydantic import BaseModel, field_validator
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    success: bool = True


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper"""
    data: Optional[T] = None
    message: Optional[str] = None
    success: bool = True
    errors: Optional[list[str]] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20
    total_pages: int = 1


class FilterParams(BaseModel):
    """Base filter parameters"""
    page: int = 1
    page_size: int = 20
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"

    @field_validator('page', 'page_size')
    @classmethod
    def validate_positive(cls, value):
        if value < 1:
            raise ValueError('Must be greater than 0')
        return value

    @field_validator('sort_order')
    @classmethod
    def validate_sort_order(cls, value):
        if value and value not in ['asc', 'desc']:
            raise ValueError('Must be either asc or desc')
        return value
