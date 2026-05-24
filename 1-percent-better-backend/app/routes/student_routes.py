from fastapi import APIRouter
from app.models.student_model import StudentCheckin
from app.utils.bmi import calculate_bmi
from app.utils.wellness_score import calculate_wellness_score
from app.database import db

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

    result = db.daily_checkins.insert_one(student_data)

    student_data["_id"] = str(result.inserted_id)

    return {
        "message": "Check-in successful",
        "data": student_data
    }