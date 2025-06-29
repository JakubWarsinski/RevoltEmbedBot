from models.rule34 import fetch_rule34_posts
from models.e621 import fetch_e621_posts
from models.inkbunny import fetch_inkbunny_posts
from models.tenor import fetch_tenor_posts
from models.imigru import fetch_imigru_posts

SUPPORTED_DOMAINS: dict[str, callable] = {
    "rule34.xxx": fetch_rule34_posts,
    "e621.net": fetch_e621_posts,
    "inkbunny.net": fetch_inkbunny_posts,
    "tenor.com": fetch_tenor_posts,
    "imgur.com": fetch_imigru_posts
}