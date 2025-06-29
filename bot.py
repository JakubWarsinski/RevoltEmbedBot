import os
import asyncio
import webserver
import revolt

from dotenv import load_dotenv
from revolt import Message, Client
from revolt.utils import client_session
from events.on_message import on_message_event
from events.on_raw_reaction_add import on_raw_reaction_add_event

load_dotenv()

TOKEN = os.getenv("TOKEN")

class Client(revolt.Client):
    async def on_ready(self):
        print("Bot is ready!")

    async def on_message(self, message: Message):
        await on_message_event(message)

    async def on_raw_reaction_add(self: Client, payload):        
        await on_raw_reaction_add_event(self, payload)

async def main():
    await asyncio.gather(
        webserver.start_web(),
        run_bot()
    )

async def run_bot():
    async with client_session() as session:
        client = Client(session, TOKEN)
        await client.start()

asyncio.run(main())