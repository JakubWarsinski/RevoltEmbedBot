import os
import httpx
from urllib.parse import parse_qs, ParseResult

IMGUR_CLIENT_ID = os.getenv("IMIGRU_API_KEY") 

async def fetch_imigru_posts(url: ParseResult) -> str | None:
    slug = url.path.split("/gallery/")[1].strip("/")
    post_id = slug.split("-")[-1]

    if not post_id:
        print("Missing ID in imigru URL")
        return None

    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    api_url = f"https://api.imgur.com/3/gallery/{post_id}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(api_url, headers=headers, timeout=10)

        payload = resp.json()

        if not payload.get("success"):
            return None
        
        data = payload.get("data", {})
        image = data.get("images", {})

        return image[0].get("link")