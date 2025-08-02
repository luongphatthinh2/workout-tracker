from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db_session
from core.pagination import get_pagination, PaginationParams
from query.exercise import get_exercises, get_exercises_by_type
from schemas.exercise import ExerciseWithType


router = APIRouter()

@router.get("/exercises", response_model=list[ExerciseWithType])
async def list_exercises(
    db: AsyncSession = Depends(get_db_session),
    pagination: PaginationParams = Depends(get_pagination)
):
    exercises = await get_exercises(db, limit=pagination.limit, offset=pagination.offset)
    return exercises

@router.get("/exercise-types/{type_name}/exercises", response_model=list[ExerciseWithType])
async def list_exercises_by_type(
    type_name: str = Path( description="Exercise type name"),
    db: AsyncSession = Depends(get_db_session),
    pagination: PaginationParams = Depends(get_pagination)
):
    return await get_exercises_by_type(
        db,
        type_name=type_name,
        limit=pagination.limit,
        offset=pagination.offset
    )
