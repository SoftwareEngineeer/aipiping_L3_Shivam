from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from .database import save_recommendation, get_recommendation_status
from .background_tasks import fetch_recommendations
import uuid

app = FastAPI()

class RecommendationRequest(BaseModel):
    country: str
    season: str

@app.post("/recommendations/")
async def create_recommendation(request: RecommendationRequest, background_tasks: BackgroundTasks):
    uid = str(uuid.uuid4())
    await save_recommendation(uid, request.country, request.season)
    background_tasks.add_task(fetch_recommendations, uid, request.country, request.season)
    return {"uid": uid}

@app.get("/recommendations/{uid}")
async def get_recommendation(uid: str):
    recommendation = await get_recommendation_status(uid)
    if recommendation:
        if recommendation["status"] == "completed":
            return recommendation
        return {
            "uid": uid,
            "status": recommendation["status"],
            "message": "The recommendations are not yet available. Please try again later."
        }
    return {
        "error": "UID not found",
        "message": "The provided UID does not exist. Please check the UID and try again."
    }
