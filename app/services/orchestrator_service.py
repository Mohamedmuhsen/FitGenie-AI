"""
Orchestrator Service — Main entry point for processing user messages.

Classifies user intent via keyword matching and routes to the appropriate
CrewAI agents and tasks. Each intent maps to a specific agent-task pair
with correct argument signatures.

Architecture:
    User Message → classify_intent() → build agents/tasks → Crew.kickoff() → ChatResponse
"""

import json
import logging
from typing import Any

from crewai import Crew, Process, Agent, Task
from app.config.settings import get_settings
from app.schemas.chat import ChatResponse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Intent keyword map — each key is an intent, each value is a list of
# trigger keywords.  Checked via substring match on the lowercased message.
# ---------------------------------------------------------------------------
INTENT_KEYWORDS: dict[str, list[str]] = {
    "workout": ["workout", "exercise", "training", "gym routine"],
    "nutrition": ["nutrition", "meal", "diet", "food", "eat", "calorie"],
    "supplement": ["supplement", "vitamin", "protein powder", "creatine"],
    "injury_prevention": ["injury", "pain", "hurt", "safe", "risk"],
    "progress": ["progress", "track", "weight change", "body"],
    "motivation": ["motivat", "inspire", "encourage"],
    "shopping": ["shop", "buy", "equipment", "clothes", "gear"],
    "restaurant": ["restaurant", "eat out", "food near", "healthy place"],
    "assessment": ["assess", "profile", "start", "about me", "my info"],
}


class OrchestratorService:
    """Routes user messages to the correct CrewAI agents based on intent."""

    def __init__(self) -> None:
        self.settings = get_settings()

    # ------------------------------------------------------------------
    # Intent classification (deterministic keyword match — no LLM call)
    # ------------------------------------------------------------------
    def classify_intent(self, message: str) -> list[str]:
        """Return a list of matched intent strings from the user message."""
        message_lower = message.lower()
        intents: list[str] = []

        for intent, keywords in INTENT_KEYWORDS.items():
            if any(kw in message_lower for kw in keywords):
                intents.append(intent)

        return intents if intents else ["general"]

    # ------------------------------------------------------------------
    # Build (agent, task) for a single intent
    # ------------------------------------------------------------------
    def _build_agent_task(
        self, intent: str, context_str: str
    ) -> tuple[Agent, Task] | None:
        """Create the agent + task pair for a given intent."""
        from app.agents.workout_agent import create_workout_agent
        from app.agents.nutrition_agent import create_nutrition_agent
        from app.agents.supplement_agent import create_supplement_agent
        from app.agents.injury_prevention_agent import create_injury_prevention_agent
        from app.agents.progress_agent import create_progress_agent
        from app.agents.motivation_agent import create_motivation_agent
        from app.agents.shopping_agent import create_shopping_agent
        from app.agents.restaurant_agent import create_restaurant_agent
        from app.agents.assessment_agent import create_assessment_agent

        from app.tasks.workout_task import create_workout_task
        from app.tasks.nutrition_task import create_nutrition_task
        from app.tasks.supplement_task import create_supplement_task
        from app.tasks.injury_prevention_task import create_injury_prevention_task
        from app.tasks.progress_task import create_progress_task
        from app.tasks.motivation_task import create_motivation_task
        from app.tasks.shopping_task import create_shopping_task
        from app.tasks.restaurant_task import create_restaurant_task
        from app.tasks.assessment_task import create_assessment_task

        # fmt: off
        if intent == "workout":
            agent = create_workout_agent()
            task  = create_workout_task(agent, context_str)
        elif intent == "nutrition":
            agent = create_nutrition_agent()
            task  = create_nutrition_task(agent, context_str, "")
        elif intent == "supplement":
            agent = create_supplement_agent()
            task  = create_supplement_task(agent, context_str, "", "")
        elif intent == "injury_prevention":
            agent = create_injury_prevention_agent()
            task  = create_injury_prevention_task(agent, context_str, "{}")
        elif intent == "progress":
            agent = create_progress_agent()
            task  = create_progress_task(agent, context_str)
        elif intent == "motivation":
            agent = create_motivation_agent()
            task  = create_motivation_task(agent, context_str)
        elif intent == "shopping":
            agent = create_shopping_agent()
            task  = create_shopping_task(agent, context_str)
        elif intent == "restaurant":
            agent = create_restaurant_agent()
            task  = create_restaurant_task(agent, context_str)
        elif intent == "assessment":
            agent = create_assessment_agent()
            task  = create_assessment_task(agent, context_str)
        else:
            return None
        # fmt: on
        return agent, task

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    async def process_message(
        self, message: str, user_context: dict | None = None
    ) -> ChatResponse:
        """Process a user message end-to-end through the multi-agent system."""
        try:
            intents = self.classify_intent(message)
            context_str = json.dumps(user_context, indent=2) if user_context else "{}"

            agents: list[Agent] = []
            tasks: list[Task] = []

            if "general" in intents:
                # Fallback: lightweight agent that responds conversationally
                general_agent = Agent(
                    role="General Fitness Assistant",
                    goal="Help the user with general fitness queries in a friendly, knowledgeable manner.",
                    backstory=(
                        "You are the friendly front-desk assistant for FitGenie AI, "
                        "a comprehensive fitness platform. You can answer general "
                        "fitness questions, explain how the platform works, and "
                        "guide users to the right specialized features."
                    ),
                    llm=self.settings.LLM_MODEL,
                    allow_delegation=False,
                    verbose=True,
                )
                general_task = Task(
                    description=(
                        f"Respond helpfully to the user's message:\n\n"
                        f"\"{message}\"\n\n"
                        f"User context: {context_str}"
                    ),
                    expected_output="A helpful, friendly, and informative response.",
                    agent=general_agent,
                )
                agents.append(general_agent)
                tasks.append(general_task)
            else:
                for intent in intents:
                    result = self._build_agent_task(intent, context_str)
                    if result:
                        agent, task = result
                        agents.append(agent)
                        tasks.append(task)

            if not agents:
                return ChatResponse(
                    response="I couldn't determine how to help. Try asking about workouts, nutrition, or supplements!",
                    agents_used=[],
                    data=None,
                )

            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True,
                process=Process.sequential,
            )

            from app.services.agent_runner import AgentRunner
            primary_intent = intents[0] if intents else "general"
            payload = user_context or {"message": message}
            
            res = AgentRunner.execute_crew(primary_intent, crew, payload)
            
            output_text = res.get("output")
            if isinstance(output_text, dict):
                output_str = json.dumps(output_text, indent=2)
            else:
                output_str = str(output_text)

            return ChatResponse(
                response=output_str,
                agents_used=intents,
                data=res if isinstance(res, dict) else None,
            )

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return ChatResponse(
                response=f"I'm sorry, I encountered an error while processing your request: {str(e)}",
                agents_used=[],
                data=None,
            )
