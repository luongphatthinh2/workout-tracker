from fastapi import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    limit: int = Query(10, ge=1, le=100)
    offset: int = Query(0, ge=0)

def get_pagination(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)
