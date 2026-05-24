from google import genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY:", API_KEY)

# Create Gemini client
client = genai.Client(api_key=API_KEY)

# Ask Gemini something
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Give health advice for students with poor sleep habits."
)

print("\n=== AI RESPONSE ===\n")

print(response.text)