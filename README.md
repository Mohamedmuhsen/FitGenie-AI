# FitGenie AI — Multi-Agent AI Fitness Platform

![Python Version](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-1.15.9-FFD60A?style=for-the-badge)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-6366F1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

FitGenie AI is a production-grade, multi-agent AI fitness platform built with **CrewAI**, **FastAPI**, **OpenRouter (Meta Llama 3.3 70B / Claude 3.5 Sonnet)**, and an interactive **React Native & Web UI**.

Unlike basic wrappers that guess nutritional data, FitGenie AI separates **deterministic calculations** (BMR via Mifflin-St Jeor, TDEE, BMI, macro splits, and time-series progress metrics executed strictly in Python) from **AI agent reasoning** (personalized routine design, biomechanical injury risk analysis, supplement protocols, healthy dining options, and mindset coaching).

---

## 📸 Preview

```
+-----------------------------------------------------------------------------------+
|                                  FITGENIE AI                                      |
|                 Your AI-Powered Personal Fitness Coach                             |
|                                                                                   |
|  [ Start Your Fitness Journey ]                      [ Learn More ]               |
|                                                                                   |
|  +-------------------+  +-------------------+  +-------------------+              |
|  | Workout Planning  |  | Nutrition & Meals |  | Supplement Advice |              |
|  +-------------------+  +-------------------+  +-------------------+              |
+-----------------------------------------------------------------------------------+
```

> *Placeholder: Screenshots and interactive demonstration GIFs will be showcased here.*

---

## ⚡ Implemented Features

- **Multi-Agent Orchestration:** 10 specialized CrewAI agents working sequentially or standalone to analyze profiles and build complete programs.
- **Deterministic Math Engine:** Pure Python `CalculatorService` for 100% accurate BMR, TDEE, BMI, daily calorie targets, and macro distribution.
- **Presentation Layer Formatter:** `ResponseFormatterService` converts raw internal JSON into clean, emoji-free Markdown formatted for React Native & Web UIs.
- **Multi-Step Onboarding Wizard:** 8-step interactive assessment flow covering demographics, measurements, goals, experience, schedule, diet, injuries, and budget.
- **Dynamic Results Dashboard:** Expandable, dark-themed result cards (`#0D0D0D` theme) for Workout Plans, Meal Protocols, Supplements, Injury Safety, Shopping, and Restaurants.
- **Async Event Loop Execution:** Native `crew.kickoff_async()` integration ensuring zero event-loop blocking inside FastAPI.
- **API Key Masking & Security:** Automatic credential detection and masking (`sk-or-v1-3c4f...08d1`) preventing accidental log exposure.

---

## 🤖 AI Multi-Agent Architecture

FitGenie AI features a team of specialized AI agents managed by an Orchestrator.

```
                         +------------------------+
                         |  Fitness Orchestrator  |
                         +-----------+------------+
                                     |
    +------------------+-------------+-------------+------------------+
    |                  |                           |                  |
+---v----+         +---v----+                  +---v----+         +---v----+
| Workout|         |Nutritn |                  |Injuries|         |Progress|
| Agent  |         | Agent  |                  | Agent  |         | Agent  |
+--------+         +--------+                  +--------+         +--------+
```

### Agent Roster Breakdown

