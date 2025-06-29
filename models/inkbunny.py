import re
import httpx
import utils.inkbunny_login as ink

from urllib.parse import ParseResult

async def fetch_inkbunny_posts(url : ParseResult) -> str | None:
    match = re.search(r"/s/(\d+)", url.path)

    if not match:
        print(f"Missing ID in Inkbunny URL")
        return

    post_id = int(match.group(1))
    
    if not ink.SID:
        await ink.login_to_inkbunny()

    sid = ink.SID
    
    return await make_request(sid, post_id, 0)
    

async def make_request(sid, post_id, attempt):
    if attempt > 1:
        return
    
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://inkbunny.net/api_submissions.php", params={
            "sid": sid,
            "submission_ids": post_id,
        })

        data = resp.json()
        
        if data.get("error_code") == 10010:
            await ink.login_to_inkbunny()
            return await make_request(sid, post_id, (attempt + 1))

        return data["submissions"][0]["file_url_full"]