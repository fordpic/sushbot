import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv

from utils.price_fetcher import fetch_token_prices
from utils.vol_fetcher import fetch_token_vols

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MAINNET_SUSHI_ADDRESS = "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# TASKS
# Opening task, called upon init - sets "Game" to current $SUSHI price in USD
@tasks.loop(minutes=30)
async def change_price_status():
    sushi_price = fetch_token_prices({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]
    await bot.change_presence(
        activity=discord.Game(name=f"Sushi Price: ${sushi_price:.2f}")
    )


# COMMANDS
# 24h volume
@bot.command(name="volume")
async def volume(ctx):
    sushi_vol = fetch_token_vols({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]

    await ctx.send(f"Current SUSHI volume: {sushi_vol:.2f}")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    change_price_status.start()


bot.run(TOKEN)
