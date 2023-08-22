import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv

from utils.price_fetcher import fetch_token_prices
from utils.vol_fetcher import fetch_token_vols

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MAINNET_SUSHI_ADDRESS = "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2"

client = discord.Client(intents=discord.Intents.default())


@tasks.loop(minutes=30)
async def change_price_status():
    sushi_price = fetch_token_prices({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]
    await client.change_presence(
        activity=discord.Game(name=f"Sushi Price: ${sushi_price:.2f}")
    )


@tasks.loop(minutes=30)
async def change_vol_status():
    sushi_vol = fetch_token_vols({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]

    await client.change_presence(
        activity=discord.Game(name=f"24hr Volume: ${sushi_vol:.2f}")
    )


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    change_price_status.start()
    change_vol_status.start()


client.run(TOKEN)
