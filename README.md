# aipiping_L3_Shivam

This is a scalable FastAPI application that provides travel recommendations for a given country and season using the OpenAI API. The application also uses background processing and MongoDB for storing and retrieving recommendations.

## Features
- FastAPI for building the API.
- MongoDB for storing recommendations.
- OpenAI API for generating recommendations.
- Background processing with FastAPI's background tasks.
- Docker Compose for containerizing the application.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- OpenAI API Key

### Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a `.env` file in the project root with your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Build and run the application using Docker Compose:

    ```sh
    docker-compose up --build
    ```

4. The application should now be running at `http://localhost:8000`.

### Usage

#### Create Recommendations

To create a recommendation, send a `POST` request to `/recommendations/` with the country and season.

Example:

```sh
curl -X POST "http://localhost:8000/recommendations/" -H "Content-Type: application/json" -d '{"country": "Canada", "season": "winter"}'

```
### Response:

json
Copy code
{
  "uid": "unique-id"
}
Retrieve Recommendations
To retrieve a recommendation, send a GET request to /recommendations/{uid} with the UID from the previous step.

Example:

sh
Copy code
curl -X GET "http://localhost:8000/recommendations/{uid}"
Response:

json
Copy code
{
  "uid": "unique-id",
  "country": "Canada",
  "season": "winter",
  "status": "completed",
  "recommendations": [
    "Go skiing in Whistler.",
    "Experience the Northern Lights in Yukon.",
    "Visit the Quebec Winter Carnival."
  ]
}

###Code Overview
Main Application

#main.py

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
from app.database import save_recommendation, get_recommendation_status, update_recommendation_status
from app.background_tasks import fetch_recommendations

app = FastAPI()

class RecommendationRequest(BaseModel):
    country: str
    season: str

@app.post("/recommendations/")
async def create_recommendation(request: RecommendationRequest, background_tasks: BackgroundTasks):
    uid = str(uuid4())
    await save_recommendation(uid, request.country, request.season, "pending", [])
    background_tasks.add_task(fetch_recommendations, uid, request.country, request.season)
    return {"uid": uid}

@app.get("/recommendations/{uid}")
async def get_recommendation(uid: str):
    recommendation = await get_recommendation_status(uid)
    if recommendation:
        return recommendation
    return {"detail": "UID not found"}


###background_tasks.py
import os
from openai import OpenAI
from app.database import update_recommendation_status

async def fetch_recommendations(uid: str, country: str, season: str):
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": f"Recommend three things to do in {country} during {season}."}
            ]
        )
        recommendations = response.choices[0].message["content"].split("\n")
        await update_recommendation_status(uid, recommendations, "completed")
    except Exception as e:
        print(f"Error occurred: {e}")
        await update_recommendation_status(uid, [], "failed")

###database.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

client = AsyncIOMotorClient("mongodb://mongodb:27017")
db = client.recommendations_db
collection = db.recommendations

async def save_recommendation(uid: str, country: str, season: str, status: str, recommendations: list):
    await collection.insert_one({"_id": uid, "country": country, "season": season, "status": status, "recommendations": recommendations})

async def get_recommendation_status(uid: str):
    recommendation = await collection.find_one({"_id": uid})
    if recommendation:
        return {
            "uid": recommendation["_id"],
            "country": recommendation["country"],
            "season": recommendation["season"],
            "status": recommendation["status"],
            "recommendations": recommendation["recommendations"]
        }
    return None

async def update_recommendation_status(uid: str, recommendations: list, status: str):
    await collection.update_one({"_id": uid}, {"$set": {"status": status, "recommendations": recommendations}})


###Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt


###docker-compose.yml
version: '3.8'

services:
  fastapi:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"


###requirements.txt
fastapi
uvicorn
pydantic
motor
openai


