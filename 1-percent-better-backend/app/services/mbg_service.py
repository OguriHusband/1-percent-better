def generate_mbg_recommendation(data):

    stress = data.get("stress_level", 0)
    sleep = data.get("sleep_hours", 0)
    bmi = data.get("bmi", {})
    mood = data.get("mood", 0)

    recommendation = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": [],
        "reason": []
    }

    if stress >= 7:
        recommendation["snack"].append(
            "Dark chocolate + almond"
        )

        recommendation["reason"].append(
            "Stress tinggi → makanan penenang"
        )

    if sleep < 6:
        recommendation["breakfast"].append(
            "Oatmeal + banana + honey"
        )

        recommendation["reason"].append(
            "Kurang tidur → energi stabil"
        )

    if mood <= 4:
        recommendation["snack"].append(
            "Buah segar"
        )

    return recommendation