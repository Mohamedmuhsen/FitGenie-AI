"""
Task factory exports.
"""
from app.tasks.assessment_task import create_assessment_task
from app.tasks.workout_task import create_workout_task
from app.tasks.nutrition_task import create_nutrition_task
from app.tasks.supplement_task import create_supplement_task
from app.tasks.injury_prevention_task import create_injury_prevention_task
from app.tasks.progress_task import create_progress_task
from app.tasks.motivation_task import create_motivation_task
from app.tasks.shopping_task import create_shopping_task
from app.tasks.restaurant_task import create_restaurant_task

__all__ = [
    "create_assessment_task",
    "create_workout_task",
    "create_nutrition_task",
    "create_supplement_task",
    "create_injury_prevention_task",
    "create_progress_task",
    "create_motivation_task",
    "create_shopping_task",
    "create_restaurant_task",
]
