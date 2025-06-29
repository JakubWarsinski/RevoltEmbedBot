import os
import re
import httpx
import base64

from dotenv import load_dotenv
from urllib.parse import ParseResult

load_dotenv()

USERNAME = os.getenv("E621_LOGIN")
API_KEY = os.getenv("E621_API_KEY")
USER_AGENT = "MyProject/1.0 (by hexerade on e621)"

async def fetch_e621_posts(url : ParseResult) -> str | None:
    match = re.search(r"/posts/(\d+)", url.path)
    
    if not match:
        print(f"Missing ID in e621 URL")
        return

    post_id = int(match.group(1))

    auth = base64.b64encode(f"{USERNAME}:{API_KEY}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "User-Agent": USER_AGENT,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://e621.net/posts/{post_id}.json", headers=headers)

        data = resp.json()

        if not data:
            return None

        return data["post"]["file"]["url"]