from fastapi import FastAPI

from app.routes.student_routes import (
    router as student_router
)

from app.database import db

app = FastAPI()

# =========================
# ROUTES
# =========================

app.include_router(student_router)

# =========================
# ROOT
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

    # FIX OBJECT ID ERROR
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
        "students": students
    }

# =========================
# HEALTH ALERTS
# =========================

@app.get("/health-alerts")
def health_alerts():

    students = list(db.daily_checkins.find({}))

    alerts = {
        "high_risk": [],
        "warning": [],
        "normal": []
    }

    for s in students:

        stress = s.get("stress_level", 0)
        sleep = s.get("sleep_hours", 0)
        mood = s.get("mood", 0)

        # Convert MongoDB ObjectId
        s["_id"] = str(s["_id"])

        # HIGH RISK
        if stress >= 8 or sleep < 5 or mood <= 3:

            alerts["high_risk"].append({
                "name": s.get("name"),
                "status": "HIGH RISK"
            })

        # WARNING
        elif stress >= 6 or sleep < 6 or mood <= 5:

            alerts["warning"].append({
                "name": s.get("name"),
                "status": "WARNING"
            })

        # NORMAL
        else:

            alerts["normal"].append({
                "name": s.get("name"),
                "status": "NORMAL"
            })

    return alerts