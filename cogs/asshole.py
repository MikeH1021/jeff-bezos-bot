from discord.commands import slash_command
from discord.ext import commands
import random
from vars import GUILD_ID


class asshole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name='ass',
                   description='I like to eat ass',
                   guild_ids=[GUILD_ID])
    async def ass(self, ctx):
        await ctx.send(f"MY ASSHOLE HURTS {random.randint(1,10)}/10")


def setup(client):
    client.add_cog(asshole(client))