| Agent Name | Role & Purpose | Input Payload | Output Delivered |
|---|---|---|---|
| **Fitness Orchestrator** | Intent classification & crew routing | User query string | Formatted synthesized response |
| **Fitness Assessment Specialist** | Physical stat analysis & health metrics | Demographic JSON (Age, Weight, Height, Goal) | BMR, TDEE, BMI, Macros & Risk Factors |
| **Workout Planning Specialist** | Multi-day progressive workout design | Goal, Experience, Days/Week, Injuries | Structured multi-day program with Warmup/Cooldown |
| **Nutrition Planning Specialist** | Daily meal plan & macro target matching | Calorie Target, Goal, Dietary Preference | Daily meal schedule with protein/carb/fat breakdown |
| **Supplement Advisor** | Evidence-based supplement recommendations | Goal, Diet, Health Profile | Prioritized supplement regimen with dosages & timing |
| **Injury Prevention Specialist** | Biomechanical risk auditing & exercise safety | Injury History, Workout Plan | Flagged exercises, safer alternatives & form cues |
| **Progress Analyst** | Body weight & workout consistency trend analysis | Current/Previous Weight, Completed Workouts | Trend status, consistency %, program adjustments |
| **Motivation Coach** | Context-aware mental performance coaching | Progress metrics, Goal adherence | Personalized performance coaching message |
| **Fitness Shopping Advisor** | Gym gear & equipment recommendations | Gear query, Budget preference | Recommended apparel/equipment with price estimates |
| **Healthy Restaurant Advisor** | Location-aware healthy dining discovery | Geo-location, Search query | Nearby healthy restaurants with recommended meals |

---

## 💻 Tech Stack

- **Backend:** Python 3.12, FastAPI 0.115, Uvicorn 0.32, Pydantic v2
- **Agentic Framework:** CrewAI 1.15.9, LiteLLM
- **LLM Model:** OpenRouter API (`openrouter/meta-llama/llama-3.3-70b-instruct` / `openrouter/anthropic/claude-3.5-sonnet`)
- **Frontend:** HTML5, Dark Design System CSS3, Vanilla ES6 JavaScript
- **Config & Security:** `python-dotenv`, Pydantic Settings

---

## 📁 Folder Structure

```
fitgenie-ai/
├── app/
│   ├── agents/                     # CrewAI Agent Definitions (10 specialized agents)
│   │   ├── assessment_agent.py
│   │   ├── injury_prevention_agent.py
│   │   ├── motivation_agent.py
│   │   ├── nutrition_agent.py
│   │   ├── orchestrator_agent.py
│   │   ├── progress_agent.py
│   │   ├── restaurant_agent.py
│   │   ├── shopping_agent.py
│   │   ├── supplement_agent.py
│   │   └── workout_agent.py
│   ├── config/                     # Configuration Layer & Settings
│   │   ├── llm_config.py           # Centralized CrewAI LLM Factory
│   │   └── settings.py             # Pydantic Settings & dotenv loader
│   ├── crews/                      # Crew Assembly Factories
│   │   └── fitness_crew.py
│   ├── schemas/                    # Pydantic Input/Output Validation Schemas
│   │   ├── assessment.py
│   │   ├── chat.py
│   │   ├── nutrition.py
│   │   ├── progress.py
│   │   ├── restaurant.py
│   │   ├── shopping.py
│   │   ├── supplement.py
│   │   └── workout.py
│   ├── services/                   # Business Logic & Core Services
│   │   ├── agent_runner.py         # Async Crew Execution & Telemetry Engine
│   │   ├── calculator_service.py   # Pure Python Deterministic Math Engine
│   │   ├── orchestrator_service.py # Query Classification & Routing
│   │   └── response_formatter_service.py # Presentation Layer Formatter
│   ├── static/                     # Web Dashboard UI
│   │   └── index.html
│   ├── tasks/                      # CrewAI Task Definitions (10 domain tasks)
│   ├── tools/                      # BaseTool Knowledge Wrappers (6 domain tools)
│   └── main.py                     # FastAPI Application Routes & Lifespan
├── .env.example                    # Environment variable template
├── .gitignore                      # Security exclusions (.env, __pycache__)
├── README.md                       # Documentation
├── requirements.txt                # Python Dependencies
└── test_all_scenarios.py           # End-to-End Test Suite
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Mohamedmuhsen/FitGenie-AI.git
cd FitGenie-AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your **OpenRouter API Key**:
```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
LLM_MODEL=openrouter/meta-llama/llama-3.3-70b-instruct
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_TEMPERATURE=0.7
LLM_TIMEOUT=60
HOST=0.0.0.0
PORT=8005
DEBUG=true
```

### 5. Launch Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

- **Web Dashboard:** Access at [http://localhost:8005](http://localhost:8005)
- **Swagger Documentation:** Access at [http://localhost:8005/docs](http://localhost:8005/docs)

---

## 🔑 Environment Variables

| Variable | Description | Default / Example | Required |
|---|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API Key for Agent LLM reasoning | `sk-or-v1-...` | **Yes** |
| `LLM_MODEL` | OpenRouter Model identifier | `openrouter/meta-llama/llama-3.3-70b-instruct` | **Yes** |
| `LLM_BASE_URL` | OpenRouter Base URL | `https://openrouter.ai/api/v1` | **Yes** |
| `LLM_TEMPERATURE` | Model temperature (0.0 to 1.0) | `0.7` | No |
| `LLM_TIMEOUT` | LLM call timeout in seconds | `60` | No |
| `TAVILY_API_KEY` | Tavily Web Search Key *(Placeholder)* | `tvly-placeholder` | No |
| `GOOGLE_MAPS_API_KEY` | Google Maps API Key *(Placeholder)* | `google-maps-placeholder` | No |
| `HOST` | Server bind host | `0.0.0.0` | No |
| `PORT` | Server bind port | `8005` | No |

