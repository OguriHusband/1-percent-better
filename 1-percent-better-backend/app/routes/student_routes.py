from fastapi import APIRouter
from app.models.student_model import StudentCheckin
from app.utils.bmi import calculate_bmi
from app.utils.wellness_score import calculate_wellness_score
from app.database import db
from app.services.gemini_service import generate_health_advice
from app.services.memory_service import save_memory

router = APIRouter()

@router.post("/checkin")
def student_checkin(data: StudentCheckin):

    student_data = data.dict()

    bmi_result = calculate_bmi(
        student_data["weight"],
        student_data["height"]
    )

    wellness_score = calculate_wellness_score(
        student_data["mood"],
        student_data["sleep_hours"],
        student_data["exercise_minutes"],
        student_data["stress_level"]
    )

    student_data["bmi"] = bmi_result
    student_data["wellness_score"] = wellness_score

    # Generate AI advice
    ai_advice = generate_health_advice(student_data)

    # Save AI advice
    student_data["ai_advice"] = ai_advice
    save_memory(
    student_input=student_data,
    ai_output=ai_advice,
    source="gemini/local"
)

    # Save to MongoDB
    result = db.daily_checkins.insert_one(student_data)

    # Convert ObjectId into string
    student_data["_id"] = str(result.inserted_id)

    return {
        "message": "Check-in successful",
        "data": student_data
    }