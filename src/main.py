import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv

from utils.price_fetcher import fetch_token_prices
from utils.vol_fetcher import fetch_token_vols
from utils.holders_fetcher import fetch_total_holders
from utils.oi_fetcher import fetch_oi

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OI_KEY = os.getenv("OI_KEY")

MAINNET_SUSHI_ADDRESS = "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2"
DEPLOYMENT_ADDY_DOCS = "https://dev.sushi.com/docs/Developers/Deployment%20Addresses"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ****TASKS****


# Opening task, called upon init - sets "Game" to current $SUSHI price in USD
@tasks.loop(minutes=30)
async def change_price_status():
    sushi_price = fetch_token_prices({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]
    await bot.change_presence(
        activity=discord.Game(name=f"Sushi Price: ${sushi_price:.2f}")
    )


# ****COMMANDS****


# METRIC COMMANDS
# Total Volume
@bot.command(name="volume")
async def volume(ctx):
    sushi_vol = fetch_token_vols({"mainnet": [MAINNET_SUSHI_ADDRESS]})["mainnet"][
        MAINNET_SUSHI_ADDRESS
    ]

    await ctx.send(f"Current SUSHI volume: {sushi_vol:.2f}")


# NEED: 24hr + 1hr volume commands


# Current OI for SUSHI
@bot.command(name="oi")
async def oi(ctx):
    current_oi = fetch_oi(OI_KEY)

    await ctx.send(f"The current open interest for SUSHI is: {current_oi:,d}")


# Total number of SUSHI holders
@bot.command(name="holders")
async def holders(ctx):
    total_holders = fetch_total_holders({"mainnet": [MAINNET_SUSHI_ADDRESS]})

    await ctx.send(f"Current number of SUSHI holders: {total_holders}")


# TEXT COMMANDS
# Get link to deployment addresses
@bot.command(name="addresses")
async def addys(ctx):
    deployment_addys = f"All of the contract deployment addresses can be found here: [Deployment Addresses]({DEPLOYMENT_ADDY_DOCS})"

    await ctx.send(deployment_addys)


# Get total # of chains Sushi is deployed across w/ names
@bot.command(name="chains")
async def chains(ctx):
    chainz = """
    The Sushi app can be utilized across 26 different blockchains at the moment. Those chains are:
    
    Ethereum (Mainnet)
    Arbitrum One
    Arbitrum Nova
    Base
    Core
    Polygon
    Polygon zkEVM
    Optimism
    BNB Smart Chain
    Avalanche (C-Chain)
    ThunderCore
    Fantom
    Gnosis
    Metis
    Kava
    Celo
    BitTorrent
    Boba (ETH / AVAX / BNB)
    Moonbeam
    Moonriver
    Fuse
    OKXChain
    Harmony
    Palm
    Telos
    Huobi
"""

    await ctx.send(chainz)


# Important Links
@bot.command(name="links")
async def links(ctx):
    linkz = """
    Here is an official list of the most helpful links:

    [Website](https://www.sushi.com/)
    [Documentation](https://docs.sushi.com/)
    [Sushi Academy](https://www.sushi.com/academy)
    [Sushi Express](https://sushiexpress.substack.com/)
    [Blog](https://www.sushi.com/blog)
    [Governance Forum](https://forum.sushi.com/)
    [Snapshot](https://snapshot.org/#/sushigov.eth)
    [Github](https://github.com/sushiswap)
    [Twitter](https://twitter.com/SushiSwap)
"""

    await ctx.send(linkz)


# On Ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    change_price_status.start()


bot.run(TOKEN)
