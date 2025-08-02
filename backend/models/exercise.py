from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from db.init_db import Base


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    exercise_name = Column(String(255), unique=True, nullable=False)
    type_id = Column(ForeignKey("exercise_types.id"), nullable=True)
    description = Column(Text)
    video_url = Column(String(512))
    is_custom = Column(Boolean, default=False)
    # Relationship to ExerciseType
    type = relationship("ExerciseType", back_populates="exercises")

class ExerciseType(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True, index=True)
    exercise_type_name = Column(String(100), unique=True, nullable=False)
    #  Relationship to Exercise
    exercises = relationship("Exercise", back_populates="type")
