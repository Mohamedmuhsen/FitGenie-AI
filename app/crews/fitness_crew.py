"""
Fitness crew module for defining multi-agent domains.
"""
from crewai import Crew, Process
from app.agents import (
    create_assessment_agent, create_workout_agent, create_nutrition_agent,
    create_supplement_agent, create_injury_prevention_agent, create_progress_agent,
    create_motivation_agent, create_shopping_agent, create_restaurant_agent,
    create_orchestrator_agent
)
from app.tasks import (
    create_assessment_task, create_workout_task, create_nutrition_task,
    create_supplement_task, create_injury_prevention_task, create_progress_task,
    create_motivation_task, create_shopping_task, create_restaurant_task
)
import json

class FitnessCrew:
    """Factory for creating domain-specific CrewAI crews.
    
    Each method creates a focused crew with only the agents and tasks
    needed for that specific domain. This keeps execution efficient
    and prevents unnecessary LLM calls.
    """
    
    @staticmethod
    def assessment_crew(input_data: dict) -> Crew:
        agent = create_assessment_agent()
        task = create_assessment_task(agent, json.dumps(input_data, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def workout_crew(assessment_data: dict) -> Crew:
        agent = create_workout_agent()
        task = create_workout_task(agent, json.dumps(assessment_data, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def nutrition_crew(assessment_data: dict, workout_data: dict = None) -> Crew:
        agent = create_nutrition_agent()
        task = create_nutrition_task(
            agent,
            json.dumps(assessment_data, indent=2),
            json.dumps(workout_data, indent=2) if workout_data else ""
        )
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def supplement_crew(assessment_data: dict, nutrition_data: dict = None, workout_data: dict = None) -> Crew:
        agent = create_supplement_agent()
        task = create_supplement_task(
            agent,
            json.dumps(assessment_data, indent=2),
            json.dumps(nutrition_data, indent=2) if nutrition_data else "",
            json.dumps(workout_data, indent=2) if workout_data else ""
        )
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def injury_prevention_crew(assessment_data: dict, workout_data: dict) -> Crew:
        agent = create_injury_prevention_agent()
        task = create_injury_prevention_task(
            agent,
            json.dumps(assessment_data, indent=2),
            json.dumps(workout_data, indent=2)
        )
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def progress_crew(progress_data: dict) -> Crew:
        agent = create_progress_agent()
        task = create_progress_task(agent, json.dumps(progress_data, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def motivation_crew(progress_data: dict) -> Crew:
        agent = create_motivation_agent()
        task = create_motivation_task(agent, json.dumps(progress_data, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def shopping_crew(user_preferences: dict) -> Crew:
        agent = create_shopping_agent()
        task = create_shopping_task(agent, json.dumps(user_preferences, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def restaurant_crew(location_data: dict) -> Crew:
        agent = create_restaurant_agent()
        task = create_restaurant_task(agent, json.dumps(location_data, indent=2))
        return Crew(agents=[agent], tasks=[task], verbose=True, process=Process.sequential)
    
    @staticmethod
    def full_plan_crew(assessment_data: dict) -> Crew:
        """Creates a comprehensive crew that runs assessment -> workout -> nutrition -> supplements sequentially."""
        assessment_agent = create_assessment_agent()
        workout_agent = create_workout_agent()
        nutrition_agent = create_nutrition_agent()
        supplement_agent = create_supplement_agent()
        injury_agent = create_injury_prevention_agent()
        
        assessment_str = json.dumps(assessment_data, indent=2)
        
        assessment_task = create_assessment_task(assessment_agent, assessment_str)
        workout_task = create_workout_task(workout_agent, assessment_str)
        injury_task = create_injury_prevention_task(injury_agent, assessment_str, '{}')
        nutrition_task = create_nutrition_task(nutrition_agent, assessment_str)
        supplement_task = create_supplement_task(supplement_agent, assessment_str)
        
        # Set task context so downstream tasks can reference upstream outputs
        workout_task.context = [assessment_task]
        injury_task.context = [assessment_task, workout_task]
        nutrition_task.context = [assessment_task, workout_task]
        supplement_task.context = [assessment_task, nutrition_task, workout_task]
        
        return Crew(
            agents=[assessment_agent, workout_agent, injury_agent, nutrition_agent, supplement_agent],
            tasks=[assessment_task, workout_task, injury_task, nutrition_task, supplement_task],
            verbose=True,
            process=Process.sequential,
        )
