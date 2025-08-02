import asyncio
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from db.init_db import Base
from models.exercise import Exercise, ExerciseType  # Adjust import path as needed

# Load .env file
load_dotenv()
DATABASE_URL = os.getenv("URL")

# Sample Data
exercise_types = ["Strength", "Cardio", "Flexibility", "Balance"]

exercises = [
    ("Push-up", "Strength"),
    ("Squat", "Strength"),
    ("Deadlift", "Strength"),
    ("Bench Press", "Strength"),
    ("Lunges", "Strength"),
    ("Running", "Cardio"),
    ("Cycling", "Cardio"),
    ("Jump Rope", "Cardio"),
    ("Burpees", "Cardio"),
    ("Mountain Climbers", "Cardio"),
    ("Hamstring Stretch", "Flexibility"),
    ("Quad Stretch", "Flexibility"),
    ("Triceps Stretch", "Flexibility"),
    ("Shoulder Stretch", "Flexibility"),
    ("Seated Forward Bend", "Flexibility"),
    ("Tree Pose", "Balance"),
    ("Single-Leg Stand", "Balance"),
    ("Heel-to-Toe Walk", "Balance"),
    ("Tai Chi", "Balance"),
    ("Balance Board", "Balance"),
]

async def seed_exercises():
    # Create engine and session
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    # Create tables if not exist (optional, only if needed)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        async with session.begin():  # atomic transaction
        # Insert Exercise Types
            type_map = {}
            for type_name in exercise_types:
                existing = await session.scalar(
                    ExerciseType.__table__.select().where(ExerciseType.name == type_name)
                )
                if not existing:
                    etype = ExerciseType(name=type_name)
                    session.add(etype)
                    await session.flush()
                    type_map[type_name] = etype.id
                else:
                    type_map[type_name] = existing.id

            # Insert Exercises
            for ex_name, ex_type in exercises:
                existing = await session.scalar(
                    Exercise.__table__.select().where(Exercise.name == ex_name)
                )
                if not existing:
                    session.add(
                        Exercise(
                            name=ex_name,
                            type_id=type_map[ex_type],
                            description=f"A popular {ex_type.lower()} exercise: {ex_name}.",
                            video_url=f"https://example.com/videos/{ex_name.replace(' ', '_').lower()}",
                            is_custom=False,
                        )
                    )

        await session.commit()
        print("✅ Seed data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(seed_exercises())
