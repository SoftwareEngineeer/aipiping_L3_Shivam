import os
import openai
from .database import update_recommendation_status

# Initialize the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

async def fetch_recommendations(uid: str, country: str, season: str):
    try:
        print(f"Starting background task for UID: {uid}, Country: {country}, Season: {season}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": f"Recommend three things to do in {country} during the {season}."}
            ]
        )
        print(f"OpenAI Response: {response}")
        recommendations = response['choices'][0]['message']['content'].strip().split('\n')
        await update_recommendation_status(uid, recommendations, "completed")
        print(f"Recommendations for UID: {uid} have been updated to completed.")
    except Exception as e:
        print(f"Error occurred: {e}")
        await update_recommendation_status(uid, [], "failed")
        print(f"Recommendations for UID: {uid} have been updated to failed.")
