# api/search.py
import aiohttp
from fastapi import FastAPI, Query

# ✅ This must exist and be named exactly 'app'
app = FastAPI(title="Flip-Saavn Clone API")

@app.get("/")
async def search(query: str = Query(..., description="Song or artist name")):
    async with aiohttp.ClientSession() as session:
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
                "128kbps": song.get("media_url"),
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
        "api": "Flip-Saavn Clone API",
        "cached": False,
        "query": query,
        "results": results
    }
