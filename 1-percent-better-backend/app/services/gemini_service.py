from google import genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# =========================
# LOCAL AI FALLBACK
# =========================

def local_ai_analysis(student_data):

    advice = []

    bmi = student_data["bmi"]["bmi"]
    mood = student_data["mood"]
    sleep = student_data["sleep_hours"]
    exercise = student_data["exercise_minutes"]
    stress = student_data["stress_level"]

    # BMI Analysis
    if bmi < 18.5:
        advice.append("⚠️ Berat badan pengguna di bawah normal.")
        advice.append("✅ Tambahkan protein dan susu.")

    elif bmi > 25:
        advice.append("⚠️ Berat badan pengguna berlebih.")
        advice.append("✅ Kurangi gula dan gorengan.")

    else:
        advice.append("✅ BMI pengguna normal.")

    # Sleep analysis
    if sleep < 7:
        advice.append("✅ Jam tidur pengguna kurang.")

    # Stress analysis
    if stress >= 7:
        advice.append("✅ Tingkat stres pengguna tinggi.")

    # Mood analysis
    if mood <= 4:
        advice.append("✅ Mood pengguna rendah.")

    # Exercise analysis
    if exercise < 30:
        advice.append("✅ Aktivitas fisik pengguna kurang.")

    advice.append("✅ Rekomendasi nutrisi: nasi, telur, tempe, sayur, susu.")
    advice.append("\n✅ Analisa menggunakan Local 1% Better AI.")

    return "\n\n".join(advice)

# =========================
# HYBRID AI FUNCTION
# =========================

def generate_health_advice(student_data):

    try:

        prompt = f"""
        Anda adalah AI kesehatan remaja Indonesia.

        Nama: {student_data["name"]}
        Umur: {student_data["age"]}
        BMI: {student_data["bmi"]["bmi"]}
        Kategori BMI: {student_data["bmi"]["category"]}
        Mood: {student_data["mood"]}
        Jam tidur: {student_data["sleep_hours"]}
        Olahraga: {student_data["exercise_minutes"]}
        Stress: {student_data["stress_level"]}

        Berikan analisa lengkap:
        - Kesehatan fisik
        - Kesehatan mental
        - Rekomendasi aktivitas
        - Rekomendasi nutrisi
        - Saran kebiasaan sehat
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text + "\n\n✅ Analisa menggunakan Gemini AI."

    except Exception as e:

        print("Gemini Error:", e)

        return local_ai_analysis(student_data)