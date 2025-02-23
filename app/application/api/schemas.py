from typing import TypeVar, Generic

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str

R = TypeVar("R", bound=BaseModel)

class BaseQueryResponseSchema(BaseModel, Generic[R]):
    count: int
    offset: int
    limit: int
    items: R

