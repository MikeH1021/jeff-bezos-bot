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

    async def weed_helper(self, msg):
        camera = self.blink.cameras['Wiz']
        camera.snap_picture()
        await asyncio.sleep(10)
        self.blink.refresh()
        current_time = datetime.now().timestamp()
        image_name = f'grow-log-{current_time}'
        camera.image_to_file(
            f'{os.getcwd()}/jeff-bezos-bot/img/grow_log/{image_name}.jpg')
        embed = Embed(
            title=msg,
            color=Color.green())
        file = File(
            f'{os.getcwd()}/jeff-bezos-bot/img/grow_log/{image_name}.jpg', filename='image.jpg')
        embed.set_image(url='attachment://image.jpg')
        return file, embed, image_name

    @tasks.loop(minutes=60)
    async def weed_loop(self):
        msg = "Hourly Grow Tent Update... Sponsored by Daddy Bezos"
        file, embed, _ = await weed.weed_helper(self, msg)
        await self.client.get_channel(LOG_CH_ID).send(file=file, embed=embed)

    @commands.command()
    async def weed(self, ctx):
        if ctx.channel.id == KYLE_LOG_CH_ID:
            return
        temp = await ctx.send("Please wait..")
        msg = "Here's your pic, you filthy animal."
        file, embed, image_name = await weed.weed_helper(self, msg)
        await ctx.send(file=file, embed=embed)
        os.remove(f'{os.getcwd()}/jeff-bezos-bot/img/grow_log/{image_name}.jpg')
        await temp.delete()


def setup(client):
    client.add_cog(weed(client))
