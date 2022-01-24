from discord.ext import commands

class Credit(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def socialcreditscore(self,ctx):
        await ctx.send("(我们的) You have lost all social credit! Bad job citizen, bad ! ! ! You've been ban from the CCP, and shall be publically executed. Report to nearest police station for punishment! Failure to comply will result in immediate execution of nearest family member. Very bad! Glory to the CCP! 🇨🇳🇨🇳🇨🇳")

def setup(client):
    client.add_cog(Credit(client))
