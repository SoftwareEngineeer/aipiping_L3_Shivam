import asyncio
from background_tasks import fetch_recommendations

uid = "65725b60-df39-4a99-a6d6-9086715bee2b"
country = "Canada"
season = "winter"

async def test():
    await fetch_recommendations(uid, country, season)

if __name__ == "__main__":
    asyncio.run(test())
