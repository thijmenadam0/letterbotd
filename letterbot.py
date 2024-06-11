#
#
#
#

import requests
from dotenv import load_dotenv
import os
import discord
from discord import Intents, Client, Message, app_commands
from discord.ext import tasks, commands
from letterboxdpy import user
from letterboxdpy.movie import Movie
import random

# LOAD TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# SET UP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_logged = {}

    async def setup_hook(self):
        print("Setting up commands...")
        await self.load_extension('cogs.letterboxd_commands')
        await self.tree.sync()
        print("Commands synced.")


bot = MyBot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    if os.path.exists("channel.txt"):
        with open("channel.txt", "r") as inf:
            global channelID 
            channelID = inf.read().rstrip()
            film_refresh.start()
    else:
        check_initiate.start()

    with open("users.txt", "r") as file:
        for username in file.readlines():
            username = username.strip()
            try:
                user_instance = user.User(username)
                diary = user.user_diary(user_instance)
                logged = len(diary['entrys'].keys())
                bot.user_logged[username] = logged
            except AttributeError as e:
                print(f"Failed to load user '{username}': {e}")

    await bot.tree.sync()

async def film_info(ctx, ui):
    ''''''
    usericon = getattr(ui, 'avatar')
    username = getattr(ui, 'username')

    diary = user.user_diary(ui)
    logged = len(diary['entrys'].keys())
    
    if logged > bot.user_logged[username]:
        recent = list(diary['entrys'].keys())[0]
        recent_film_slug = str(diary['entrys'][recent]['slug'])

        movie_instance = Movie(recent_film_slug)
        movie_name = getattr(movie_instance, 'title')
        movie_poster = getattr(movie_instance, 'poster')
        movie_year = getattr(movie_instance, 'year')

        colors = [(255,128,0), (0,224,84), (64,188,244)]
        color_set = random.choice(colors)

        embedVar = discord.Embed(title=f'{username}', color=discord.Color.from_rgb(color_set[0], color_set[1], color_set[2]))
        embedVar.set_thumbnail(url = usericon['url'])

        rating = diary['entrys'][recent]['actions']['rating'] / 2

        embedVar.add_field(name=f'**JUST WATCHED**', value=f'{movie_name} *({movie_year})*', inline=False)

        if rating.is_integer():
            print(rating)
            embedVar.add_field(name="Rating: ", value=f'{int(rating)}/5')
        else:
            embedVar.add_field(name="Rating: ", value=f'{float(rating)}/5')
        embedVar.set_image(url = movie_poster) 

        await ctx.send(embed = embedVar)
        bot.user_logged[username] = logged


@tasks.loop(seconds=600)
async def film_refresh():
    ctx = bot.get_channel(int(channelID))
    for username in bot.user_logged.keys():
        user_instance = user.User(username)
        await film_info(ctx, user_instance)

@tasks.loop(seconds=60)
async def check_initiate():
    if os.path.exists("channel.txt"):
        with open("channel.txt", "r") as inf:
            global channelID 
            channelID = inf.read().rstrip()
            film_refresh.start()
            check_initiate.cancel()
    else:
        return




def main() -> None:
    bot.run(token=TOKEN)

    

if __name__ == "__main__":
    main()