# 🏋️ FitGenie AI

> AI-powered Multi-Agent Fitness Platform built with **CrewAI + FastAPI**

FitGenie AI is an intelligent fitness assistant composed of **10 specialized AI agents** that collaborate through an orchestrator. Instead of one giant model doing everything, each agent owns a single responsibility — workout planning, nutrition, supplements, injury prevention, and more.

---

## Architecture

```
User Request
     │
     ▼
  FastAPI (/chat, /workout, /nutrition, ...)
     │
     ▼
  Orchestrator Service
     │  ← Keyword-based intent classification (no LLM)
     ▼
  ┌─────────────────────────────────────────────────┐
  │           CrewAI Crew (Sequential)              │
  │                                                 │
  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
  │  │Assessment│  │ Workout  │  │  Nutrition    │  │
  │  │  Agent   │  │  Agent   │  │    Agent      │  │
  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
  │       │             │               │           │
  │  ┌────┴─────┐  ┌────┴─────┐  ┌──────┴───────┐  │
  │  │Calculator│  │ Exercise │  │  Nutrition    │  │
  │  │  Tool    │  │  Search  │  │   Search      │  │
  │  └──────────┘  └──────────┘  └──────────────┘  │
  └─────────────────────────────────────────────────┘
     │
     ▼
  Structured JSON Response → User
```

---

## Agents

| # | Agent | Responsibility | Tools |
|---|-------|---------------|-------|
| 1 | **Orchestrator** | Routes requests to the right agents | None (delegates) |
| 2 | **Assessment** | Collects user data, calculates health metrics | Calculator |
| 3 | **Workout** | Designs personalized training programs | Exercise Search, Calculator |
| 4 | **Nutrition** | Creates meal plans matching macro targets | Nutrition Search, Calculator |
| 5 | **Supplement** | Evidence-based supplement recommendations | Nutrition Search |
| 6 | **Injury Prevention** | Flags risky exercises, suggests alternatives | Exercise Search |
| 7 | **Progress** | Analyzes body metrics and workout consistency | Progress Analytics, Calculator |
| 8 | **Motivation** | Personalized encouragement based on data | Progress Analytics |
| 9 | **Shopping** | Recommends gym gear and equipment | Shopping Search |
| 10 | **Restaurant** | Finds healthy restaurants nearby | Google Maps |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | CrewAI |
| API | FastAPI |
| LLM | OpenRouter (any model) |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Quick Start

### 1. Clone & Install

```bash
cd "d:\AI GYM AGENTS\fitgenie-ai"
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy .env.example .env
# Edit .env and add your OpenRouter API key
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

OpenAPI docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Input | Description |
|--------|----------|-------|-------------|
| GET | `/` | — | Welcome / status |
| GET | `/health` | — | Health check |
| POST | `/chat` | `ChatRequest` | Main conversational endpoint (auto-routes to agents) |
| POST | `/assessment` | `AssessmentInput` | User profile + calculated metrics |
| POST | `/workout` | `dict` (assessment data) | Workout plan generation |
| POST | `/nutrition` | `dict` (assessment data) | Nutrition plan generation |
| POST | `/supplements` | `dict` (assessment + optional nutrition/workout) | Supplement recommendations |
| POST | `/shopping` | `dict` (user preferences) | Gym gear recommendations |
| POST | `/restaurants` | `dict` (location data) | Healthy restaurant recommendations |
| POST | `/progress` | `ProgressInput` | Progress tracking + motivation |

---

## Example Requests

### Chat (Auto-routing)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a workout plan for muscle gain"}'
```

### Assessment
```bash
curl -X POST http://localhost:8000/assessment \
  -H "Content-Type: application/json" \
  -d '{
    "age": 28,
    "gender": "male",
    "weight_kg": 75,
    "height_cm": 178,
    "goal": "muscle_gain",
    "experience_level": "intermediate",
    "budget": "medium",
    "workout_days_per_week": 4,
    "injuries": ["lower_back"],
    "diseases": []
  }'
```

### Progress Tracking
```bash
curl -X POST http://localhost:8000/progress \
  -H "Content-Type: application/json" \
  -d '{
    "current_weight_kg": 76.5,
    "previous_weight_kg": 75.0,
    "goal": "muscle_gain",
    "weeks_active": 6,
    "workouts_completed": 20,
    "workouts_planned": 24
  }'
```

---

## Design Principles

- **Zero-LLM Math** — All calculations (BMR, TDEE, BMI, macros) are done by `CalculatorService` in pure Python
- **Structured Communication** — Agents exchange Pydantic models, never free text
- **Single Responsibility** — Each agent does one thing well
- **Tool-Based Reasoning** — Agents use tools instead of hallucinating
- **Deterministic Routing** — Intent classification is keyword-based (no LLM overhead)

---

## Project Structure

```
app/
├── main.py              # FastAPI application
├── config/
│   └── settings.py      # Pydantic Settings
├── schemas/             # Pydantic I/O models
│   ├── assessment.py
│   ├── workout.py
│   ├── nutrition.py
│   ├── supplement.py
│   ├── progress.py
│   ├── restaurant.py
│   ├── shopping.py
│   └── chat.py
├── services/
│   ├── calculator_service.py     # Deterministic math (NO LLM)
│   └── orchestrator_service.py   # Intent classification + routing
├── tools/               # CrewAI Tools (placeholder data for MVP)
│   ├── calculator_tool.py
│   ├── exercise_search_tool.py
│   ├── nutrition_search_tool.py
│   ├── google_maps_tool.py
│   ├── shopping_search_tool.py
│   └── progress_analytics_tool.py
├── agents/              # CrewAI Agent definitions
│   ├── orchestrator_agent.py
│   ├── assessment_agent.py
│   ├── workout_agent.py
│   ├── nutrition_agent.py
│   ├── supplement_agent.py
│   ├── injury_prevention_agent.py
│   ├── progress_agent.py
│   ├── motivation_agent.py
│   ├── shopping_agent.py
│   └── restaurant_agent.py
├── tasks/               # CrewAI Task definitions
│   └── (one per agent)
└── crews/
    └── fitness_crew.py  # Crew factory with domain-specific methods
```

---

## Future Production Enhancements

- [ ] PostgreSQL for persistent storage
- [ ] ChromaDB + RAG for exercise/nutrition knowledge
- [ ] Redis for caching and job queues
- [ ] JWT authentication
- [ ] React Native mobile app
- [ ] AgentOps / Langfuse monitoring
- [ ] Docker Compose deployment
- [ ] Google Maps API integration
- [ ] Tavily Search API integration

---

> **Note:** This is an MVP demo showcasing the multi-agent architecture. All tools use placeholder data. Replace TODO markers with real implementations for production.
