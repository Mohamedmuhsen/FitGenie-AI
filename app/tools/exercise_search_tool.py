import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ExerciseSearchInput(BaseModel):
    """Input schema for ExerciseSearchTool."""
    query: str = Field(..., description="Muscle group, exercise name, or goal to search for.")
    experience_level: str = Field('intermediate', description="Experience level (e.g., 'beginner', 'intermediate', 'advanced').")
    equipment: str = Field('full_gym', description="Available equipment (e.g., 'none', 'dumbbells', 'full_gym').")

class ExerciseSearchTool(BaseTool):
    name: str = "Exercise Search Tool"
    description: str = "Searches for appropriate exercises based on muscle group, goal, equipment, and experience level."
    args_schema: type[BaseModel] = ExerciseSearchInput

    def _run(self, query: str, experience_level: str = 'intermediate', equipment: str = 'full_gym', **kwargs) -> str:
        # TODO: Replace with ChromaDB vector search in production
        
        # Hardcoded dictionary of exercises organized by muscle group
        exercises = [
            {"name": "bench press", "muscle_group": "chest", "equipment": "barbell", "difficulty": "intermediate", "description": "Lying on a bench, press the barbell upwards.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            {"name": "incline dumbbell press", "muscle_group": "chest", "equipment": "dumbbells", "difficulty": "intermediate", "description": "Press dumbbells upwards on an incline bench.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            {"name": "cable flyes", "muscle_group": "chest", "equipment": "cables", "difficulty": "beginner", "description": "Bring cables together in a hugging motion.", "sets_recommended": "3", "reps_recommended": "10-15"},
            {"name": "push-ups", "muscle_group": "chest", "equipment": "none", "difficulty": "beginner", "description": "Classic bodyweight push-up.", "sets_recommended": "3", "reps_recommended": "to failure"},
            {"name": "dips", "muscle_group": "chest", "equipment": "dip station", "difficulty": "intermediate", "description": "Lower and raise your body on parallel bars.", "sets_recommended": "3", "reps_recommended": "8-12"},
            
            {"name": "pull-ups", "muscle_group": "back", "equipment": "pull-up bar", "difficulty": "intermediate", "description": "Pull your body up to the bar.", "sets_recommended": "3-4", "reps_recommended": "8-10"},
            {"name": "barbell rows", "muscle_group": "back", "equipment": "barbell", "difficulty": "intermediate", "description": "Row the barbell to your stomach while bent over.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            {"name": "lat pulldown", "muscle_group": "back", "equipment": "machine", "difficulty": "beginner", "description": "Pull the cable bar down to your chest.", "sets_recommended": "3-4", "reps_recommended": "10-12"},
            {"name": "seated cable row", "muscle_group": "back", "equipment": "machine", "difficulty": "beginner", "description": "Row the cable handle to your torso while seated.", "sets_recommended": "3-4", "reps_recommended": "10-12"},
            {"name": "deadlift", "muscle_group": "back", "equipment": "barbell", "difficulty": "advanced", "description": "Lift the barbell from the floor to standing position.", "sets_recommended": "3-4", "reps_recommended": "5-8"},
            
            {"name": "overhead press", "muscle_group": "shoulders", "equipment": "barbell", "difficulty": "intermediate", "description": "Press the barbell overhead from the shoulders.", "sets_recommended": "3-4", "reps_recommended": "8-10"},
            {"name": "lateral raises", "muscle_group": "shoulders", "equipment": "dumbbells", "difficulty": "beginner", "description": "Raise dumbbells out to the sides.", "sets_recommended": "3-4", "reps_recommended": "12-15"},
            {"name": "face pulls", "muscle_group": "shoulders", "equipment": "cables", "difficulty": "beginner", "description": "Pull the rope attachment to your face.", "sets_recommended": "3-4", "reps_recommended": "12-15"},
            {"name": "front raises", "muscle_group": "shoulders", "equipment": "dumbbells", "difficulty": "beginner", "description": "Raise dumbbells straight out in front.", "sets_recommended": "3", "reps_recommended": "10-12"},
            
            {"name": "squats", "muscle_group": "legs", "equipment": "barbell", "difficulty": "intermediate", "description": "Squat down and up with the barbell on your upper back.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            {"name": "leg press", "muscle_group": "legs", "equipment": "machine", "difficulty": "beginner", "description": "Press the platform away with your legs.", "sets_recommended": "3-4", "reps_recommended": "10-12"},
            {"name": "Romanian deadlifts", "muscle_group": "legs", "equipment": "barbell", "difficulty": "intermediate", "description": "Hinge at the hips keeping legs mostly straight.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            {"name": "lunges", "muscle_group": "legs", "equipment": "dumbbells", "difficulty": "beginner", "description": "Step forward into a lunge and push back.", "sets_recommended": "3", "reps_recommended": "10-12 per leg"},
            {"name": "leg curls", "muscle_group": "legs", "equipment": "machine", "difficulty": "beginner", "description": "Curl your legs against resistance.", "sets_recommended": "3-4", "reps_recommended": "10-15"},
            {"name": "leg extensions", "muscle_group": "legs", "equipment": "machine", "difficulty": "beginner", "description": "Extend your legs against resistance.", "sets_recommended": "3-4", "reps_recommended": "10-15"},
            {"name": "calf raises", "muscle_group": "legs", "equipment": "machine", "difficulty": "beginner", "description": "Raise up on your toes.", "sets_recommended": "3-4", "reps_recommended": "15-20"},
            
            {"name": "barbell curls", "muscle_group": "arms", "equipment": "barbell", "difficulty": "beginner", "description": "Curl the barbell up to your chest.", "sets_recommended": "3", "reps_recommended": "10-12"},
            {"name": "tricep pushdowns", "muscle_group": "arms", "equipment": "cables", "difficulty": "beginner", "description": "Push the cable attachment down.", "sets_recommended": "3", "reps_recommended": "10-12"},
            {"name": "hammer curls", "muscle_group": "arms", "equipment": "dumbbells", "difficulty": "beginner", "description": "Curl dumbbells with a neutral grip.", "sets_recommended": "3", "reps_recommended": "10-12"},
            {"name": "skull crushers", "muscle_group": "arms", "equipment": "EZ bar", "difficulty": "intermediate", "description": "Lower the bar to your forehead and extend.", "sets_recommended": "3-4", "reps_recommended": "8-12"},
            
            {"name": "planks", "muscle_group": "core", "equipment": "none", "difficulty": "beginner", "description": "Hold a push-up position on your forearms.", "sets_recommended": "3", "reps_recommended": "30-60 sec"},
            {"name": "hanging leg raises", "muscle_group": "core", "equipment": "pull-up bar", "difficulty": "intermediate", "description": "Hang from a bar and raise your legs.", "sets_recommended": "3", "reps_recommended": "10-15"},
            {"name": "cable crunches", "muscle_group": "core", "equipment": "cables", "difficulty": "beginner", "description": "Crunch down holding a cable rope.", "sets_recommended": "3-4", "reps_recommended": "12-15"},
            {"name": "Russian twists", "muscle_group": "core", "equipment": "medicine ball", "difficulty": "beginner", "description": "Twist your torso side to side while seated.", "sets_recommended": "3", "reps_recommended": "20 total"}
        ]
        
        query_lower = query.lower()
        results = [
            ex for ex in exercises 
            if query_lower in ex["name"].lower() or query_lower in ex["muscle_group"].lower()
        ]
        
        return json.dumps(results)
