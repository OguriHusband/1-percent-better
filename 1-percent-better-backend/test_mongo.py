from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)

db = client["1_percent_better"]

print("MongoDB Connected Successfully!")