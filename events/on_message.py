import re
from revolt import Message
from urllib.parse import urlparse
from config import SUPPORTED_DOMAINS
import utils.domain_timer as limit_timer

async def on_message_event(message: Message):
    if message.author.bot or not message.content or message.content.startswith("!"):
        return

    content_stripped = message.content.strip()
    
    urls = re.findall(r'https?://\S+', content_stripped)
    
    if not urls:
        return

    buffer: list[str] = []
    seen: set[str] = set()

    for url in urls:
        if url in seen:
            continue
        
        seen.add(url)

        try:
            parsed = urlparse(url)
        except ValueError:
            continue

        host = parsed.netloc.lower().lstrip("www.")
        handler = SUPPORTED_DOMAINS.get(host)

        if handler is None:
            print(f"Unsupported domain: {host}")
            continue

        await limit_timer.rate_limit(host)

        try:
            result = await handler(parsed)
        except Exception as e:
            print(f"[{host}] error: {e}")
            continue

        if result:
            buffer.append(result)

    if not buffer or len(buffer) < 0:
        return

    user_id = message.author.id
    content  = "##### ❌ - remove message as author"

    lines = [f"![{user_id}]({url})" for url in buffer]

    for line in lines:
        content += f" {line}"

    new_message = await message.reply(content=content, mention=False)
    await new_message.add_reaction("❌")