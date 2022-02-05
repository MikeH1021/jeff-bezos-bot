import os
from vars import *
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
            self.pepper_loop.start()
            self.mushroom_loop.start()


    async def image_helper(self, msg, camera, grow):
        camera = self.blink.cameras[f'{camera}']
        camera.snap_picture()
        await asyncio.sleep(10)
        current_time = datetime.now().timestamp()
        if grow == 'grow_log':
            image_name = f'grow-log-{current_time}'
        else:
            image_name = f'{grow}-{current_time}'
        camera.image_to_file(
            f'{os.getcwd()}/jeff-bezos-bot/img/{grow}/{image_name}.jpg')
        embed = Embed(
            title=msg,
            color=Color.green())
        file = File(
            f'{os.getcwd()}/jeff-bezos-bot/img/{grow}/{image_name}.jpg', filename='image.jpg')
        embed.set_image(url='attachment://image.jpg')
        return file, embed, image_name

    @tasks.loop(minutes=60)
    async def weed_loop(self):
        msg = "Hourly Grow Tent Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'Wiz', 'grow_log')
        await self.client.get_channel(GROW_LOG_CH_ID).send(file=file, embed=embed)

    @tasks.loop(minutes=60)
    async def pepper_loop(self):
        msg = "Hourly Pepper Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'balcony', 'pepper_log')
        await self.client.get_channel(PEPPER_LOG_CH_ID).send(file=file, embed=embed)

    @tasks.loop(minutes=60)
    async def mushroom_loop(self):
        msg = "Hourly Shroom Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.image_helper(self, msg, 'myco', 'mushroom_log')
        await self.client.get_channel(MUSHROOM_LOG_CH_ID).send(file=file, embed=embed)
        
    @mushroom_loop.after_loop
    async def after_mushroom(self):
        await asyncio.sleep(5)
        self.blink.refresh()

    @commands.command()
    async def weed(self, ctx):
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        temp = await ctx.send("Please wait..")
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'Wiz', 'grow_log')
        await ctx.send(file=file, embed=embed)
        os.remove(f'{os.getcwd()}/jeff-bezos-bot/img/grow_log/{image_name}.jpg')
        await temp.delete()
        self.blink.refresh()

    @commands.command()
    async def pepper(self, ctx):
        await ctx.message.delete()
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        temp = await ctx.send("Please wait..")
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'balcony', 'pepper_log')
        await ctx.send(file=file, embed=embed)
        os.remove(f'{os.getcwd()}/jeff-bezos-bot/img/pepper_log/{image_name}.jpg')
        await temp.delete()
        self.blink.refresh()

    @commands.command()
    async def shroom(self, ctx):
        await ctx.message.delete()
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        temp = await ctx.send("Please wait..")
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.image_helper(self, msg, 'myco', 'mushroom_log')
        await ctx.send(file=file, embed=embed)
        os.remove(f'{os.getcwd()}/jeff-bezos-bot/img/mushroom_log/{image_name}.jpg')
        await temp.delete()
        self.blink.refresh()


def setup(client):
    client.add_cog(weed(client))
