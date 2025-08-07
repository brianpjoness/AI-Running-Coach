"""
AI Running Training Plan Generator

A scientific, evidence-based training plan generator that follows the principles
outlined in the .cursorrules file, including periodization, progressive overload,
and injury prevention.
"""

from .models import (
    RunnerProfile, TrainingPlan, TrainingWeek, Workout,
    RaceDistance, ExperienceLevel, TrainingZone, WorkoutType, TrainingPhase
)
from .plan_generator import TrainingPlanGenerator
from .formatter import TrainingPlanFormatter

__version__ = "1.0.0"
__author__ = "AI Running Coach"

__all__ = [
    "RunnerProfile",
    "TrainingPlan", 
    "TrainingWeek",
    "Workout",
    "RaceDistance",
    "ExperienceLevel", 
    "TrainingZone",
    "WorkoutType",
    "TrainingPhase",
    "TrainingPlanGenerator",
    "TrainingPlanFormatter"
]
