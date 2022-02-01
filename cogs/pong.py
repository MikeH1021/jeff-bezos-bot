from datetime import datetime
import psutil
from discord import Color, Embed
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = datetime.now()

    @commands.command()
    async def ping(self, ctx):
        """Ping bot"""
        uptime_seconds = round(
            (datetime.now() - self.start_time).total_seconds())
        uptime = await Ping.format_seconds(self, uptime_seconds)
        ping = f'{round(self.client.latency * 1000)}ms'
        cpu_usage = f'{psutil.cpu_percent()}%'
        mem_usage = f'{psutil.virtual_memory().percent}%'
        embed = Embed(
            title='Jeff Bezos Bot Stats',
            color=Color.orange()
        )
        embed.add_field(name='Ping', value=ping)
        embed.add_field(name='Uptime', value=uptime)
        embed.add_field(name='CPU Usage', value=cpu_usage, inline=False)
        embed.add_field(name='Memory Usage', value=mem_usage)
        await ctx.send(embed=embed)

    async def format_seconds(self, time_seconds):
        """Formats some number of seconds into a string of format d days, x hours, y minutes, z seconds"""
        seconds = time_seconds
        hours = 0
        minutes = 0
        days = 0
        while seconds >= 60:
            if seconds >= 60 * 60 * 24:
                seconds -= 60 * 60 * 24
                days += 1
            elif seconds >= 60 * 60:
                seconds -= 60 * 60
                hours += 1
            elif seconds >= 60:
                seconds -= 60
                minutes += 1

        return f"{days}d {hours}h {minutes}m {seconds}s"


def setup(client):
    client.add_cog(Ping(client))
