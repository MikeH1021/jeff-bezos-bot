from discord import Color, Embed
from discord.ext import commands
import requests
import os
import json
# from pyarr import SonarrAPI
import tvdb_v4_official
import asyncio
from vars import *

AVG_DOWNLOAD_TIME = 60

# sonarr = SonarrAPI(S_HOST_URL, S_TOKEN)
tvdb = tvdb_v4_official.TVDB(TVDB_API_KEY, pin=TVDB_PIN)


class PlexSonarr(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx, *args):
        req_movie = ' '.join(args)
        shows = tvdb.get_all_series(1, req_movie)
        # shows2 = tvdb.get_series()
        # shows3 = tvdb.get_series_extended()
        print(shows)

    # async def create_movie_embed(self, movie):
    #     title = f"{movie['title']} | {movie['description']}"
    #     img_url = movie['image']
    #     movie_url = f"{IMDB_BASE_URL}{movie['id']}/"
    #     embed = Embed(
    #         title=title,
    #         color=Color.blue(),
    #         url=movie_url
    #     )
    #     embed.set_image(url=img_url)
    #     return embed

    # @commands.command()
    # async def movie(self, ctx, *args):
    #     if ctx.channel.id == MOVIES_CH_ID:
    #         await ctx.message.delete()
    #         req_movie = ' '.join(args)
    #         tmp = await ctx.send(f'Searching for {req_movie.title()}. One moment...')
    #         url = f'{IMDB_MOVIE_BASE_URL}{req_movie}'
    #         response = requests.get(url).json()
    #         result_cnt = 0
    #         for movie in response['results']:
    #             result_cnt += 1

    #         embed_flag = False
    #         movie_embed = None
    #         while True:
    #             tmp2 = await ctx.send(f'Displaying results. Type `cancel` to stop search')
    #             await asyncio.sleep(1)
    #             tmp3 = await ctx.send('Is this the correct movie? (`yes` or `no`)')
    #             for movie in response['results']:
    #                 embed = await PlexSonarr.create_movie_embed(self, movie)
    #                 if embed_flag:
    #                     movie_embed = await movie_embed.edit(embed=embed)
    #                 else:
    #                     movie_embed = await ctx.send(embed=embed)
    #                     embed_flag = True

    #                 def check(message):
    #                     return message.author == ctx.author and message.channel.id == ctx.channel.id and message.content.lower().strip() in ['yes', 'y', 'no', 'n', 'cancel']

    #                 message = await self.client.wait_for('message', timeout=300, check=check)
    #                 movie_choice = message.content.lower().strip()
    #                 if movie_choice == 'yes' or movie_choice == 'y':
    #                     await message.delete()
    #                     selected_movie = movie['title']
    #                     select_msg = await ctx.send(f'Selected: {selected_movie}')
    #                     selected_movie_id = movie['id']
    #                     break
    #                 elif movie_choice == 'no' or movie_choice == 'n':
    #                     await message.delete()
    #                     result_cnt -= 1
    #                     if result_cnt == 0:
    #                         await tmp.delete()
    #                         await tmp2.delete()
    #                         await tmp3.delete()
    #                         await movie_embed.delete()
    #                         msg = await ctx.send(f'We have run out of results searching for {req_movie.title()}.')
    #                         await asyncio.sleep(10)
    #                         await msg.delete()
    #                         return
    #                     else:
    #                         pass
    #                 elif movie_choice == 'cancel':
    #                     await message.delete()
    #                     await tmp.delete()
    #                     await tmp2.delete()
    #                     await tmp3.delete()
    #                     await movie_embed.delete()
    #                     msg = await ctx.send('Search cancelled!')
    #                     await asyncio.sleep(10)
    #                     await msg.delete()
    #                     return
    #             if movie_choice == 'yes' or movie_choice == 'y':
    #                 await tmp.delete()
    #                 await tmp2.delete()
    #                 await tmp3.delete()
    #                 break
    #         add_movie = radarr.add_movie(
    #             selected_movie_id, 1, '/mnt/user/Media/Movies', True, True, False)
    #         if str(type(add_movie)) == "<class 'list'>":
    #             await select_msg.delete()
    #             await movie_embed.delete()
    #             msg = await ctx.send(f"Looks like this movie is already available on {SERVER_NAME}, if not, please contact {ADMIN_NAME}.")
    #             await asyncio.sleep(10)
    #             await msg.delete()
    #             return
    #         else:
    #             await select_msg.delete()
    #             tmp = await ctx.send(f"Movie is being downloaded to {SERVER_NAME}.")
    #             await asyncio.sleep(1)
    #             tmp2 = await ctx.send(f"Please wait: {AVG_DOWNLOAD_TIME} minute(s)...")
    #             avg_time_seconds = AVG_DOWNLOAD_TIME * 60
    #             await asyncio.sleep(10)
    #             await tmp.delete()
    #             await tmp2.delete()
    #             await asyncio.sleep(avg_time_seconds)
    #             movie_check = radarr.get_movie(selected_movie_id)
    #             try:
    #                 radarr_id = movie_check[0]["movieFile"]['id']
    #                 if radarr.get_movie_file(radarr_id) == {'message': 'NotFound'}:
    #                     msg = await ctx.send(f"{SERVER_NAME} is having trouble finding `{selected_movie}`, please check server frequently for updates as this may be added at a later time.")
    #                     await asyncio.sleep(10)
    #                     await msg.delete()
    #                 else:
    #                     msg = await ctx.send(f"`{selected_movie}` is now available on {SERVER_NAME}. Enjoy!")
    #                     await asyncio.sleep(10)
    #                     await msg.delete()
    #             except:
    #                 msg = await ctx.send(f"{SERVER_NAME} is having trouble finding `{selected_movie}`, please check server frequently for updates as this may be added at a later time.")
    #                 await asyncio.sleep(10)
    #                 await msg.delete()
    #     else:
    #         msg = await ctx.send(f'<@{ctx.author.id}> Please use <#{MOVIES_CH_ID}> for that!')
    #         await asyncio.sleep(10)
    #         await msg.delete()

    # @commands.command()
    # async def sonarrtime(self, ctx, arg):
    #     global AVG_DOWNLOAD_TIME
    #     AVG_DOWNLOAD_TIME = int(arg)
    #     msg = await ctx.send(f'Plex TV show average download time updated to {arg} minutes')
    #     await asyncio.sleep(10)
    #     await msg.delete()


def setup(client):
    client.add_cog(PlexSonarr(client))
