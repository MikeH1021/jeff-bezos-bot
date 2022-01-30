from discord.ext import commands


class Pong(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kyle(self, ctx):
        await ctx.send("mus b nice - Used to convey jealousy towards another person that has something that you do not. \n *Mike: Yo, Kyle I was hitting it from behind last night.* \n *Kyle: mus b nice*")


def setup(client):
    client.add_cog(Pong(client))
