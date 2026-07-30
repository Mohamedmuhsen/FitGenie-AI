class CalculatorService:
    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        gender = gender.lower()
        if gender == "male":
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        elif gender == "female":
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        else:
            male_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
            female_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
            return (male_bmr + female_bmr) / 2

    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
        return bmr * multiplier

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)

    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi <= 24.9:
            return "Normal"
        elif 25 <= bmi <= 29.9:
            return "Overweight"
        else:
            return "Obese"

    @staticmethod
    def calculate_macros(daily_calories: int, goal: str, weight_kg: float) -> dict:
        goal = goal.lower()
        if goal == "muscle_gain":
            protein_g = 2.2 * weight_kg
            fats_g = 0.25 * daily_calories / 9
            carbs_g = (daily_calories - (protein_g * 4 + fats_g * 9)) / 4
        elif goal == "fat_loss":
            protein_g = 2.4 * weight_kg
            fats_g = 0.30 * daily_calories / 9
            carbs_g = (daily_calories - (protein_g * 4 + fats_g * 9)) / 4
        elif goal == "maintenance":
            protein_g = 1.8 * weight_kg
            fats_g = 0.25 * daily_calories / 9
            carbs_g = (daily_calories - (protein_g * 4 + fats_g * 9)) / 4
        elif goal == "endurance":
            protein_g = 1.6 * weight_kg
            fats_g = 0.20 * daily_calories / 9
            carbs_g = (daily_calories - (protein_g * 4 + fats_g * 9)) / 4
        else:
            protein_g = 1.8 * weight_kg
            fats_g = 0.25 * daily_calories / 9
            carbs_g = (daily_calories - (protein_g * 4 + fats_g * 9)) / 4
            
        return {
            "protein_g": round(protein_g, 1),
            "carbs_g": round(carbs_g, 1),
            "fats_g": round(fats_g, 1)
        }

    @staticmethod
    def calculate_daily_calories(tdee: float, goal: str) -> int:
        goal = goal.lower()
        if goal == "muscle_gain":
            return int(tdee + 300)
        elif goal == "fat_loss":
            return int(tdee - 500)
        elif goal == "endurance":
            return int(tdee + 200)
        else:
            return int(tdee)

    @staticmethod
    def calculate_progress_metrics(current_weight: float, previous_weight: float, workouts_completed: int, workouts_planned: int, goal: str) -> dict:
        weight_change_kg = current_weight - previous_weight
        weight_change_pct = (weight_change_kg / previous_weight) * 100
        consistency_pct = (workouts_completed / workouts_planned) * 100 if workouts_planned > 0 else 0
        
        goal = goal.lower()
        if abs(weight_change_kg) < 0.2:
            trend = "stalling"
        elif (goal == "fat_loss" and weight_change_kg < 0) or (goal == "muscle_gain" and weight_change_kg > 0):
            trend = "improving"
        elif goal == "maintenance" and abs(weight_change_kg) < 1.0:
            trend = "improving"
        else:
            trend = "declining"
            
        return {
            "weight_change_kg": round(weight_change_kg, 2),
            "weight_change_pct": round(weight_change_pct, 2),
            "consistency_pct": round(consistency_pct, 2),
            "trend": trend
        }
