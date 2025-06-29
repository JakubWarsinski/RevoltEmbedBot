import os
import httpx

from dotenv import load_dotenv

load_dotenv()

SID = ""
LOGIN = os.getenv("INKBUNNY_LOGIN")
PASSWORD = os.getenv("INKBUNNY_PASSWORD")

async def login_to_inkbunny():
    global SID

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://inkbunny.net/api_login.php", params={
            "username": LOGIN,
            "password": PASSWORD
        })

        data = resp.json()

        SID = data.get("sid")