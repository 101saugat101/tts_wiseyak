import asyncio
from sqlalchemy import insert
from database.database import database, features

async def seed_features():
    await database.connect()

    features_data = [
        {"name": "speech_to_text", "description": "Convert audio to text", "is_free": False, "credit_cost": 4},
        {"name": "text_to_speech", "description": "Convert text to audio", "is_free": False, "credit_cost": 3},
        {"name": "summarize", "description": "Summarize large texts", "is_free": False, "credit_cost": 2},
        {"name": "diarization", "description": "Separate speakers in audio", "is_free": False, "credit_cost": 5},
        {"name": "call_bot", "description": "Voice call automation", "is_free": True, "credit_cost": 0},
        {"name": "chatbot", "description": "Chat assistant interaction", "is_free": True, "credit_cost": 0},
    ]

    for feature in features_data:
        await database.execute(insert(features).values(**feature))

    print("✅ Features table seeded successfully.")
    await database.disconnect()

if __name__ == "__main__":
    asyncio.run(seed_features())
