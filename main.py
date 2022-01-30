import os
from vars import CLIENT_TOKEN
from discord import Intents
from discord.ext import commands

# Setup Client
intents = Intents.all()
client = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive=True)


@client.command()
async def load(ctx, extension):
    """Load cog"""
    client.load_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    """Reload cog"""
    client.reload_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    """Unload cog"""
    client.unload_extension(f'cogs.{extension}')

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Run Client
client.run(CLIENT_TOKEN)
