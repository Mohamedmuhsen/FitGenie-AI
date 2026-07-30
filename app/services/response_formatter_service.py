"""
FitGenie AI - Response Formatter Service (Presentation Layer)

Transforms structured JSON outputs from all CrewAI agents into 
clean, premium Markdown suitable for React Native and Web UIs.

Design Requirements:
- ZERO EMOJIS in headers, titles, lists, or tags
- Clean typography and structured headings (## Titles, Bullet Lists, Spacing)
- Exposes no raw JSON to end users while preserving internal data payloads
"""

import json
import logging
from typing import Any

logger = logging.getLogger("fitgenie.response_formatter")


class ResponseFormatterService:
    """Formats structured agent outputs into clean, emoji-free Markdown."""

    @staticmethod
    def format_response(domain: str, raw_output: Any) -> str:
        """Main entry point to convert raw structured agent output into formatted Markdown."""
        
        data = raw_output
        if isinstance(raw_output, str):
            try:
                clean_str = raw_output.strip()
                if clean_str.startswith("```"):
                    lines = clean_str.split("\n")
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    clean_str = "\n".join(lines).strip()
                data = json.loads(clean_str)
            except Exception:
                return raw_output.strip()

        if not isinstance(data, dict):
            return str(data)

        # Dispatch formatting by domain
        try:
            if domain == "assessment":
                return ResponseFormatterService._format_assessment(data)
            elif domain == "workout":
                return ResponseFormatterService._format_workout(data)
            elif domain == "nutrition":
                return ResponseFormatterService._format_nutrition(data)
            elif domain == "supplements":
                return ResponseFormatterService._format_supplements(data)
            elif domain == "injury_prevention":
                return ResponseFormatterService._format_injury_prevention(data)
            elif domain == "shopping":
                return ResponseFormatterService._format_shopping(data)
            elif domain == "restaurants":
                return ResponseFormatterService._format_restaurants(data)
            elif domain == "progress":
                return ResponseFormatterService._format_progress(data)
            elif domain == "motivation":
                return ResponseFormatterService._format_motivation(data)
            else:
                return ResponseFormatterService._format_generic(data)
        except Exception as e:
            logger.error(f"Error formatting domain '{domain}': {e}", exc_info=True)
            return ResponseFormatterService._format_generic(data)

    @staticmethod
    def _format_assessment(data: dict[str, Any]) -> str:
        profile = data.get("user_profile", {})
        bmr = data.get("bmr", "N/A")
        tdee = data.get("tdee", "N/A")
        bmi = data.get("bmi", "N/A")
        bmi_cat = data.get("bmi_category", "N/A")
        cals = data.get("daily_calories", "N/A")
        macros = data.get("macros", {})
        risks = data.get("risk_factors", [])

        lines = [
            "## Fitness Assessment & Health Profile",
            "",
            "### Health Metrics",
            f"- **BMR (Basal Metabolic Rate):** {bmr} kcal",
            f"- **TDEE (Daily Energy Expenditure):** {tdee} kcal",
            f"- **BMI:** {bmi} ({bmi_cat})",
            f"- **Target Daily Intake:** **{cals} kcal** ({profile.get('goal', 'maintenance').replace('_', ' ').title()})",
            "",
            "### Daily Macro Targets",
            f"- **Protein:** {macros.get('protein_g', 'N/A')} g",
            f"- **Carbohydrates:** {macros.get('carbs_g', 'N/A')} g",
            f"- **Fats:** {macros.get('fats_g', 'N/A')} g",
            ""
        ]

        if risks:
            lines.append("### Safety Considerations")
            for r in risks:
                lines.append(f"- {r}")

        return "\n".join(lines)

    @staticmethod
    def _format_workout(data: dict[str, Any]) -> str:
        plan_name = data.get("plan_name", "Personalized Workout Plan")
        goal = data.get("goal", "Fitness").replace("_", " ").title()
        days_per_week = data.get("days_per_week", 4)
        days = data.get("workout_days", [])
        warmup = data.get("warmup", "")
        cooldown = data.get("cooldown", "")
        progression = data.get("progression_notes", "")

        lines = [
            f"## {plan_name}",
            f"*Goal: {goal} | Frequency: {days_per_week} Days / Week*",
            ""
        ]

        if warmup:
            lines.extend(["**Warmup Routine:**", f"{warmup}", ""])

        for day in days:
            day_title = day.get("day", "Workout Day")
            focus = day.get("focus", "Full Body")
            duration = day.get("duration_minutes", 60)
            exercises = day.get("exercises", [])

            lines.append(f"### {day_title} — {focus} ({duration} min)")
            
            for ex in exercises:
                if isinstance(ex, dict):
                    name = ex.get("name", "Exercise").title()
                    sets = ex.get("sets", "3-4")
                    reps = ex.get("reps", "8-12")
                    rest = ex.get("rest_seconds", 60)
                    muscle = ex.get("muscle_group", "").title()
                    notes = ex.get("notes", "")

                    ex_str = f"- **{name}** — {sets} sets × {reps} reps"
                    if rest:
                        ex_str += f" *(Rest: {rest}s)*"
                    if muscle:
                        ex_str += f" `[{muscle}]`"
                    lines.append(ex_str)
                    if notes:
                        lines.append(f"  *Note:* {notes}")
                else:
                    lines.append(f"- {ex}")
            lines.append("")

        if cooldown:
            lines.extend(["**Cooldown Routine:**", f"{cooldown}", ""])

        if progression:
            lines.extend(["**Progression Strategy:**", f"{progression}"])

        return "\n".join(lines)

    @staticmethod
    def _format_nutrition(data: dict[str, Any]) -> str:
        cals = data.get("daily_calories", "N/A")
        p = data.get("protein_g", "N/A")
        c = data.get("carbs_g", "N/A")
        f = data.get("fats_g", "N/A")
        hydration = data.get("hydration_liters", 3.0)
        meals = data.get("meals", [])
        notes = data.get("notes", "")

        lines = [
            "## Daily Nutrition Plan",
            "",
            "### Daily Targets Summary",
            f"- **Calories:** **{cals} kcal**",
            f"- **Macros:** Protein {p}g  |  Carbs {c}g  |  Fats {f}g",
            f"- **Hydration:** {hydration} Liters / day",
            "",
            "---",
            "### Daily Meal Schedule",
            ""
        ]

        for meal in meals:
            m_name = meal.get("meal_name", "Meal")
            m_time = meal.get("time", "")
            m_cals = meal.get("total_calories", "N/A")
            m_p = meal.get("total_protein_g", "N/A")
            m_c = meal.get("total_carbs_g", "N/A")
            m_f = meal.get("total_fats_g", "N/A")
            foods = meal.get("foods", [])

            header = f"#### {m_name}"
            if m_time:
                header += f" ({m_time})"
            header += f" — **{m_cals} kcal** `[P: {m_p}g | C: {m_c}g | F: {m_f}g]`"
            lines.append(header)

            for food in foods:
                if isinstance(food, dict):
                    f_name = food.get("name", "Food")
                    portion = food.get("portion", "")
                    f_cals = food.get("calories", "")
                    lines.append(f"- **{f_name}** ({portion}) — {f_cals} kcal")
                else:
                    lines.append(f"- {food}")
            lines.append("")

        if notes:
            lines.extend(["**Dietitian Notes:**", f"{notes}"])

        return "\n".join(lines)

    @staticmethod
    def _format_supplements(data: dict[str, Any]) -> str:
        recs = data.get("recommendations", [])
        cost = data.get("total_monthly_cost_estimate", "")
        warnings = data.get("warnings", [])

        lines = [
            "## Supplement Recommendations",
            ""
        ]

        if cost:
            lines.extend([f"**Estimated Monthly Cost:** {cost}", ""])

        for item in recs:
            name = item.get("name", "Supplement")
            dosage = item.get("dosage", "")
            timing = item.get("timing", "")
            reason = item.get("reason", "")
            priority = item.get("priority", "recommended").upper()

            lines.append(f"### {name} `[{priority}]`")
            if dosage:
                lines.append(f"- **Dosage:** {dosage}")
            if timing:
                lines.append(f"- **Optimal Timing:** {timing}")
            if reason:
                lines.append(f"- **Scientific Rationale:** {reason}")
            lines.append("")

        if warnings:
            lines.append("### Safety Warnings")
            for w in warnings:
                lines.append(f"- {w}")

        return "\n".join(lines)

    @staticmethod
    def _format_injury_prevention(data: dict[str, Any]) -> str:
        flagged = data.get("original_exercises_flagged", [])
        alternatives = data.get("safe_alternatives", [])
        warnings = data.get("safety_warnings", [])
        notes = data.get("modified_workout_plan_notes", "")

        lines = [
            "## Injury Prevention & Safety Guidance",
            ""
        ]

        if flagged:
            lines.append("### Flagged Risky Exercises")
            for f in flagged:
                if isinstance(f, dict):
                    lines.append(f"- **{f.get('exercise', 'Exercise')}** — {f.get('reason', '')}")
                else:
                    lines.append(f"- {f}")
            lines.append("")

        if alternatives:
            lines.append("### Safe Replacement Exercises")
            for alt in alternatives:
                if isinstance(alt, dict):
                    orig = alt.get("original", "Original Exercise")
                    repl = alt.get("replacement", "Safer Alternative")
                    reason = alt.get("reason", "")
                    lines.append(f"- **{orig}** -> Replace with **{repl}**")
                    if reason:
                        lines.append(f"  *Reason:* {reason}")
                else:
                    lines.append(f"- {alt}")
            lines.append("")

        if warnings:
            lines.append("### Form Cues & Precautions")
            for w in warnings:
                lines.append(f"- {w}")

        if notes:
            lines.extend(["", f"**Note:** {notes}"])

        return "\n".join(lines)

    @staticmethod
    def _format_shopping(data: dict[str, Any]) -> str:
        items = data.get("items", [])
        budget = data.get("total_estimated_budget", "")

        lines = [
            "## Fitness Equipment & Gear Recommendations",
            ""
        ]

        if budget:
            lines.extend([f"**Estimated Budget:** {budget}", ""])

        for item in items:
            name = item.get("name", "Product")
            cat = item.get("category", "").title()
            price = item.get("estimated_price", "")
            reason = item.get("reason", "")
            priority = item.get("priority", "").title()

            lines.append(f"### {name}")
            details = []
            if cat: details.append(f"Category: {cat}")
            if price: details.append(f"Price: {price}")
            if priority: details.append(f"Priority: {priority}")
            if details:
                lines.append(f"- *{' | '.join(details)}*")
            if reason:
                lines.append(f"- **Why recommended:** {reason}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _format_restaurants(data: dict[str, Any]) -> str:
        restaurants = data.get("restaurants", [])

        lines = [
            "## Healthy Restaurants Nearby",
            ""
        ]

        for r in restaurants:
            name = r.get("name", "Restaurant")
            cuisine = r.get("cuisine", "")
            rating = r.get("rating", 4.5)
            dist = r.get("distance_km", 0.0)
            addr = r.get("address", "")
            meal = r.get("recommended_meal", "")
            cals = r.get("estimated_calories", "")
            reason = r.get("reason", "")

            lines.append(f"### {name} (Rating: {rating} / 5.0 • {dist} km)")
            if cuisine or addr:
                lines.append(f"- *{cuisine}* — {addr}")
            if meal:
                lines.append(f"- **Recommended Meal:** {meal}")
            if cals:
                lines.append(f"- **Calorie Estimate:** ~{cals} kcal")
            if reason:
                lines.append(f"- **Why it fits:** {reason}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _format_progress(data: dict[str, Any]) -> str:
        w_change = data.get("weight_change_kg", 0.0)
        w_pct = data.get("weight_change_pct", 0.0)
        consistency = data.get("consistency_pct", 0.0)
        trend = data.get("trend", "stable").title()
        summary = data.get("summary", "")
        adjustments = data.get("adjustments", [])
        motivation = data.get("motivation_message", "")

        lines = [
            "## Progress Analysis & Metrics",
            "",
            "### Performance Summary",
            f"- **Weight Change:** {w_change:+.1f} kg ({w_pct:+.1f}%)",
            f"- **Workout Consistency:** {consistency:.0f}%",
            f"- **Overall Trend:** **{trend}**",
            ""
        ]

        if summary:
            lines.extend(["### Overview", summary, ""])

        if adjustments:
            lines.append("### Recommended Adjustments")
            for adj in adjustments:
                lines.append(f"- {adj}")
            lines.append("")

        if motivation:
            lines.extend(["### Performance Coaching", motivation])

        return "\n".join(lines)

    @staticmethod
    def _format_motivation(data: dict[str, Any]) -> str:
        msg = data.get("motivation_message", data.get("summary", "Maintain consistency toward your long-term goals."))
        return f"## Performance Mindset & Coaching\n\n{msg}"

    @staticmethod
    def _format_generic(data: dict[str, Any]) -> str:
        """Fallback formatter for arbitrary dictionary outputs."""
        lines = ["## FitGenie AI Response", ""]
        for k, v in data.items():
            if k in ("status", "execution_mode", "llm_model", "agents_executed", "duration_ms", "api_key_status"):
                continue
            title = k.replace("_", " ").title()
            if isinstance(v, list):
                lines.append(f"### {title}")
                for item in v:
                    lines.append(f"- {item}")
                lines.append("")
            elif isinstance(v, dict):
                lines.append(f"### {title}")
                for sub_k, sub_v in v.items():
                    lines.append(f"- **{sub_k.replace('_', ' ').title()}:** {sub_v}")
                lines.append("")
            else:
                lines.append(f"- **{title}:** {v}")
        return "\n".join(lines)
