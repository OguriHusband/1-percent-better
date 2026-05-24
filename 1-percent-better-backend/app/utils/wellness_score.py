def calculate_wellness_score(
    mood,
    sleep_hours,
    exercise_minutes,
    stress_level
):

    score = 100

    if sleep_hours < 7:
        score -= 20

    if stress_level > 7:
        score -= 25

    if mood < 5:
        score -= 20

    if exercise_minutes < 30:
        score -= 15

    return max(score, 0)