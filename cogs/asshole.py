from discord.ext import commands
import random
from vars import *

class asshole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ass(self, ctx):
        await ctx.send(f"MY ASSHOLE HURTS {random.randint(1,10)}/10")


def setup(client):
    client.add_cog(asshole(client))
