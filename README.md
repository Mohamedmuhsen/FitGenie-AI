# FitGenie AI — Multi-Agent AI Fitness Platform

FitGenie AI is a production-grade, multi-agent AI fitness assistant built with **CrewAI**, **FastAPI**, **OpenRouter (Claude 3.5 Sonnet / Llama 3.3 70B)**, and a modern **React Native & Web UI**.

It provides personalized, evidence-based fitness programs including workout planning, nutrition & macro calculations, supplement protocols, injury prevention risk analysis, progress analytics, healthy restaurant discovery, and fitness gear shopping.

---

## 🌟 Key Features

- **Multi-Agent Orchestration (CrewAI):** 10 specialized AI agents working collaboratively to deliver holistic fitness programs.
- **Deterministic Math Engine:** All BMR (Mifflin-St Jeor), TDEE, BMI, and macro targets are computed in pure Python using `CalculatorService` (zero LLM math hallucination).
- **Presentation Layer Formatter:** Converts internal structured JSON into clean, emoji-free Markdown formatted for React Native & Web UIs.
- **Multi-Step Assessment Wizard:** Interactive 8-step onboarding flow capturing demographics, goals, experience, injuries, schedule, and budget preferences.
- **Interactive Dark Dashboard:** Modern Nike/WHOOP-inspired UI (`#0D0D0D` dark aesthetic) with SVG vector icons and expandable card layouts.
- **RESTful API:** FastAPI backend exposing OpenAPI/Swagger documentation (`GET /docs`).

---

## 🏗️ Architecture Overview

```
User / UI -> FastAPI Endpoints -> AgentRunner Telemetry -> CrewAI Multi-Agent Crews
                                                                │
                                                                ├─► Fitness Assessment Specialist
                                                                ├─► Workout Planning Specialist
                                                                ├─► Nutrition Planning Specialist
                                                                ├─► Supplement Advisor
                                                                ├─► Injury Prevention Specialist
                                                                ├─► Progress Analyst
                                                                ├─► Healthy Restaurant Advisor
                                                                └─► Fitness Shopping Advisor
```

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **AI / Agentic Framework:** CrewAI v1.15.9, LiteLLM
- **LLM Provider:** OpenRouter API (`openrouter/meta-llama/llama-3.3-70b-instruct` / `openrouter/anthropic/claude-3.5-sonnet`)
- **Frontend UI:** HTML5, Vanilla CSS3 (Dark Design System), Modern JavaScript ES6+
- **Environment:** `python-dotenv` for secure environment variable management

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mohamedmuhsen/FitGenie-AI.git
cd FitGenie-AI
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# LLM Configuration
LLM_MODEL=openrouter/meta-llama/llama-3.3-70b-instruct
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_TEMPERATURE=0.7
LLM_TIMEOUT=60

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### 4. Run the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Web UI:** Access the dashboard at [http://localhost:8000](http://localhost:8000)
- **API Documentation:** Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testing & Validation

Run the complete end-to-end scenario test suite:
```bash
python -u test_all_scenarios.py
```

---

## 📄 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web Dashboard UI |
| `GET` | `/health` | Health Check Endpoint |
| `GET` | `/api` | System API Status & Configuration Metadata |
| `POST` | `/chat` | Conversational AI Orchestrator |
| `POST` | `/assessment` | Fitness Profile & Health Assessment |
| `POST` | `/workout` | Workout Program Generation |
| `POST` | `/nutrition` | Nutrition & Daily Meal Plan |
| `POST` | `/supplements` | Evidence-Based Supplement Protocol |
| `POST` | `/injury_prevention` | Biomechanical Risk Analysis & Alternatives |
| `POST` | `/shopping` | Gym Gear & Equipment Recommendations |
| `POST` | `/restaurants` | Healthy Restaurant Discovery |
| `POST` | `/progress` | Progress Metrics Analytics |

---

## 🔒 Security

All API keys and environment configurations are excluded from version control via `.gitignore`. API keys are securely loaded at runtime and masked in all server logs.

---

## 👤 Author & Maintainer

- **Developer:** Mohamed Mohsen ([@Mohamedmuhsen](https://github.com/Mohamedmuhsen))
- **Email:** mohummedmohsen24@gmail.com
