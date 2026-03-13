# app.py
import aiohttp
from fastapi import FastAPI, Query

app = FastAPI(title="Flip-Saavn Clone API")

BASE_URL = "https://www.jiosaavn.com/api.php"  # Example, we'll fetch search results

@app.get("/search")
async def search(query: str = Query(..., description="Song or artist name")):
    """
    Search songs by query and return JSON like Flip-Saavn API
    """
    async with aiohttp.ClientSession() as session:
        # Example: JioSaavn unofficial API call
        search_url = f"https://www.saavn.com/api.php?__call=search.getResults&q={query}&_format=json&_marker=0"
        async with session.get(search_url) as resp:
            data = await resp.json()

    results = []
    for song in data.get("songs", {}).get("data", []):
        results.append({
            "title": song.get("name"),
            "artist": song.get("primaryArtists"),
            "id": song.get("id"),
            "language": song.get("language"),
            "download": {
                "128kbps": song.get("media_url"),  # or you can fetch higher quality
            },
            "image": {
                "50x50": song.get("image"),
                "150x150": song.get("image"),
                "500x500": song.get("image"),
            },
            "duration": song.get("duration"),
            "jiosaavn": f"https://www.jiosaavn.com/song/{song.get('perma_url')}"
        })

    return {
        "api": "Your Flip-Saavn Clone API",
        "cached": False,
        "query": query,
        "results": results
    }
