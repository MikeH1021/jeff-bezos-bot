from discord import Color, Embed
from discord.ext import commands, tasks
from vars import *
import tinytuya
import asyncio
import random

WATER_TIME = 5.0

c = tinytuya.Cloud(
    apiRegion="us",
    apiKey=TUYA_API_KEY,
    apiSecret=TUYA_API_SECRET,
    apiDeviceID=TUYA_DEVICE_ID)


class tuya(commands.Cog):
    def __init__(self, client):
        self.client = client
        if PY_ENV == 'PROD':
            self.water_loop.start()

    @commands.cooldown(1, 1000, commands.BucketType.user)
    @commands.command()
    async def water(self, ctx, arg=1.0):
        print(arg)
        if float(arg) >= 20.0:
            arg = 1.0
        await ctx.send(f"Watering for {arg} seconds.. Please wait.")
        d = tinytuya.OutletDevice(
            '80527250a4e57c11e7b9', '192.168.0.102', '09c7bef14266a54d')
        d.set_version(3.3)
        data = d.status()
        d.turn_on()
        await asyncio.sleep(float(arg))
        d.turn_off()
        await ctx.send("Watering complete - maximum moisture acheived. ;)")

    @water.error
    async def water_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = Embed(title=f"Slow it down bro!",
                          description=f"Try again in {error.retry_after:.2f}s.", color=Color.red())
            await ctx.send(f'<@{ctx.author.id}>', embed=embed)
            print("spamming detected, rate-limiting activated")

    @commands.command()
    async def light(self, ctx, arg=None):
        print(arg)
        d = tinytuya.OutletDevice(
            '30103770f4cfa2194159', '192.168.0.220', '69756f2b239d20db')
        d.set_version(3.3)
        data = d.status()
        if arg == 'on':
            d.turn_on()
        elif arg == 'off':
            d.turn_off()
        else:
            await ctx.send("stop being a fucking idiot and put in a real arg")
        if arg is not None:
            await ctx.send(f"light set to {arg}")

    @commands.command()
    async def watertime(self, ctx, arg=None):
        global WATER_TIME
        if float(arg) >= 35.0:
            arg = 20.0
        WATER_TIME = float(arg)
        await ctx.send(f"Watering duration changed to {WATER_TIME}!!")

    @tasks.loop(minutes=60)
    async def water_loop(self):
        d = tinytuya.OutletDevice(
            '80527250a4e57c11e7b9', '192.168.0.102', '09c7bef14266a54d')
        d.set_version(3.3)
        data = d.status()
        d.turn_on()
        await asyncio.sleep(WATER_TIME)
        d.turn_off()
        await self.client.get_channel(LOG_CH_ID).send(f"Scheduled watering executed for {WATER_TIME} seconds.")

    # async def water_level(self, d):
    #     pass


def setup(client):
    client.add_cog(tuya(client))
