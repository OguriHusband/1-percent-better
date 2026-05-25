from fastapi import FastAPI
from app.routes.student_routes import router as student_router
from app.database import db

app = FastAPI()

# Include routes
app.include_router(student_router)

# =========================
# ROOT ENDPOINT
# =========================

@app.get("/")
def root():

    return {
        "message": "1% Better Backend Running"
    }

# =========================
# SCHOOL INTELLIGENCE
# =========================

@app.get("/school-intelligence")
def school_intelligence():

    students = list(db.daily_checkins.find({}))

    # Convert MongoDB ObjectId into string
    for student in students:

        student["_id"] = str(student["_id"])

    total_students = len(students)

    high_stress = len([
        s for s in students
        if s.get("stress_level", 0) >= 7
    ])

    low_sleep = len([
        s for s in students
        if s.get("sleep_hours", 0) < 6
    ])

    low_mood = len([
        s for s in students
        if s.get("mood", 0) < 5
    ])

    return {
        "total_students": total_students,
        "high_stress_cases": high_stress,
        "low_sleep_cases": low_sleep,
        "low_mood_cases": low_mood,
        "students_data": students
    }