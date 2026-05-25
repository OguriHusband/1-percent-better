from app.database import db
from datetime import datetime

def save_memory(student_input, ai_output, source="local"):

    memory = {
        "timestamp": datetime.utcnow(),
        "input": student_input,
        "output": ai_output,
        "source": source
    }

    db.ai_memory.insert_one(memory)

    return memory