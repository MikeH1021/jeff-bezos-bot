import os
from discord import Intents
from discord.ext import commands
from vars import CLIENT_TOKEN, GROW_LOG_CH_ID, KYLE_ID, MY_ID, PY_ENV

# Setup Client
intents = Intents.all()
client = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive=True)
if PY_ENV == 'DEV':
    client.command_prefix = '.'


@client.command()
async def load(ctx, extension):
    """Load cog"""
    if ctx.author.id == MY_ID:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded: {extension}')
    elif ctx.channel.id == GROW_LOG_CH_ID and ctx.author.id == KYLE_ID:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded: {extension}')
    else:
        await ctx.send('You don\'t have permission to do that!')


@client.command()
async def reload(ctx, extension):
    """Reload cog"""
    if ctx.author.id == MY_ID:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded: {extension}')
    elif ctx.channel.id == GROW_LOG_CH_ID and ctx.author.id == KYLE_ID:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded: {extension}')
    else:
        await ctx.send('You don\'t have permission to do that!')


@client.command()
async def unload(ctx, extension):
    """Unload cog"""
    if ctx.author.id == MY_ID:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded: {extension}')
    elif ctx.channel.id == GROW_LOG_CH_ID and ctx.author.id == KYLE_ID:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded: {extension}')
    else:
        await ctx.send('You don\'t have permission to do that!')

# Load Cogs
for filename in os.listdir(f'{os.path.dirname(os.path.realpath(__file__))}/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Run Client
client.run(CLIENT_TOKEN)
