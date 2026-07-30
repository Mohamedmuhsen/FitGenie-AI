"""
FitGenie AI Agent Runner & Execution Engine

Handles agent/crew execution with:
- Async support for FastAPI event loops (`crew.kickoff_async()`)
- Detailed debug & performance logging
- API key detection & validation with secure masking
- Live CrewAI execution when valid API key is present
- JSON string auto-parsing for live LLM structured outputs
- Deterministic tool-driven fallback execution when LLM is unavailable
- ResponseFormatterService integration to convert structured data to Markdown
"""

import json
import time
import logging
import asyncio
from typing import Any
from crewai import Crew

from app.config.settings import get_settings
from app.services.calculator_service import CalculatorService
from app.services.response_formatter_service import ResponseFormatterService
from app.tools.exercise_search_tool import ExerciseSearchTool
from app.tools.nutrition_search_tool import NutritionSearchTool
from app.tools.google_maps_tool import GoogleMapsTool
from app.tools.shopping_search_tool import ShoppingSearchTool
from app.tools.progress_analytics_tool import ProgressAnalyticsTool

logger = logging.getLogger("fitgenie.agent_runner")


class AgentRunner:
    """Executes CrewAI Crews with telemetry, logging, fallback handling, and response formatting."""

    @staticmethod
    async def execute_crew_async(domain: str, crew: Crew, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Executes a CrewAI crew asynchronously for FastAPI compatibility.
        Uses crew.kickoff_async() when live API key is active.
        """
        settings = get_settings()
        start_time = time.time()

        agent_names = [a.role for a in crew.agents]
        task_descriptions = [t.description[:60] + "..." for t in crew.tasks]

        masked_key = settings.get_masked_api_key()
        logger.info(f"=== [AGENT STARTED] Domain: '{domain}' ===")
        logger.info(f"  Agents involved: {agent_names}")
        logger.info(f"  Tasks assigned: {task_descriptions}")
        logger.info(f"  LLM Model: {settings.LLM_MODEL} | Key: {masked_key}")

        has_key = settings.has_valid_api_key()
        raw_output = None
        exec_mode = "live_llm" if has_key else "deterministic_tool_engine"

        if has_key:
            logger.info("  [LLM CALLED] Valid OPENROUTER_API_KEY active. Executing crew.kickoff_async()...")
            try:
                result = await crew.kickoff_async()
                raw_str = str(result).strip()
                
                # Strip markdown code blocks if wrapped by LLM
                if raw_str.startswith("```"):
                    lines = raw_str.split("\n")
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_str = "\n".join(lines).strip()
                
                try:
                    raw_output = json.loads(raw_str)
                except Exception:
                    raw_output = raw_str
            except Exception as e:
                logger.warning(f"  [LLM CALL FAILED] Live LLM execution error: {e}. Falling back to tool engine.")
                exec_mode = "deterministic_tool_engine"

        if not raw_output or exec_mode == "deterministic_tool_engine":
            logger.info(f"  [EXECUTING TOOL ENGINE] Generating structured '{domain}' data...")
            raw_output = AgentRunner.generate_fallback(domain, payload)

        duration = round((time.time() - start_time) * 1000, 2)

        # Presentation Layer: Format structured output to Markdown
        formatted_response = ResponseFormatterService.format_response(domain, raw_output)

        logger.info(f"=== [AGENT FINISHED] Domain: '{domain}' ({exec_mode}) in {duration}ms ===")

        structured_dict = raw_output if isinstance(raw_output, dict) else {"raw": str(raw_output)}

        return {
            "status": "success",
            "execution_mode": exec_mode,
            "llm_model": settings.LLM_MODEL,
            "agents_executed": agent_names,
            "duration_ms": duration,
            "response": formatted_response,
            "data": structured_dict
        }

    @staticmethod
    def execute_crew(domain: str, crew: Crew, payload: dict[str, Any]) -> dict[str, Any]:
        """Synchronous wrapper for non-async environments."""
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                return loop.run_until_complete(AgentRunner.execute_crew_async(domain, crew, payload))
        except RuntimeError:
            pass
        return asyncio.run(AgentRunner.execute_crew_async(domain, crew, payload))

    @staticmethod
    def generate_fallback(domain: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Generates rich, structured domain outputs using Python tools & services."""
        
        if domain == "assessment":
            weight = float(payload.get("weight_kg", 75.0))
            height = float(payload.get("height_cm", 175.0))
            age = int(payload.get("age", 25))
            gender = str(payload.get("gender", "male"))
            goal = str(payload.get("goal", "muscle_gain"))
            injuries = payload.get("injuries", [])

            bmr = CalculatorService.calculate_bmr(weight, height, age, gender)
            tdee = CalculatorService.calculate_tdee(bmr, "moderately_active")
            bmi = CalculatorService.calculate_bmi(weight, height)
            bmi_cat = CalculatorService.get_bmi_category(bmi)
            cals = CalculatorService.calculate_daily_calories(tdee, goal)
            macros = CalculatorService.calculate_macros(cals, goal, weight)

            risks = []
            if "shoulder" in [i.lower() for i in injuries]:
                risks.append("Shoulder impingement risk: Avoid heavy overhead press and wide-grip bench press.")
            if "knee" in [i.lower() for i in injuries]:
                risks.append("Knee stress risk: Replace deep squats with leg press or box squats.")
            if not risks:
                risks.append("No specific injury risk factors identified.")

            return {
                "user_profile": payload,
                "bmr": round(bmr, 1),
                "tdee": round(tdee, 1),
                "bmi": round(bmi, 1),
                "bmi_category": bmi_cat,
                "daily_calories": cals,
                "macros": macros,
                "risk_factors": risks
            }

        elif domain == "workout":
            goal = payload.get("goal", "muscle_gain")
            exp = payload.get("experience_level", "intermediate")
            days_count = int(payload.get("workout_days_per_week", 4))
            
            ex_tool = ExerciseSearchTool()
            chest_ex = json.loads(ex_tool._run(query="chest"))
            back_ex = json.loads(ex_tool._run(query="back"))
            leg_ex = json.loads(ex_tool._run(query="legs"))
            shoulder_ex = json.loads(ex_tool._run(query="shoulders"))
            arm_ex = json.loads(ex_tool._run(query="arms"))

            workout_days = [
                {
                    "day": "Monday",
                    "focus": "Chest & Triceps",
                    "duration_minutes": 60,
                    "exercises": [
                        chest_ex[0] if chest_ex else {"name": "Bench Press", "sets": 4, "reps": "8-12", "rest_seconds": 90},
                        chest_ex[1] if len(chest_ex)>1 else {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "rest_seconds": 60},
                        chest_ex[2] if len(chest_ex)>2 else {"name": "Cable Flyes", "sets": 3, "reps": "12-15", "rest_seconds": 60},
                        arm_ex[1] if len(arm_ex)>1 else {"name": "Tricep Pushdowns", "sets": 3, "reps": "10-12", "rest_seconds": 60}
                    ]
                },
                {
                    "day": "Tuesday",
                    "focus": "Back & Biceps",
                    "duration_minutes": 60,
                    "exercises": [
                        back_ex[0] if back_ex else {"name": "Pull-ups", "sets": 4, "reps": "8-10", "rest_seconds": 90},
                        back_ex[1] if len(back_ex)>1 else {"name": "Barbell Rows", "sets": 3, "reps": "10-12", "rest_seconds": 60},
                        arm_ex[0] if arm_ex else {"name": "Barbell Curls", "sets": 3, "reps": "10-12", "rest_seconds": 60}
                    ]
                },
                {
                    "day": "Thursday",
                    "focus": "Legs & Core",
                    "duration_minutes": 65,
                    "exercises": [
                        leg_ex[0] if leg_ex else {"name": "Barbell Squats", "sets": 4, "reps": "8-12", "rest_seconds": 120},
                        leg_ex[2] if len(leg_ex)>2 else {"name": "Romanian Deadlifts", "sets": 3, "reps": "10-12", "rest_seconds": 90},
                        leg_ex[4] if len(leg_ex)>4 else {"name": "Leg Curls", "sets": 3, "reps": "12-15", "rest_seconds": 60}
                    ]
                },
                {
                    "day": "Friday",
                    "focus": "Shoulders & Arms",
                    "duration_minutes": 55,
                    "exercises": [
                        shoulder_ex[0] if shoulder_ex else {"name": "Overhead Press", "sets": 4, "reps": "8-12", "rest_seconds": 90},
                        shoulder_ex[1] if len(shoulder_ex)>1 else {"name": "Lateral Raises", "sets": 3, "reps": "12-15", "rest_seconds": 60},
                        shoulder_ex[2] if len(shoulder_ex)>2 else {"name": "Face Pulls", "sets": 3, "reps": "12-15", "rest_seconds": 60}
                    ]
                }
            ]

            return {
                "plan_name": f"FitGenie {goal.replace('_', ' ').title()} Program",
                "goal": goal,
                "experience_level": exp,
                "days_per_week": days_count,
                "weeks": 4,
                "workout_days": workout_days[:days_count],
                "warmup": "5-10 minutes light cardio followed by dynamic shoulder and hip mobility drills.",
                "cooldown": "5 minutes static stretching focusing on chest, lats, hamstrings, and quads.",
                "progression_notes": "Increase weight by 2.5kg once you hit the top of the rep range for all sets with clean form."
            }

        elif domain == "nutrition":
            cals = int(payload.get("daily_calories", 2500))
            goal = payload.get("goal", "muscle_gain")

            return {
                "daily_calories": cals,
                "protein_g": round(cals * 0.30 / 4, 1),
                "carbs_g": round(cals * 0.45 / 4, 1),
                "fats_g": round(cals * 0.25 / 9, 1),
                "meals": [
                    {
                        "meal_name": "Breakfast",
                        "time": "8:00 AM",
                        "foods": [
                            {"name": "Oatmeal with Blueberries", "portion": "80g oats", "calories": 320, "protein_g": 11, "carbs_g": 54, "fats_g": 6},
                            {"name": "Whey Protein Shake", "portion": "1 scoop (30g)", "calories": 120, "protein_g": 24, "carbs_g": 3, "fats_g": 1.5}
                        ],
                        "total_calories": 440,
                        "total_protein_g": 35,
                        "total_carbs_g": 57,
                        "total_fats_g": 7.5
                    },
                    {
                        "meal_name": "Lunch",
                        "time": "12:30 PM",
                        "foods": [
                            {"name": "Grilled Chicken Breast", "portion": "200g", "calories": 330, "protein_g": 62, "carbs_g": 0, "fats_g": 7.2},
                            {"name": "Brown Rice", "portion": "150g cooked", "calories": 165, "protein_g": 3.5, "carbs_g": 35, "fats_g": 1.4},
                            {"name": "Steamed Broccoli", "portion": "100g", "calories": 35, "protein_g": 2.4, "carbs_g": 7, "fats_g": 0.4}
                        ],
                        "total_calories": 530,
                        "total_protein_g": 67.9,
                        "total_carbs_g": 42,
                        "total_fats_g": 9.0
                    },
                    {
                        "meal_name": "Pre-Workout Snack",
                        "time": "4:30 PM",
                        "foods": [
                            {"name": "Greek Yogurt with Banana", "portion": "200g yogurt + 1 banana", "calories": 210, "protein_g": 18, "carbs_g": 32, "fats_g": 1}
                        ],
                        "total_calories": 210,
                        "total_protein_g": 18,
                        "total_carbs_g": 32,
                        "total_fats_g": 1
                    },
                    {
                        "meal_name": "Dinner",
                        "time": "7:30 PM",
                        "foods": [
                            {"name": "Salmon Fillet", "portion": "180g", "calories": 370, "protein_g": 36, "carbs_g": 0, "fats_g": 23},
                            {"name": "Sweet Potato", "portion": "200g baked", "calories": 180, "protein_g": 4, "carbs_g": 41, "fats_g": 0.3}
                        ],
                        "total_calories": 550,
                        "total_protein_g": 40,
                        "total_carbs_g": 41,
                        "total_fats_g": 23.3
                    }
                ],
                "hydration_liters": 3.0,
                "notes": "Drink 500ml water upon waking and stay hydrated throughout your workout."
            }

        elif domain == "supplements":
            return {
                "recommendations": [
                    {
                        "name": "Creatine Monohydrate",
                        "dosage": "5g daily",
                        "timing": "Post-workout or anytime with water",
                        "reason": "Increases muscle phosphocreatine stores, enhancing strength, power output, and muscle mass.",
                        "priority": "essential"
                    },
                    {
                        "name": "Whey Protein Concentrate/Isolate",
                        "dosage": "1 scoop (25-30g protein)",
                        "timing": "Post-workout or between meals",
                        "reason": "Convenient high-quality protein source to meet daily protein targets for recovery.",
                        "priority": "essential"
                    },
                    {
                        "name": "Vitamin D3",
                        "dosage": "2000-5000 IU daily",
                        "timing": "Morning with a fat-containing meal",
                        "reason": "Supports bone health, immune function, and natural testosterone production.",
                        "priority": "recommended"
                    },
                    {
                        "name": "Omega-3 Fish Oil",
                        "dosage": "2g (1200mg EPA/DHA)",
                        "timing": "With lunch or dinner",
                        "reason": "Reduces joint inflammation, supports cardiovascular health and muscle recovery.",
                        "priority": "recommended"
                    }
                ],
                "total_monthly_cost_estimate": "$45 - $65",
                "warnings": [
                    "Consult your doctor before starting any supplement regimen if you have pre-existing medical conditions.",
                    "Ensure adequate hydration when supplementing with Creatine."
                ]
            }

        elif domain == "shopping":
            shop_tool = ShoppingSearchTool()
            shoes = json.loads(shop_tool._run(query="shoes"))
            gloves = json.loads(shop_tool._run(query="gloves"))
            belts = json.loads(shop_tool._run(query="belts"))

            items = []
            if shoes: items.append(shoes[0])
            if belts: items.append(belts[0])
            if gloves: items.append(gloves[0])

            return {
                "items": items if items else [
                    {"name": "Nike Metcon 9", "category": "shoes", "estimated_price": "$130", "reason": "Superior heel stability for heavy squats and deadlifts.", "priority": "essential"},
                    {"name": "Rogue Ohio Lifting Belt", "category": "belts", "estimated_price": "$80", "reason": "10mm genuine leather for intra-abdominal support on heavy compound lifts.", "priority": "recommended"}
                ],
                "total_estimated_budget": "$210 - $250"
            }

        elif domain == "restaurants":
            maps_tool = GoogleMapsTool()
            places = json.loads(maps_tool._run(query="healthy"))
            return {
                "restaurants": places if places else [
                    {
                        "name": "Green Bowl Kitchen",
                        "cuisine": "Healthy Bowl / Salad Bar",
                        "rating": 4.7,
                        "distance_km": 1.2,
                        "address": "123 Fitness Way, Downtown",
                        "recommended_meal": "Grilled Chicken Power Bowl (~520 cal, 45g Protein)",
                        "estimated_calories": 520,
                        "reason": "High protein, clean complex carbs, and fresh greens with dressing served on the side."
                    }
                ]
            }

        elif domain == "progress":
            curr = float(payload.get("current_weight_kg", 74.0))
            prev = float(payload.get("previous_weight_kg", 75.0))
            comp = int(payload.get("workouts_completed", 12))
            plan = int(payload.get("workouts_planned", 16))
            goal = payload.get("goal", "fat_loss")

            prog_tool = ProgressAnalyticsTool()
            res = json.loads(prog_tool._run(
                current_weight_kg=curr,
                previous_weight_kg=prev,
                goal=goal,
                weeks_active=4,
                workouts_completed=comp,
                workouts_planned=plan
            ))

            metrics = res.get("metrics", {})
            return {
                "weight_change_kg": metrics.get("weight_change_kg", -1.0),
                "weight_change_pct": metrics.get("weight_change_pct", -1.33),
                "consistency_pct": metrics.get("consistency_pct", 75.0),
                "trend": metrics.get("trend", "improving"),
                "summary": f"You lost {abs(curr - prev):.1f} kg with a workout consistency of {comp}/{plan} ({comp/plan*100:.0f}%).",
                "adjustments": [
                    "Maintain your current caloric deficit.",
                    "Aim to increase workout completion to 90%+ next week to maximize progress."
                ],
                "motivation_message": "Great work! You are making steady, measurable progress toward your goals. Keep pushing!"
            }

        else:
            return {
                "message": f"Processed domain '{domain}' successfully.",
                "payload": payload
            }
