import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv

from utils.price_fetcher import fetch_token_prices

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MAINNET_SUSHI_ADDRESS = "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2"
