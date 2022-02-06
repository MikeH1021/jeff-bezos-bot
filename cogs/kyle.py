from discord.commands import slash_command
from discord.ext import commands
from vars import GUILD_ID


class Pong(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name='kyle',
                   description='Mus b Nice',
                   guild_ids=[GUILD_ID])
    async def kyle(self, ctx):
        await ctx.respond("mus b nice - Used to convey jealousy towards another person that has something that you do not. \n *Mike: Yo, Kyle I was hitting it from behind last night.* \n *Kyle: mus b nice*")


def setup(client):
    client.add_cog(Pong(client))
