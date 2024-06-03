from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://mongodb:27017")
db = client.travel
collection = db.recommendations

async def save_recommendation(uid: str, country: str, season: str):
    await collection.insert_one({
        "_id": uid,
        "country": country,
        "season": season,
        "status": "pending",
        "recommendations": []
    })

async def update_recommendation_status(uid: str, recommendations: list, status: str):
    await collection.update_one(
        {"_id": uid},
        {"$set": {"recommendations": recommendations, "status": status}}
    )

async def get_recommendation_status(uid: str):
    return await collection.find_one({"_id": uid})
