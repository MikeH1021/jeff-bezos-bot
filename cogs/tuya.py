import asyncio
from discord import AutocompleteContext
from discord.commands import Option, slash_command
from discord.ext import commands, tasks
from vars import *
import tinytuya

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

    def cog_unload(self):
        if PY_ENV == 'PROD':
            self.water_loop.cancel()
        else:
            pass

    @slash_command(name='water',
                   description='Water plants',
                   guild_ids=[GUILD_ID])
    async def water(self, ctx, arg: Option(float, 'The number of seconds to water', required=True)):
        if arg >= 20.0:
            arg = 1.0
        msg = await ctx.respond(f"Watering for {arg} seconds.. Please wait.")
        d = tinytuya.OutletDevice(
            '80527250a4e57c11e7b9', '192.168.0.102', '09c7bef14266a54d')
        d.set_version(3.3)
        d.turn_on()
        await asyncio.sleep(arg)
        d.turn_off()
        await msg.edit_original_message("Watering complete - maximum moisture acheived. ;)")

    async def get_lights(self, ctx: AutocompleteContext):
        """Return available options for light command"""
        return ['on', 'off']

    @slash_command(name='light',
                   description='Control grow tent lights',
                   guild_ids=[GUILD_ID])
    async def light(self, ctx, arg: Option(str, 'on or off', autocomplete=get_lights)):
        d = tinytuya.OutletDevice(
            '30103770f4cfa2194159', '192.168.0.220', '69756f2b239d20db')
        d.set_version(3.3)
        if arg == 'on':
            d.turn_on()
        elif arg == 'off':
            d.turn_off()
        else:
            await ctx.respond("something went wrong")
        if arg is not None:
            await ctx.respond(f"light set to {arg}")

    @slash_command(name='watertime',
                   description='Change Tuya hourly watering duration',
                   guild_ids=[GUILD_ID])
    async def watertime(self, ctx, arg: Option(float, 'The number of seconds to water for', required=True, defualt=5.0)):
        global WATER_TIME
        if arg >= 35.0:
            arg = 20.0
        WATER_TIME = arg
        await ctx.respond(f"Watering duration changed to {WATER_TIME}!!")

    @tasks.loop(minutes=60)
    async def water_loop(self):
        d = tinytuya.OutletDevice(
            '80527250a4e57c11e7b9', '192.168.0.102', '09c7bef14266a54d')
        d.set_version(3.3)
        d.turn_on()
        await asyncio.sleep(WATER_TIME)
        d.turn_off()
        await self.client.get_channel(PEPPER_LOG_CH_ID).send(f"Scheduled watering executed for {WATER_TIME} seconds.")

    @water_loop.before_loop
    async def before_water_loop(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(tuya(client))
