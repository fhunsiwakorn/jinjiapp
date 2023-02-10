from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel
from datetime import date, datetime, time

T = TypeVar('T')


class ResponseProcess(GenericModel, Generic[T]):
    status: str
    status_code: str
    message: str


class ResponseData(GenericModel, Generic[T]):
    status: str
    status_code: str
    message: str
    page: int
    per_page: int
    total_page: int
    total_data: int
    total_filter_data: int
    data: Optional[T]


class FilterRequestSchema(GenericModel, Generic[T]):
    page: Optional[int] = 0
    per_page: Optional[int] = 100
    search_value: Optional[str] = None


class fullcalendarTypeAOutSchema(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    editable: Optional[bool] = None
    backgroundColor: Optional[str] = None

    class Config:
        orm_mode = True


class fullcalendarTypeBOutSchema(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None
    backgroundColor: Optional[str] = None

    class Config:
        orm_mode = True
