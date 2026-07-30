"""
Orchestrator Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm

def create_orchestrator_agent() -> Agent:
    return Agent(
        role="Fitness Orchestrator",
        goal="Understand user fitness requests, determine which specialized agents should handle them, and synthesize their outputs into clear, actionable responses.",
        backstory="You are the lead coordinator of a team of fitness AI specialists. You analyze user requests, route them to the right specialist agents, and compile their structured outputs into friendly, comprehensive responses. You never perform domain-specific calculations or recommendations yourself — you delegate to specialists and present their findings.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[],
    )
