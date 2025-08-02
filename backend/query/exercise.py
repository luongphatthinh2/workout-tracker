# query/exercise.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models.exercise import Exercise, ExerciseType

async def get_exercises(
    db: AsyncSession,
    limit: int = 10,
    offset: int = 0
):
    stmt = (
        select(Exercise)
        .options(selectinload(Exercise.type))  # eager load the type relationship
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)

    exercises = result.scalars().all()
    print('DEBUG88 exercises ', exercises)

    # convert manually to dicts for Pydantic
    return [
        {
            "exercise_name": ex.exercise_name,
            "description": ex.description,
            "video_url": ex.video_url,
            "exercise_type_name": ex.type.exercise_type_name if ex.type else None
        }
        for ex in exercises
    ]

async def get_exercises_by_type(
    db: AsyncSession,
    type_name: str,
    limit: int = 10,
    offset: int = 0
):
    stmt = (
        select(Exercise)
        .join(ExerciseType)
        .options(selectinload(Exercise.type))
        .where(ExerciseType.exercise_type_name == type_name)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    exercises = result.scalars().all()
    print('DEBUG88 exercises ', exercises)

    return [
        {
           "exercise_name": ex.exercise_name,
            "description": ex.description,
            "video_url": ex.video_url,
            "exercise_type_name": ex.type.exercise_type_name if ex.type else None
        }
        for ex in exercises
    ]