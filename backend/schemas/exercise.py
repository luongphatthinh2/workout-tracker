# schemas/exercise.py
from pydantic import BaseModel

class ExerciseWithType(BaseModel):
    exercise_name: str
    description: str | None
    video_url: str | None
    exercise_type_name: str

    class Config:
        orm_mode = True  # needed to serialize from SQLAlchemy results