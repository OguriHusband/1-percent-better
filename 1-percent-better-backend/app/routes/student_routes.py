from fastapi import APIRouter

from app.models.student_model import StudentCheckin

from app.utils.bmi import calculate_bmi
from app.utils.wellness_score import calculate_wellness_score

from app.database import db

from app.services.gemini_service import generate_health_advice

from app.services.mbg_service import generate_mbg_recommendation

from app.services.memory_service import save_memory

from app.services.pattern_service import (
    extract_pattern_ai,
    save_pattern
)

router = APIRouter()


@router.post("/checkin")
def student_checkin(data: StudentCheckin):

    # Convert request into dictionary
    student_data = data.dict()

    # =========================
    # BMI CALCULATION
    # =========================

    bmi_result = calculate_bmi(
        student_data["weight"],
        student_data["height"]
    )

    student_data["bmi"] = bmi_result

    # =========================
    # WELLNESS SCORE
    # =========================

    wellness_score = calculate_wellness_score(
        student_data["mood"],
        student_data["sleep_hours"],
        student_data["exercise_minutes"],
        student_data["stress_level"]
    )

    student_data["wellness_score"] = wellness_score

    # =========================
    # MBG RECOMMENDATION
    # =========================

    mbg_recommendation = generate_mbg_recommendation(student_data)

    student_data["mbg_recommendation"] = mbg_recommendation

    # =========================
    # AI HEALTH ADVICE
    # =========================

    ai_advice = generate_health_advice(student_data)

    student_data["ai_advice"] = ai_advice

    # =========================
    # PATTERN AI
    # =========================

    pattern = extract_pattern_ai(student_data)

    student_data["pattern"] = pattern

    save_pattern(pattern)

    # =========================
    # SAVE AI MEMORY
    # =========================

    save_memory(
        student_input=student_data,
        ai_output=ai_advice,
        source="gemini/local"
    )

    # =========================
    # SAVE TO MONGODB
    # =========================

    result = db.daily_checkins.insert_one(student_data)

    student_data["_id"] = str(result.inserted_id)

    # =========================
    # FINAL RESPONSE
    # =========================

    return {
        "message": "Check-in successful",
        "data": student_data
    }