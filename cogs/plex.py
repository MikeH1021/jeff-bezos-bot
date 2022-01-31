import discord
from discord.ext import commands
from urllib.request import Request, urlopen
from time import sleep
import json
import os
import io
from pyarr import RadarrAPI
from datetime import date
import sys
import asyncio
from vars import *

radarr = RadarrAPI(R_HOST_URL, R_TOKEN)
# Last search json file
last_search = os.path.join(os.path.dirname(__file__), f'last_search.json')
# Set your avg download time per movie - in seconds
avg_time_download = 30
avg_time_seconds = avg_time_download * 60

embed = discord.Embed()


class Plex(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def movie(self, ctx, *args):
        if ctx.channel.id == MOVIES_CH_ID:
            current_requester = ctx.author
            current_channel = ctx.channel.id
            player_choice = None
            req_movie = " ".join(args[:])
            str_req_movie = req_movie.title()
            await ctx.send(f"Searching for {req_movie.title()}")
            await asyncio.sleep(1)
            await ctx.send(f"One moment...")
            await asyncio.sleep(1)
            req_movie_rep = ""
            for x in req_movie:
                if x == " ":
                    req_movie_rep += "%"
                elif x.isalpha() == False and x.isdigit() == False:
                    pass
                else:
                    req_movie_rep += x
            google_search_req = ""
            for x in req_movie_rep:
                if x == "%":
                    google_search_req += "+"
                else:
                    google_search_req += x
            req_movie = req_movie_rep
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
            req = Request(
                url=f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_TOKEN}&query={req_movie}", headers=headers)
            html = urlopen(req)
            html = json.load(html)
            if html == {"page": 1, "results": [], "total_pages": 0, "total_results": 0}:
                if "%" in req_movie:
                    req_movie_rep = ""
                    for x in req_movie:
                        if x == "%":
                            req_movie_rep += "-"
                        else:
                            req_movie_rep += x
                    req_movie = req_movie_rep
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
                    req = Request(
                        url=f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_TOKEN}&query={req_movie}", headers=headers)
                    html = urlopen(req)
                    html = json.load(html)
                    if html == {"page": 1, "results": [], "total_pages": 0, "total_results": 0}:
                        await ctx.send(f"No results found for '{str_req_movie}'")
                        await asyncio.sleep(1)
                        await ctx.send(f"Let's try searching the internet for it...")
                        await asyncio.sleep(1)
                        await ctx.send(f"https://letmegooglethat.com/?q={google_search_req}%3F")
                        return
                else:
                    await ctx.send(f"No results found for '{str_req_movie}'")
                    await asyncio.sleep(1)
                    await ctx.send(f"Let's try searching the internet for it...")
                    await asyncio.sleep(1)
                    await ctx.send(f"https://letmegooglethat.com/?q={google_search_req}%3F")
                    return
            print_list = {}
            for x in html["results"]:
                x["release_date"] = x.get(
                    "release_date", "Release date unavailable")
                x["title"] = x.get("title", "Title unavailable")
                poster_suffix = x.get(
                    "poster_path", "/dykOcAqI01Fci5cKQW3bEUrPWwU.jpg")
                x["poster_path"] = (
                    f"https://image.tmdb.org/t/p/original{poster_suffix}")
                x["overview"] = x.get("overview", "Description unavailable.")
                # x["id"] = x.get("id", )
                if x["overview"] == "":
                    x["overview"] = "Description unavailable."
                if "jpg" not in x["poster_path"]:
                    x["poster_path"] = "https://i.imgur.com/1glpRCZ.png?1"
                print_list[x["original_title"]] = [
                    x["id"], x["poster_path"], x["title"], x["release_date"], x["overview"]]
            with io.open(last_search, "w", encoding="UTF-8") as last_search_w:
                json.dump(print_list, last_search_w)
            with io.open(last_search, "r", encoding="UTF-8") as last_search_r:
                list_of_movies = json.load(last_search_r)
            selected_movie_id = ""
            selected_movie = ""
            number_of_results = len(list_of_movies.keys())
            count_1 = 0
            await ctx.send(f"Displaying results... \nType 'stop' to cancel search, or 'startover' to restart your search.")
            await asyncio.sleep(1)
            while True:
                for x, y in list_of_movies.items():
                    await ctx.send("Is this the correct movie? ('yes' or 'no')")
                    await asyncio.sleep(1)
                    embed.set_image(url=y[1])
                    await ctx.send(embed=embed)
                    await ctx.send(f"`{y[2]} ({y[3]})`\n```{y[4]}```")
                    
                    player_choice = await self.client.wait_for('message', check=lambda message: message.author == current_requester and message.channel.id == current_channel and message.content.lower().strip() in ["yes", "y", "startover", "stop", "no", "n", ])
                    if player_choice.content.lower().strip() == "yes" or player_choice.content.lower().strip() == "y":
                        selected_movie = (f"{y[2]} ({y[3]})")
                        await ctx.send(f"Selected: `{selected_movie}`")
                        await asyncio.sleep(2)
                        selected_movie_id = y[0]
                        break
                    elif player_choice.content.lower().strip() == "startover":
                        await ctx.send(f"Starting search over...")
                        await asyncio.sleep(1)
                        break
                    elif player_choice.content.lower().strip() == "stop":
                        await ctx.send(f"Cancelling search... Have a good day!")
                        await asyncio.sleep(1)
                        return
                    elif player_choice.content.lower().strip() == "no" or player_choice.content.lower().strip() == "n":
                        count_1 += 1
                        if count_1 == number_of_results:
                            await ctx.send(f"Unfortunately, we have run out of results.")
                            await asyncio.sleep(1)
                            await ctx.send(f"It's possible that this movie does not exist, let's check if it does and try again...")
                            await asyncio.sleep(1)
                            await ctx.send(f"https://letmegooglethat.com/?q={google_search_req}%3F")
                            return
                        else:
                            pass
                if player_choice.content.lower().strip() == "yes" or player_choice.content.lower().strip() == "y":
                    break
                elif player_choice.content.lower().strip() == "startover":
                    pass
            add_movie = radarr.add_movie(selected_movie_id, 1, '/mnt/user/Media/Movies')
            if str(type(add_movie)) == "<class 'list'>":
                await ctx.send(f"Looks like this movie is already available on {SERVER_NAME}, if not, please contact {ADMIN_NAME}.")
                return
            else:
                await ctx.send(f"Movie is being downloaded to {SERVER_NAME}.")
                await asyncio.sleep(1)
                await ctx.send(f"Please wait: {avg_time_download} minute(s)...")
                await asyncio.sleep(avg_time_seconds)
                movie_check = radarr.get_movie(selected_movie_id)
                try:
                    radarr_id = movie_check[0]["movieFile"]['id']
                    if radarr.get_movie_file(radarr_id) == {'message': 'NotFound'}:
                        await ctx.send(f"{SERVER_NAME} is having trouble finding `{selected_movie}`, please check server frequently for updates as this may be added at a later time.")
                    else:
                        await ctx.send(f"`{selected_movie}` is now available on {SERVER_NAME}. Enjoy!")
                except:
                    await ctx.send(f"{SERVER_NAME} is having trouble finding `{selected_movie}`, please check server frequently for updates as this may be added at a later time.")
        else:
            msg = await ctx.send(f'<@{ctx.author.id}> Please use <#{MOVIES_CH_ID}> for that!')
            await asyncio.sleep(10)
            await msg.delete()

def setup(client):
    client.add_cog(Plex(client))
