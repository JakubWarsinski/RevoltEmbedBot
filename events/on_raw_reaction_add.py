import re
from revolt import Client, Channel, Message

IGNORED_IDS = {"01JY9GE919G8YMC9Y9CXG6KKFP"}

async def on_raw_reaction_add_event(self: Client, payload: dict):
    user_id = payload["user_id"]
    
    if user_id in IGNORED_IDS:
        return

    if payload["emoji_id"] != "❌":
        return

    channel: Channel = await self.fetch_channel(payload["channel_id"])
    bot_msg: Message = await channel.fetch_message(payload["id"])

    content = bot_msg.content

    hinned_id = re.search(r"!\[([^\]]+)\]\(", content)
    
    hinned_id = hinned_id.group(1)
    
    if not hinned_id:
        return

    if user_id == hinned_id:
        await bot_msg.delete()