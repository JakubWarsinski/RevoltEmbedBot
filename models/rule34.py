import httpx

from urllib.parse import parse_qs, ParseResult

async def fetch_rule34_posts(url : ParseResult) -> str | None:
    query = parse_qs(url.query)
    post_ids = query.get("id")

    if not post_ids:
        print(f"Missing ID in rule34 URL")
        return
    
    params = {
        "page": "dapi",
        "s": "post",
        "q": "index",
        "id" : post_ids[0],
        "json" : 1
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.rule34.xxx/index.php", params=params)

        data = resp.json()

        if not data:
            return None

        return data[0].get("file_url")