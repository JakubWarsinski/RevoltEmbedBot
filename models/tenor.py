import os
import re
import httpx

from dotenv import load_dotenv
from urllib.parse import ParseResult

load_dotenv()

API_KEY = os.getenv("TENOR_API_KEY")
USER_AGENT = "MyProject/1.0 (by hexerade on Tenor)"

async def fetch_tenor_posts(url : ParseResult) -> str | None:
    match = re.search(r"(?:-|/gif/)(\d+)(?:$|[/?])", url.path)

    if not match:
        print(f"Missing ID in Tenor URL")
        return

    post_id = match.group(1)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    params = {
        "key": API_KEY,
        "ids": post_id,
        "media_filter": "gif",
    }

    async with httpx.AsyncClient() as client:
        r = await client.get("https://tenor.googleapis.com/v2/posts", headers=headers, params=params)
       
        data = r.json()

        if not data.get("results"):
            return None

        return data["results"][0]["media_formats"]["gif"]["url"]