import os
from vars import *
from discord.commands import slash_command
from discord.ext import commands, tasks
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import asyncio
from discord import Color, Embed, File
from datetime import datetime


class weed(commands.Cog):
    def __init__(self, client):
        self.client = client
        if PY_ENV == 'PROD':
            self.blink = Blink()
            self.auth = Auth({"username": BLINK_USERNAME,
                              "password": BLINK_PASSWORD}, no_prompt=True)
            self.blink.auth = self.auth
            self.blink.start()
            self.weed_loop.start()
            self.mushroom_loop.start()
            self.pepper_loop.start()

    def cog_unload(self):
        if PY_ENV == 'PROD':
            self.weed_loop.cancel()
            self.pepper_loop.cancel()
            self.mushroom_loop.cancel()
        else:
            pass

    async def image_helper(self, msg, camera, grow):
        try:
            camera = self.blink.cameras[f'{camera}']
            camera.snap_picture()
            self.blink.refresh()
            current_time = datetime.now().timestamp()
            if grow == 'grow_log':
                image_name = f'grow-log-{current_time}'
            else:
                image_name = f'{grow}-{current_time}'
            await asyncio.sleep(5)
            camera.image_to_file(
                f'{os.getcwd()}/jeff-bezos-bot/img/{grow}/{image_name}.jpg')
            embed = Embed(
                title=msg,
                color=Color.green())
            file = File(
                f'{os.getcwd()}/jeff-bezos-bot/img/{grow}/{image_name}.jpg', filename='image.jpg')
            embed.set_image(url='attachment://image.jpg')
            return file, embed, image_name
        except Exception as e:
            print(e)

    @tasks.loop(minutes=60)
    async def weed_loop(self):
        await asyncio.sleep(5)
        msg = "Hourly Grow Tent Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'wiz', 'grow_log')
        await self.client.get_channel(GROW_LOG_CH_ID).send(file=file, embed=embed)

    @weed_loop.before_loop
    async def before_weed_loop(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes=60)
    async def pepper_loop(self):
        await asyncio.sleep(10)
        msg = "Hourly Pepper Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'balcony', 'pepper_log')
        await self.client.get_channel(PEPPER_LOG_CH_ID).send(file=file, embed=embed)

    @pepper_loop.before_loop
    async def before_pepper_loop(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes=60)
    async def mushroom_loop(self):
        await asyncio.sleep(20)
        msg = "Hourly Shroom Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'myco', 'mushroom_log')
        await self.client.get_channel(MUSHROOM_LOG_CH_ID).send(file=file, embed=embed)

    @mushroom_loop.before_loop
    async def before_mushroom_loop(self):
        await self.client.wait_until_ready()

    @slash_command(name='weed',
                   description='Get live pic of grow tent',
                   guild_ids=[GUILD_ID])
    async def weed(self, ctx):
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        embed = Embed(title='Please wait...',
                      color=Color.green())
        tmp = await ctx.respond(embed=embed)
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'wiz', 'grow_log')
        await tmp.edit_original_message(file=file, embed=embed)
        await asyncio.sleep(1200)
        os.remove(f'{os.getcwd()}/jeff-bezos-bot/img/grow_log/{image_name}.jpg')

    @slash_command(name='pepper',
                   description='Get live pic of peppers',
                   guild_ids=[GUILD_ID])
    async def pepper(self, ctx):
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        embed = Embed(title='Please wait...',
                      color=Color.green())
        tmp = await ctx.respond(embed=embed)
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'balcony', 'pepper_log')
        await tmp.edit_original_message(file=file, embed=embed)
        await asyncio.sleep(1200)
        os.remove(
            f'{os.getcwd()}/jeff-bezos-bot/img/pepper_log/{image_name}.jpg')

    @slash_command(name='shroom',
                   description='Get live pic of shrooms',
                   guild_ids=[GUILD_ID])
    async def shroom(self, ctx):
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        embed = Embed(title='Please wait...',
                      color=Color.green())
        tmp = await ctx.respond(embed=embed)
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'myco', 'mushroom_log')
        await tmp.edit_original_message(file=file, embed=embed)
        await asyncio.sleep(1200)
        os.remove(
            f'{os.getcwd()}/jeff-bezos-bot/img/mushroom_log/{image_name}.jpg')


def setup(client):
    client.add_cog(weed(client))
