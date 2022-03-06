from discord.commands import slash_command
from discord.ext import commands
from vars import GUILD_ID


class Credit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name='ccp',
                   description='Social Credit Score',
                   guild_ids=[GUILD_ID])
    async def ccp(self, ctx):
        await ctx.respond("(我们的) You have lost all social credit! Bad job citizen, bad ! ! ! \
            You've been ban from the CCP, and shall be publically executed. Report to nearest police \
            station for punishment! Failure to comply will result in immediate execution of nearest family \
            member. Very bad! Glory to the CCP! 🇨🇳🇨🇳🇨🇳")


def setup(client):
    client.add_cog(Credit(client))