---

## 📖 Usage Guide

1. **Home Screen:** Review platform capabilities and click **"Start Your Fitness Journey"**.
2. **Assessment Wizard:** Complete the 8-step wizard entering Age, Weight, Height, Goal, Experience, Days/Week, Injuries, and Budget.
3. **AI Processing:** Watch real-time execution as specialized agents generate program components.
4. **Results Dashboard:** Toggle expandable cards for Workout Plans, Meal Schedules, Supplement Regimens, Injury Precautions, Progress Metrics, and Gear.
5. **AI Chat Coach:** Switch to the **AI Chat** tab to ask open-ended questions (*"How do I substitute overhead press?"*).

---

## 📡 API Endpoints Table

| Method | Endpoint Path | Request Body | Description |
|---|---|---|---|
| `GET` | `/` | None | Serves interactive Web Dashboard UI |
| `GET` | `/health` | None | Health check endpoint returning `{"status": "healthy"}` |
| `GET` | `/api` | None | System status and API key configuration metadata |
| `POST` | `/chat` | `{"message": "..."}` | Routes queries to Orchestrator Agent |
| `POST` | `/assessment` | `AssessmentInput` JSON | Computes BMR, TDEE, BMI, Macros, and risk factors |
| `POST` | `/workout` | Assessment profile JSON | Generates multi-day progressive workout plan |
| `POST` | `/nutrition` | Assessment profile JSON | Generates daily meal schedule matching macro targets |
| `POST` | `/supplements` | Assessment profile JSON | Recommends prioritized supplement protocol |
| `POST` | `/shopping` | `{"query": "shoes"}` | Recommends fitness equipment & gear |
| `POST` | `/restaurants` | `{"location": "NY"}` | Discovers healthy restaurant dining options |
| `POST` | `/progress` | Progress metrics JSON | Analyzes weight trends and consistency |

---

## 🗺️ Future Roadmap

- [ ] **ChromaDB Vector Integration:** Implement ChromaDB for semantic search across exercise and food databases.
- [ ] **PostgreSQL Persistence:** Migrate profile storage and workout history from transient memory to PostgreSQL.
- [ ] **JWT Authentication:** Add user registration, login, and JWT access token verification.
- [ ] **Redis Caching Layer:** Cache frequent agent crew responses for 0ms latency on common queries.
- [ ] **Docker Containerization:** Add multi-stage Dockerfile and Docker Compose orchestration.
- [ ] **React Native Mobile App:** Package native iOS/Android mobile clients interfacing with FastAPI endpoints.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

## 👤 Author

**Mohamed Mohsen**
- **GitHub:** [@Mohamedmuhsen](https://github.com/Mohamedmuhsen)
- **Repository:** [FitGenie AI on GitHub](https://github.com/Mohamedmuhsen/FitGenie-AI)
- **Email:** mohummedmohsen24@gmail.com
